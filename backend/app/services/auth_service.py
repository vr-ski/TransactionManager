"""
Authentication service.

Handles user login, password verification, and token creation.
This service enforces authentication-related domain rules and delegates
persistence to the UserRepository.
"""

from datetime import datetime, timedelta

from jose import jwt

from app.core.config.settings import settings
from app.core.security import verify_password
from app.repositories.user_repo import UserRepository


class AuthService:
    """Service responsible for user authentication."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, username: str, password: str) -> str:
        """
        Authenticate a user and return a JWT access token.

        Raises
        ------
        ValueError
            If the username does not exist or the password is invalid.
        """
        user = self.user_repo.get_by_username(username)
        if not user:
            raise ValueError("Invalid username or password.")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid username or password.")

        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRE_HOURS)

        payload = {
            "sub": str(user.user_id),
            "exp": expire,
        }

        token = jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

        return token
