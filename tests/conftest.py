"""
This module provides reusable fixtures and configurations for the test session
"""
import pytest
import logging as logs

from faker import Faker
 
from app.app_settings import AppSettings
from app.database import DatabaseClient

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
        settings = AppSettings()
        settings.database_url = "postgresql://user:password@localhost:5432/test_db"
        return settings

# =============================================================================
# Database Fixtures
# =============================================================================

face = Faker()
Faker.seed(12345)

@pytest.fixture(scope="module")
def test_db(request, test_settings):
    """Provides a test-scoped database configuration"""

    logger.info(f"Deploying Test Database at {test_settings.database_url}...")
    test_client = DatabaseClient()
    engine = test_client.engine

    logger.info("Dropping existing tables...")
    test_client.model_base.metadata.drop_all(bind=engine)

    logger.info("Creating tables for test session...")
    test_client.model_base.metadata.create_all(bind=engine)












