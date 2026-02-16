from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.status_repo import StatusRepository
from app.schemas.status import StatusResponse
from app.services.status_service import StatusService

router = APIRouter(prefix="/statuses", tags=["statuses"])


def get_status_service(db: Session = Depends(get_db)) -> StatusService:  # noqa: B008
    return StatusService(StatusRepository(db))


@router.get("/", response_model=list[StatusResponse])
def get_statuses(
    service: StatusService = Depends(get_status_service),  # noqa: B008
    lang: str = "en",
):
    options = service.get_all_options(lang)
    return [
        StatusResponse(
            status_id=opt.status_id,
            code=opt.code,
            display_name=opt.display_name,
            color=opt.color,
        )
        for opt in options
    ]
