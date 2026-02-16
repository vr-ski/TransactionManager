"""
Transaction status repository.

Provides access to status metadata including code, color, and translations.
Converts ORM models into domain status-related entities.
"""

from app.db.models import (
    TransactionStatusColorORM,
    TransactionStatusORM,
    TransactionStatusTranslationORM,
)
from app.domain.models import (
    TransactionStatus,
    TransactionStatusColor,
    TransactionStatusTranslation,
)
from app.repositories.base import BaseRepository


class StatusRepository(BaseRepository):
    """Repository for accessing transaction status metadata."""

    def _to_domain(self, orm: TransactionStatusORM) -> TransactionStatus:
        """
        Convert an ORM status instance to a domain TransactionStatus entity.
        """
        return TransactionStatus(status_id=orm.status_id, code=orm.code)  # type: ignore[arg-type]

    def get_all(self) -> list[TransactionStatus]:
        """
        Retrieve all status definitions.
        """
        rows = self.db.query(TransactionStatusORM).all()
        return [self._to_domain(r) for r in rows]

    def get_by_id(self, status_id: int) -> TransactionStatus | None:
        """
        Retrieve a single status definition by ID.

        Returns None if no such status exists.
        """
        orm = (
            self.db.query(TransactionStatusORM)
            .filter(TransactionStatusORM.status_id == status_id)
            .first()
        )
        return self._to_domain(orm) if orm else None

    def get_color(self, status_id: int) -> TransactionStatusColor | None:
        """
        Retrieve the color associated with a given status ID.

        Returns None if no color is defined.
        """
        orm = (
            self.db.query(TransactionStatusColorORM)
            .filter(TransactionStatusColorORM.status_id == status_id)
            .first()
        )
        if not orm:
            return None
        return TransactionStatusColor(status_id=orm.status_id, color=orm.color)  # type: ignore[arg-type]

    def get_translation(
        self, status_id: int, lang: str
    ) -> TransactionStatusTranslation | None:
        """
        Retrieve the localized label for a status in a given language.

        Returns None if no translation is defined.
        """
        orm = (
            self.db.query(TransactionStatusTranslationORM)
            .filter(
                TransactionStatusTranslationORM.status_id == status_id,
                TransactionStatusTranslationORM.language_code == lang,
            )
            .first()
        )
        if not orm:
            return None
        return TransactionStatusTranslation(
            status_id=orm.status_id,  # type: ignore[arg-type]
            language_code=orm.language_code,  # type: ignore[arg-type]
            display_name=orm.display_name,  # type: ignore[arg-type]
        )

    def get_all_colors(self) -> list[TransactionStatusColor]:
        """
        Retrieve all status colors.
        """
        rows = self.db.query(TransactionStatusColorORM).all()
        return [
            TransactionStatusColor(status_id=r.status_id, color=r.color)  # type: ignore[arg-type]
            for r in rows
        ]

    def get_all_translations(self) -> list[TransactionStatusTranslation]:
        """
        Retrieve all status translations.
        """
        rows = self.db.query(TransactionStatusTranslationORM).all()
        return [
            TransactionStatusTranslation(
                status_id=r.status_id,  # type: ignore[arg-type]
                language_code=r.language_code,  # type: ignore[arg-type]
                display_name=r.display_name,  # type: ignore[arg-type]
            )
            for r in rows
        ]
