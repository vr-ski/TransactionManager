from pydantic import BaseModel


class StatusPresentation(BaseModel):
    code: str
    display_name: str
    color: str

    model_config = {"from_attributes": True}


class StatusResponse(BaseModel):
    status_id: int
    code: str
    display_name: str
    color: str

    model_config = {"from_attributes": True}
