from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.status import StatusPresentation, StatusResponse
from app.schemas.transaction_type import TransactionTypeResponse


class TransactionCreateRequest(BaseModel):
    contractor_from_id: int
    contractor_to_id: int
    amount: Decimal
    status_id: int
    transaction_type_id: int


class TransactionDetailResponse(BaseModel):
    transaction_id: int
    contractor_from: str
    contractor_to: str
    amount: Decimal
    transaction_type: TransactionTypeResponse
    status: StatusResponse
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TransactionListItem(BaseModel):
    transaction_id: int
    contractor_from: str
    contractor_to: str
    amount: Decimal
    transaction_type: str
    status: StatusPresentation
    created_at: datetime

    model_config = {"from_attributes": True}


class TransactionListResponse(BaseModel):
    items: list[TransactionListItem]


class TransactionUpdateRequest(BaseModel):
    status_id: int | None = None
    # Add more fields later as needed
