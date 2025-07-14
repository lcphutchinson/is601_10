"""This module provides a data model for user-related input forms and user record creation"""
import pydantic as pyd

from typing import Optional
from uuid import UUID
from datetime import datetime

class UserForm(pyd.BaseModel):
    """User creation form schema with common fields."""
    first_name: str     = pyd.Field(max_length=50, example="Jane")
    last_name: str      = pyd.Field(max_length=50, example="Doe")
    email: pyd.EmailStr = pyd.Field(example="jane.doe@example.com")
    username: str       = pyd.Field(min_length=3, max_length=50, example="janedoe")

    model_config = pyd.ConfigDict(from_attributes=True)

class PasswordMixin(pyd.BaseModel):
    """Mixin for password validation"""
    password: str       = pyd.Field(min_length=6, max_length=128, example="SecurePass123")

    @pyd.model_validator(mode="before")
    @classmethod
    def validate_password(cls, values: dict) -> dict:
        password = values.get("password")
        if not password:
            raise ValueError("Password is required")
        if len(password) < 6:
            raise ValueError("Password must contain at least 6 characters")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        return values

class UserLoginForm(PasswordMixin):
    """User Login form schema with username/password"""
    username: str = pyd.Field(
        description="Username or email",
        min_length=3,
        max_length=50,
        example="janedoe123"
    )

class UserCreate(UserForm, PasswordMixin):
    """Formatted schema for User Create actions"""
pass
   

