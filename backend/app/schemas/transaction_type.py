from pydantic import BaseModel


class TransactionTypePresentation(BaseModel):
    code: str
    display_name: str

    model_config = {"from_attributes": True}


class TransactionTypeResponse(BaseModel):
    transaction_type_id: int
    code: str
    display_name: str

    model_config = {"from_attributes": True}
