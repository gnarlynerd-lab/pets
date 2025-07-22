"""Pydantic schemas for authentication."""

from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for user creation."""
    username: str
    email: EmailStr
    password: str
    user_preferences: Optional[Dict[str, Any]] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response (excludes sensitive data)."""
    user_id: str
    username: str
    email: str
    user_preferences: Optional[Dict[str, Any]] = None
    token_balance: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token data."""
    username: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for user updates."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    user_preferences: Optional[Dict[str, Any]] = None


class PasswordChange(BaseModel):
    """Schema for password change."""
    current_password: str
    new_password: str