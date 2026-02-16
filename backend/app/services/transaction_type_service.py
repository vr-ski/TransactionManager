from app.domain.value_objects import TransactionTypeOption
from app.repositories.transaction_type_repo import TransactionTypeRepository


class TransactionTypeService:
    def __init__(self, type_repo: TransactionTypeRepository):
        self.type_repo = type_repo

    def get_all_options(self, lang: str = "en") -> list[TransactionTypeOption]:
        """
        Return all transaction types with id, code, and display name.
        """
        types = self.type_repo.get_all()
        translations = {}
        all_translations = self.type_repo.get_all_translations()
        for t in all_translations:
            if t.language_code == lang:
                translations[t.transaction_type_id] = t.display_name

        result = []
        for typ in types:
            display_name = translations.get(typ.transaction_type_id, typ.code)
            result.append(
                TransactionTypeOption(
                    type_id=typ.transaction_type_id,
                    code=typ.code,
                    display_name=display_name,
                )
            )
        return result
