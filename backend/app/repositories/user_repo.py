"""
User repository implementation.

Handles persistence operations related to users, including lookup by ID
and username. Converts ORM models into domain User entities.
"""

from app.db.models import UserORM
from app.domain.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """Repository for accessing and manipulating User data."""

    def _to_domain(self, orm: UserORM) -> User:
        """Convert ORM user to domain user."""
        return User(
            user_id=orm.user_id,  # type: ignore[arg-type]
            username=orm.username,  # type: ignore[arg-type]
            password_hash=orm.password_hash,  # type: ignore[arg-type]
        )

    def exists(self, user_id: int) -> bool:
        return (
            self.db.query(UserORM).filter(UserORM.user_id == user_id).first()
            is not None
        )

    def get_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by ID.

        Returns None if the user does not exist.
        """
        orm = self.db.query(UserORM).filter(UserORM.user_id == user_id).first()
        return self._to_domain(orm) if orm else None

    def get_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by username.

        Returns None if the user does not exist.
        """
        orm = self.db.query(UserORM).filter(UserORM.username == username).first()
        return self._to_domain(orm) if orm else None

    def add(self, user: UserORM):
        """
        Add a user to the DB.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
