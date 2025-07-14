"""This module provides a data model for the user-related output records, including Auth tokens"""
import pydantic as pyd

from datetime import datetime
from typing import Optional
from uuid import UUID

class UserRecord(pyd.BaseModel):
    """User record schema for Read operations"""
    id: UUID
    username: str
    email: pyd.EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = pyd.ConfigDict(from_attributes=True)

class AuthToken(pyd.BaseModel):
    """Auth Token schema for cookie passing"""
    access_token: str
    token_type: str = "bearer"
    user: UserRecord

    model_config = pyd.ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "janedoe",
                    "email": "jane.doe@example.com",
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "is_active": True,
                    "is_verified": False,
                    "created_at": "2025-07-01T00:00:00",
                    "updated_at": "2025-07-08T00:00:00",
                },
            }
        }
    )

class AuthData(pyd.BaseModel):
    """Data Schema for JWT encoded tokens"""
    user_id: Optional[UUID] = None

class UserLoginFormat(pyd.BaseModel):
    """Login sample schema for populating login fields"""
    username: str
    password: str

    model_config = pyd.ConfigDict(
        json_schema_extra={
            "example": {
                "username": "janedoe123",
                "password": "SecurePass123",
            }
        }
    )
