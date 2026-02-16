from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.transaction_type_repo import TransactionTypeRepository
from app.schemas.transaction_type import TransactionTypeResponse
from app.services.transaction_type_service import TransactionTypeService

router = APIRouter(prefix="/transaction-types", tags=["transaction-types"])


def get_transaction_type_service(
    db: Session = Depends(get_db),  # noqa: B008
) -> TransactionTypeService:
    return TransactionTypeService(TransactionTypeRepository(db))


@router.get("/", response_model=list[TransactionTypeResponse])
def get_transaction_types(
    service: TransactionTypeService = Depends(get_transaction_type_service),  # noqa: B008
    lang: str = "en",
):
    options = service.get_all_options(lang)
    return [
        TransactionTypeResponse(
            transaction_type_id=opt.type_id,
            code=opt.code,
            display_name=opt.display_name,
        )
        for opt in options
    ]
