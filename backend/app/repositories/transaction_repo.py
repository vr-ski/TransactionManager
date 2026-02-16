"""
Transaction repository implementation.

Handles retrieval and creation of transactions, including batch queries
for recent transactions. Converts ORM models into domain Transaction
entities.
"""

from decimal import Decimal

from sqlalchemy import desc

from app.db.models import TransactionORM
from app.domain.models import Transaction
from app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository):
    """Repository for accessing and manipulating Transaction data."""

    def _to_domain(self, orm: TransactionORM) -> Transaction:
        """
        Convert an ORM transaction instance to a domain Transaction entity.
        """
        return Transaction(
            transaction_id=orm.transaction_id,  # type: ignore[arg-type]
            user_id=orm.user_id,  # type: ignore[arg-type]
            contractor_from_id=orm.contractor_from_id,  # type: ignore[arg-type]
            contractor_to_id=orm.contractor_to_id,  # type: ignore[arg-type]
            amount=orm.amount,  # type: ignore[arg-type]
            transaction_type_id=orm.transaction_type_id,  # type: ignore[arg-type]
            status_id=orm.status_id,  # type: ignore[arg-type]
            created_at=orm.created_at,  # type: ignore[arg-type]
            updated_at=orm.updated_at,  # type: ignore[arg-type]
        )

    def get_by_id(self, transaction_id: int) -> Transaction | None:
        """
        Retrieve a single transaction by its ID.

        Returns None if no such transaction exists.
        """
        orm = (
            self.db.query(TransactionORM)
            .filter(TransactionORM.transaction_id == transaction_id)
            .first()
        )
        return self._to_domain(orm) if orm else None

    def get_for_contractors(self, contractor_ids: list[int]) -> list[Transaction]:
        """
        Retrieve all transactions where any of the given contractor is either
        the sender or the receiver.
        """
        rows = (
            self.db.query(TransactionORM)
            .filter(
                (TransactionORM.contractor_from_id.in_(contractor_ids))
                | (TransactionORM.contractor_to_id.in_(contractor_ids))
            )
            .order_by(desc(TransactionORM.created_at))
            .all()
        )
        return [self._to_domain(r) for r in rows]

    def get_recent(self, user_id: int, limit: int) -> list[Transaction]:
        """
        Retrieve the most recent transactions, ordered by creation date
        descending, limited by the given count.
        """
        rows = (
            self.db.query(TransactionORM)
            .filter(TransactionORM.user_id == user_id)
            .order_by(desc(TransactionORM.created_at))
            .limit(limit)
            .all()
        )
        return [self._to_domain(r) for r in rows]

    def create(
        self,
        user_id: int,
        contractor_from_id: int,
        contractor_to_id: int,
        amount: Decimal,
        status_id: int,
        transaction_type_id: int,
    ) -> Transaction:
        """
        Create and persist a new transaction.

        Returns the created domain Transaction entity.
        """
        orm = TransactionORM(
            user_id=user_id,
            contractor_from_id=contractor_from_id,
            contractor_to_id=contractor_to_id,
            amount=amount,
            status_id=status_id,
            transaction_type_id=transaction_type_id,
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return self._to_domain(orm)

    def update(self, tx_id: int, updates: dict):
        """
        Update transaction.

        Returns the updated domain Transaction entity.
        """
        orm = (
            self.db.query(TransactionORM)
            .filter(TransactionORM.transaction_id == tx_id)
            .first()
        )

        if not orm:
            return None

        # Apply updates selectively
        if "status_id" in updates:
            orm.status_id = updates["status_id"]

        self.db.commit()
        self.db.refresh(orm)
        return self._to_domain(orm)
