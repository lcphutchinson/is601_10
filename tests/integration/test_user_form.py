"""This module provides a test suite for the User Forms schema set at app.schemas.user_form"""
import pytest

from pydantic import ValidationError
from unittest.mock import patch

import app.schemas.user_form as forms

def test_user_form_properties():
    """Validates UserForm object properties and constructor"""
    data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "username": "janedoe",
    }
    user_form = forms.UserForm(**data)
    assert isinstance(user_form, forms.UserForm)
    assert user_form.first_name == "Jane"
    assert user_form.last_name == "Doe"
    assert user_form.email == "jane.doe@example.com"
    assert user_form.username == "janedoe"

def test_email_constraint():
    """Tests format enforcement on the email field, provided by pydantic.EmailStr"""
    data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "invalid",
        "username": "janedoe",
    }
    with pytest.raises(ValidationError):
        forms.UserForm(**data)

def test_password_mixin_properties():
    """Validates PasswordMixin object properties and contructor"""
    data = {"password": "SecurePass123"}
    password_mixin = forms.PasswordMixin(**data)
    assert isinstance(password_mixin, forms.PasswordMixin)
    assert password_mixin.password == "SecurePass123"

@pytest.mark.parametrize(
    "data, expected",
    [
        ({}, "Password is required"),
        ({"password": "short"}, "Password must contain at least 6 characters"),
        ({"password": "securepass123"}, "Password must contain at least one uppercase letter"),
        ({"password": "SECUREPASS123"}, "Password must contain at least one lowercase letter"),
        ({"password": "SecurePass"}, "Password must contain at least one digit")
    ],
    ids=[
        "empty_pass",
        "short_pass",
        "lower_pass",
        "upper_pass",
        "alpha_pass",
    ]
)
def test_password_constraints(data: dict[str, str], expected: str):
    """Tests format enforcement on the password field"""
    with pytest.raises(ValueError, match=expected):
        forms.PasswordMixin(**data)

def test_user_create_properties():
    """Validates the UserCreate schema's properties and constructor"""
    data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "username": "janedoe",
        "password": "SecurePass123",
    }
    user_create = forms.UserCreate(**data)
    assert isinstance(user_create, forms.UserCreate)
    assert user_create.first_name == "Jane"
    assert user_create.last_name == "Doe"
    assert user_create.email == "jane.doe@example.com"
    assert user_create.username == "janedoe"
    assert user_create.password == "SecurePass123"

def test_user_login_form_properties():
    """Validates the UserLoginForm schema's properties and constructor"""
    data = { "username": "janedoe", "password": "SecurePass123" }
    login_form = forms.UserLoginForm(**data)
    assert isinstance(login_form, forms.UserLoginForm)
    assert login_form.username == "janedoe"
    assert login_form.password == "SecurePass123"

@pytest.mark.parametrize(
        "username",
        [
            ("lo"),
            ("loremipsumdolorsitametconsecteturadipiscingelitsedd"),
        ],
        ids=[
            "short_username",
            "long_username",
        ]
)
def test_login_username_constraints(username: str):
    """Tests length constrains on the login username field"""
    data = { "username": username, "password": "SecurePass123" }
    with pytest.raises(ValidationError):
        forms.UserLoginForm(**data)

