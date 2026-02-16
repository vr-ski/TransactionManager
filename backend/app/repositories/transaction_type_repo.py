from app.db.models import (
    TransactionTypeORM,
    TransactionTypeTranslationORM,
)
from app.domain.models import (
    TransactionType,
    TransactionTypeTranslation,
)
from app.repositories.base import BaseRepository


class TransactionTypeRepository(BaseRepository):
    def _to_domain(self, orm: TransactionTypeORM) -> TransactionType:
        return TransactionType(
            transaction_type_id=orm.transaction_type_id,  # type: ignore[arg-type]
            code=orm.code,  # type: ignore[arg-type]
        )

    def get_by_id(self, type_id: int) -> TransactionType | None:
        orm = (
            self.db.query(TransactionTypeORM)
            .filter(TransactionTypeORM.transaction_type_id == type_id)  # type: ignore[arg-type]
            .first()
        )
        return self._to_domain(orm) if orm else None

    def get_all(self) -> list[TransactionType]:
        rows = self.db.query(TransactionTypeORM).all()
        return [self._to_domain(r) for r in rows]

    def get_translation(
        self, type_id: int, lang: str
    ) -> TransactionTypeTranslation | None:
        orm = (
            self.db.query(TransactionTypeTranslationORM)
            .filter(
                TransactionTypeTranslationORM.transaction_type_id == type_id,
                TransactionTypeTranslationORM.language_code == lang,
            )
            .first()
        )
        if not orm:
            return None

        return TransactionTypeTranslation(
            transaction_type_id=orm.transaction_type_id,  # type: ignore[arg-type]
            language_code=orm.language_code,  # type: ignore[arg-type]
            display_name=orm.display_name,  # type: ignore[arg-type]
        )

    def get_all_translations(self) -> list[TransactionTypeTranslation]:
        rows = self.db.query(TransactionTypeTranslationORM).all()
        return [
            TransactionTypeTranslation(
                transaction_type_id=r.transaction_type_id,  # type: ignore[arg-type]
                language_code=r.language_code,  # type: ignore[arg-type]
                display_name=r.display_name,  # type: ignore[arg-type]
            )
            for r in rows
        ]
