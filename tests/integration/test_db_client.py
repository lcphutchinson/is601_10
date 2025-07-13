"""This module provides a test suite for the DatabaseClient class"""
import pytest

from app.database_client import DatabaseClient

def test_singleton(test_db):
    test_client = DatabaseClient()
    assert test_client is test_db

    
