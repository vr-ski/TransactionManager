from pydantic import BaseModel


class ContractorCreate(BaseModel):
    name: str


class ContractorResponse(BaseModel):
    contractor_id: int
    user_id: int
    name: str

    model_config = {"from_attributes": True}
