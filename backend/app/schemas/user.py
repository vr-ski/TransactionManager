from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: int
    username: str

    model_config = {"from_attributes": True}
