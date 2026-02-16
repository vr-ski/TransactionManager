from app.domain.models import User
from app.repositories.user_repo import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.user_repo.get_by_id(user_id)
