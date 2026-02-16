from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.repositories.contractor_repo import ContractorRepository
from app.repositories.status_repo import StatusRepository
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.transaction_type_repo import TransactionTypeRepository
from app.schemas.transaction import (
    TransactionCreateRequest,
    TransactionDetailResponse,
    TransactionListItem,
    TransactionListResponse,
    TransactionUpdateRequest,
)
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


# -----------------------------
# Dependency: TransactionService
# -----------------------------
def get_transaction_service(db: Session = Depends(get_db)) -> TransactionService:  # noqa: B008
    return TransactionService(
        tx_repo=TransactionRepository(db),
        contractor_repo=ContractorRepository(db),
        status_repo=StatusRepository(db),
        type_repo=TransactionTypeRepository(db),
    )


# -----------------------------
# Create transaction
# -----------------------------
@router.post("/create", response_model=TransactionDetailResponse)
def create_transaction(
    request: TransactionCreateRequest,
    service: TransactionService = Depends(get_transaction_service),  # noqa: B008
    user_id: int = Depends(get_current_user),
):
    try:
        tx = service.create_transaction(
            user_id=user_id,
            contractor_from_id=request.contractor_from_id,
            contractor_to_id=request.contractor_to_id,
            amount=request.amount,
            status_id=request.status_id,
            transaction_type_id=request.transaction_type_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    detail = service.get_transaction_detail(tx.transaction_id)
    return TransactionDetailResponse(**detail)  # type: ignore[arg-type]


# -----------------------------
# Update transaction
# -----------------------------
@router.patch("/{tx_id}", response_model=TransactionDetailResponse)
def update_transaction(
    tx_id: int,
    updates: TransactionUpdateRequest,
    service: TransactionService = Depends(get_transaction_service),  # noqa: B008
    user_id: int = Depends(get_current_user),
):
    try:
        # Convert Pydantic → dict (exclude_unset ensures partial updates)
        updates_dict = updates.dict(exclude_unset=True)

        service.update_transaction(
            user_id=user_id,
            tx_id=tx_id,
            updates=updates_dict,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    detail = service.get_transaction_detail(tx_id)
    return TransactionDetailResponse(**detail)  # type: ignore[arg-type]


# -----------------------------
# List recent transactions
# -----------------------------
@router.get("/recent", response_model=TransactionListResponse)
def list_recent_transactions(
    limit: int = 50,
    user_id: int = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),  # noqa: B008
):
    items = service.list_recent_transactions(user_id=user_id, limit=limit)
    return TransactionListResponse(items=[TransactionListItem(**i) for i in items])


# -----------------------------
# Get transaction detail
# -----------------------------
@router.get("/{tx_id}", response_model=TransactionDetailResponse)
def get_transaction_detail(
    tx_id: int,
    service: TransactionService = Depends(get_transaction_service),  # noqa: B008
):
    detail = service.get_transaction_detail(tx_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionDetailResponse(**detail)
