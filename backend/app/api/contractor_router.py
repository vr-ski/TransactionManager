from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.repositories.contractor_repo import ContractorRepository
from app.repositories.user_repo import UserRepository
from app.schemas.contractor import ContractorCreate, ContractorResponse
from app.services.contractor_service import ContractorService

router = APIRouter(prefix="/contractors", tags=["contractors"])


# Instantiate service + repo once; DB is per-request via context var
def get_contractor_service(db: Session = Depends(get_db)) -> ContractorService:  # noqa: B008
    return ContractorService(ContractorRepository(db))


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:  # noqa: B008
    return UserRepository(db)


@router.get(
    "/user/{user_id}",
    response_model=list[ContractorResponse],
)
def list_contractors_for_user(
    user_id: int = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repo),  # noqa: B008
    service: ContractorService = Depends(get_contractor_service),  # noqa: B008
):
    if not user_repo.exists(user_id):
        raise HTTPException(status_code=404, detail="User not found.")

    contractors = service.list_for_user(user_id)
    return contractors


@router.get(
    "/{contractor_id}",
    response_model=ContractorResponse,
)
def get_contractor(
    contractor_id: int,
    service: ContractorService = Depends(get_contractor_service),  # noqa: B008
):
    contractor = service.get(contractor_id)
    if not contractor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contractor not found",
        )
    return contractor


@router.post(
    "/user/{user_id}",
    response_model=ContractorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contractor(
    contractor_data: ContractorCreate,
    user_id: int = Depends(get_current_user),
    service: ContractorService = Depends(get_contractor_service),  # noqa: B008
):
    contractor = service.create(user_id=user_id, name=contractor_data.name)
    return contractor
