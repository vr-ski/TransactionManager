"""
Base repository interfaces for the DDD architecture.

These abstract classes define the contract that all concrete repository
implementations must follow. They ensure that the domain layer remains
decoupled from persistence concerns.
"""

from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session


class BaseRepository(ABC):
    """Abstract base class for all repositories."""

    def __init__(self, db: Session):
        self.db = db

    @abstractmethod
    def _to_domain(self, orm_obj: Any) -> Any:
        """
        Convert an ORM model instance into a domain model instance.

        Parameters
        ----------
        orm_obj : SQLAlchemy ORM model
            The persistence model to convert.

        Returns
        -------
        Domain model instance
        """
        raise NotImplementedError
