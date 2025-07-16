"""This module provides an importable global oauth2 scheme setting"""
from fastapi.security import OAuth2PasswordBearer

oath2_scheme = OAuth2PasswordBearer(tokenURL="token")
