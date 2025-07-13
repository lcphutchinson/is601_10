"""This module provides a central interface for accessing global settings"""

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

class AppSettings(BaseSettings):
    _instance: 'AppSettings' = None
    _is_configured: bool = False

    @classmethod
    def __new__(cls, *args, **kwargs) -> 'AppSettings':
        if not cls._instance:
            cls._instance = super(AppSettings, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Builds the global configuration from a local .env file"""
        if self._is_configured:
            return

        load_dotenv()
        self.database_url = os.getenv(
            'DATABASE_URL', 
            'postgresql://postgres:postgres@localhost:5432/fastapi_db'
        )
        self.jwt_secret = os.getenv(
            'JWT_SECRET',
            '
        )
        self.jwt_algorithm = os.getenv(
            'JWT_ALGORITHM',
            'HS256'
        )
        self.access_token_ttl_minutes int(os.getenv(
            'ACCESS_TOKEN_TTL_MINUTES',
            '30'
        ))

        self._is_configured = True
    
    class Config:
        env_file = ".env"

