from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:  # noqa: B008
    return AuthService(UserRepository(db))


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    service: AuthService = Depends(get_auth_service),  # noqa: B008
):
    try:
        token = service.authenticate(username, password)
    except ValueError as e:
        raise HTTPException(
            status_code=401, detail="Invalid username or password"
        ) from e

    return {
        "access_token": token,
        "token_type": "bearer",
    }
