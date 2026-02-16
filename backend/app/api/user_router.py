from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/me", tags=["me"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:  # noqa: B008
    return UserService(UserRepository(db))


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    user_id: int = Depends(get_current_user),
    service: UserService = Depends(get_user_service),  # noqa: B008
):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(user_id=user.user_id, username=user.username)
