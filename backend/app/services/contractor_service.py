"""
Contractor service.

Provides higher-level operations for managing contractors.
"""

from app.domain.models import Contractor
from app.repositories.contractor_repo import ContractorRepository


class ContractorService:
    """Service for retrieving and managing contractor information."""

    def __init__(self, contractor_repo: ContractorRepository):
        self.contractor_repo = contractor_repo

    def list_for_user(self, user_id: int) -> list[Contractor]:
        """
        Return all contractors belonging to a specific user.
        """
        return self.contractor_repo.get_by_user(user_id)

    def get(self, contractor_id: int) -> Contractor | None:
        """
        Retrieve a single contractor by ID.
        """
        return self.contractor_repo.get_by_id(contractor_id)

    def create(self, user_id: int, name: str) -> Contractor:
        """
        Create a new contractor for the user.
        """
        return self.contractor_repo.create(user_id, name)
