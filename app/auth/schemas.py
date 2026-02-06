"""
Pydantic schemas for authentication.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Schema for token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data."""
    email: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema for login request."""
    username: EmailStr  # FastAPI OAuth2PasswordRequestForm uses 'username' field
    password: str


class RegisterRequest(BaseModel):
    """Schema for registration request."""
    email: EmailStr
    password: str
