"""
Contractor repository implementation.

Provides access to contractor data, including lookup by user and by ID.
Converts ORM models into domain Contractor entities.
"""

from sqlalchemy.exc import IntegrityError

from app.db.models import ContractorORM
from app.domain.models import Contractor
from app.repositories.base import BaseRepository


class ContractorRepository(BaseRepository):
    """Repository for accessing and manipulating Contractor data."""

    def _to_domain(self, orm: ContractorORM) -> Contractor:
        """
        Convert an ORM contractor instance to a domain Contractor entity.
        """
        return Contractor(
            contractor_id=orm.contractor_id,  # type: ignore[arg-type]
            user_id=orm.user_id,  # type: ignore[arg-type]
            name=orm.name,  # type: ignore[arg-type]
        )

    def get_by_id(self, contractor_id: int) -> Contractor | None:
        """
        Retrieve a single contractor by its ID.

        Returns None if no such contractors exists.
        """
        orm = (
            self.db.query(ContractorORM)
            .filter(ContractorORM.contractor_id == contractor_id)
            .first()
        )
        return self._to_domain(orm) if orm else None

    def get_by_user(self, user_id: int) -> list[Contractor]:
        """
        Retrieve all contractors belonging to a given user.
        """
        rows = (
            self.db.query(ContractorORM).filter(ContractorORM.user_id == user_id).all()
        )
        return [self._to_domain(r) for r in rows]

    def create(self, user_id: int, name: str) -> Contractor:
        try:
            orm = ContractorORM(user_id=user_id, name=name)
            self.db.add(orm)
            self.db.commit()
            self.db.refresh(orm)
        except IntegrityError as e:
            raise ValueError("User does not exist.") from e

        return self._to_domain(orm)
