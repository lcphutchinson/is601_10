"""
This module provides reusable fixtures and configurations for the test session
"""
import os
import pytest
import logging as logs

from contextlib import contextmanager
from faker import Faker
 
from app.settings import GlobalSettings
from app.database_client import DatabaseClient

# =============================================================================
# Logging Configuration
# =============================================================================

logs.basicConfig(
    level=logs.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logs.getLogger(__name__)

# =============================================================================
# Application Settings Fixture
# =============================================================================

@pytest.fixture(scope="session", autouse=True)
def test_settings(request):
    """Provides a test-scoped settings singleton"""
    if 'suspend_autouse' in request.keywords:
        yield
    else:
        os.environ['DATABASE_URL'] = \
            "postgresql://user:password@localhost:5432/test_db"
        settings = GlobalSettings()
        yield settings

# =============================================================================
# Database Fixtures
# =============================================================================

@pytest.fixture(scope="session", autouse=True)
def test_db(request, test_settings):
    """Provides a test-scoped database configuration"""

    logger.info(f"Deploying Test Database at {test_settings.DATABASE_URL}...")
    test_client = DatabaseClient()
    engine = test_client.engine

    logger.info("Dropping existing tables...")
    test_client.model_base.metadata.drop_all(bind=engine)

    logger.info("Creating tables for test session...")
    test_client.model_base.metadata.create_all(bind=engine)
    
    yield test_client

    if request.config.getoption("--preserve-db"):
        logger.info("'--preserve-db' option detected: skipping data teardown")
    else:
        logger.info("Beginning database teardown...")
        test_client.model_base.metadata.drop_all(bind=engine)
        logger.info("Database teardown complete.")

@contextmanager
def managed_db_session(test_db):
    """
    Context manager for safe database session handling
    Automatically handles rollback and cleanup

    Example:
        with managed_db_session() as session:
            user = session.query(User).first()
    """
    session = test_db.get_session()
    try:
        yield session
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

# =============================================================================
# Data Record Fixtures & Methods
# =============================================================================

@pytest.fixture(scope="session", autouse=True)
def data_faker(request):
    """Provides a seeded generator for repeatable test data"""
    Faker.seed(12345)
    yield Faker()

def generate_user_data() -> dict[str, str]:
    """
    Helper funciton for generating user data values

    Returns
    -------
    dict[str, str]
        A dict containing user fields with faked data
    """
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "username": fake.unique.user_name(),
        "password": fake.password(length=12)
    }















