"""
Module for authentication and authorization services.
Provides password hashing, JWT token generation, and user authentication.
"""

import pickle
from datetime import datetime, timedelta, UTC
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.database.db import get_db
from src.conf.config import settings
from src.database.models import User, UserRole
from src.services.users import UserService

import redis


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def create_access_token(data: dict, expires_delta: Optional[int] = None):
    """
    Generate a JWT access token.

    Args:
        data (dict): The payload to encode into the token.
        expires_delta (Optional[int], optional): Expiration time in seconds. Defaults to None.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(UTC) + timedelta(seconds=settings.JWT_EXPIRATION_SECONDS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    """
    Retrieve the currently authenticated user from the JWT token.

    Args:
        token (str): The JWT token extracted from the request.
        db (AsyncSession): The database session.

    Returns:
        User: The authenticated user instance.

    Raises:
        HTTPException: If authentication fails.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        username = payload["sub"]
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_service = UserService(db)
    r = redis.from_url(settings.REDIS_URL)
    user = r.get(username)
    if user is None:
        user = await user_service.get_user_by_username(username)
        if user is not None:
            r.set(username, pickle.dumps(user))
            r.expire(username, 3600)
            print("---> Getting User from DB")
            return user

    if user is None:
        raise credentials_exception
    print("---> Getting User from REDIS")
    return pickle.loads(user)


def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """Gets the current authenticated admin user.

    Args:
        current_user (User): The currently authenticated user.

    Returns:
        User: The authenticated admin user.

    Raises:
        HTTPException: If the user does not have admin privileges.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Insufficient access rights")
    return current_user


async def get_email_from_token(token: str):
    """
    Extract the email from a JWT token.

    Args:
        token (str): The JWT token.

    Returns:
        str: The extracted email.

    Raises:
        HTTPException: If the token is invalid.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload["sub"]
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Token incorrect",
        )


def create_email_token(data: dict):
    """
    Generate a JWT token for email verification.

    Args:
        data (dict): The payload to encode into the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=7)
    to_encode.update({"iat": datetime.now(UTC), "exp": expire})
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token
