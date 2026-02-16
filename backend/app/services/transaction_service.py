"""
Transaction service.

Handles creation, retrieval, and presentation of transactions.
Enforces domain invariants such as one-way cashflow (contractor → client)
and ensures that transactions are enriched with contractor and status
information for UI consumption.
"""

from decimal import Decimal

from app.domain.value_objects import (
    StatusOption,
    StatusPresentation,
    TransactionTypeOption,
)
from app.repositories.contractor_repo import ContractorRepository
from app.repositories.status_repo import StatusRepository
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.transaction_type_repo import TransactionTypeRepository


class TransactionService:
    """Service responsible for transaction workflow and presentation."""

    def __init__(
        self,
        tx_repo: TransactionRepository,
        contractor_repo: ContractorRepository,
        status_repo: StatusRepository,
        type_repo: TransactionTypeRepository,
    ):
        self.tx_repo = tx_repo
        self.contractor_repo = contractor_repo
        self.status_repo = status_repo
        self.type_repo = type_repo

    # ---------------------------------------------------------
    # Creation
    # ---------------------------------------------------------
    def create_transaction(
        self,
        user_id: int,
        contractor_from_id: int,
        contractor_to_id: int,
        amount: Decimal,
        status_id: int,
        transaction_type_id: int,
    ):
        """
        Create a new transaction.

        Domain rules:
        - contractor_from_id must belong to the user.
        - contractor_to_id must belong to the user.

        Raises
        ------
        ValueError
            If the user has no primary account or if the contractor account
            equals the client's primary account.
        """

        # Validate sender contractor
        sender = self.contractor_repo.get_by_id(contractor_from_id)
        if not sender or sender.user_id != user_id:
            raise ValueError("Invalid sender contractor for this user.")

        # Validate receiver contractor
        receiver = self.contractor_repo.get_by_id(contractor_to_id)
        if not receiver:
            raise ValueError("Receiver contractor does not exist.")
        if receiver == sender:
            raise ValueError("Receiver and Sender must differ.")
        if receiver.user_id != user_id:
            raise ValueError("Receiver contractor must belong to the same user.")

        # Validate transaction type
        tx_type = self.type_repo.get_by_id(transaction_type_id)
        if not tx_type:
            raise ValueError("Invalid transaction type.")

        # Create transaction
        return self.tx_repo.create(
            user_id=user_id,
            contractor_from_id=contractor_from_id,
            contractor_to_id=contractor_to_id,
            amount=amount,
            status_id=status_id,
            transaction_type_id=transaction_type_id,
        )

    # ---------------------------------------------------------
    # Update transaction
    # ---------------------------------------------------------
    def update_transaction(self, user_id: int, tx_id: int, updates: dict):
        tx = self.tx_repo.get_by_id(tx_id)
        if not tx:
            raise ValueError("Transaction not found.")

        if tx.user_id != user_id:
            raise ValueError("You do not have permission to modify this transaction.")

        # Normalize: remove None values
        updates = {k: v for k, v in updates.items() if v is not None}

        # Validate status
        if "status_id" in updates and not self.status_repo.get_by_id(
            updates["status_id"]
        ):
            raise ValueError("Invalid status.")

        # Apply updates
        return self.tx_repo.update(tx_id, updates)

    # ---------------------------------------------------------
    # Detail view
    # ---------------------------------------------------------
    def get_transaction_detail(
        self,
        tx_id: int,
        lang: str = "en",
    ) -> dict | None:
        tx = self.tx_repo.get_by_id(tx_id)
        if not tx:
            return None

        contractor_from = self.contractor_repo.get_by_id(tx.contractor_from_id)
        contractor_to = self.contractor_repo.get_by_id(tx.contractor_to_id)

        # Status presentation
        status = self.status_repo.get_by_id(tx.status_id)
        translation = self.status_repo.get_translation(tx.status_id, lang)
        color = self.status_repo.get_color(tx.status_id)
        status_option = StatusOption(
            status_id=tx.status_id,
            code=status.code if status else "unknown",
            display_name=translation.display_name if translation else "Unknown",
            color=color.color if color else "gray",
        )

        # Transaction type presentation
        tx_type = self.type_repo.get_by_id(tx.transaction_type_id)
        if not tx_type:
            raise ValueError("Invalid transaction type.")

        tx_type_translation = self.type_repo.get_translation(
            tx.transaction_type_id, lang
        )
        type_option = TransactionTypeOption(
            type_id=tx_type.transaction_type_id,
            code=tx_type.code,
            display_name=tx_type_translation.display_name
            if tx_type_translation
            else tx_type.code,
        )

        return {
            "transaction_id": tx.transaction_id,
            "contractor_from": contractor_from.name if contractor_from else "Unknown",
            "contractor_to": contractor_to.name if contractor_to else "Unknown",
            "amount": tx.amount,
            "transaction_type": {
                "transaction_type_id": type_option.type_id,
                "code": type_option.code,
                "display_name": type_option.display_name,
            },
            "status": {
                "status_id": status_option.status_id,
                "code": status_option.code,
                "display_name": status_option.display_name,
                "color": status_option.color,
            },
            "created_at": tx.created_at,
            "updated_at": tx.updated_at,
        }

    # ---------------------------------------------------------
    # Recent transactions (batch)
    # ---------------------------------------------------------
    def list_recent_transactions(
        self,
        user_id: int,
        limit: int = 50,
        lang: str = "en",
    ) -> list[dict]:
        """
        Retrieve recent transactions in a single batch query and enrich them.

        This is optimized for the dashboard list view and returns:
        - date
        - contractor name
        - amount
        - status label and color
        """

        # Fetch contractors for this user
        contractors = {
            c.contractor_id: c for c in self.contractor_repo.get_by_user(user_id)
        }

        # Fetch status colors
        colors = {c.status_id: c.color for c in self.status_repo.get_all_colors()}

        # Fetch status translations
        translations = {
            (t.status_id, t.language_code): t.display_name
            for t in self.status_repo.get_all_translations()
        }

        # Fetch transaction type translations
        type_translations = {
            (t.transaction_type_id, t.language_code): t.display_name
            for t in self.type_repo.get_all_translations()
        }

        # Fetch recent transactions
        txs = self.tx_repo.get_recent(user_id=user_id, limit=limit)

        result: list[dict] = []
        for tx in txs:
            contractor_from = contractors.get(tx.contractor_from_id)
            contractor_to = self.contractor_repo.get_by_id(tx.contractor_to_id)

            status = self.status_repo.get_by_id(tx.status_id)
            status_label = translations.get((tx.status_id, lang), "Unknown")
            status_color = colors.get(tx.status_id, "gray")

            tx_type_label = type_translations.get(
                (tx.transaction_type_id, lang),
                "Unknown",
            )

            result.append(
                {
                    "transaction_id": tx.transaction_id,
                    "contractor_from": contractor_from.name
                    if contractor_from
                    else "Unknown",
                    "contractor_to": contractor_to.name if contractor_to else "Unknown",
                    "amount": tx.amount,
                    "transaction_type": tx_type_label,
                    "status": StatusPresentation(
                        code=status.code if status else "unknown",
                        display_name=status_label,
                        color=status_color,
                    ),
                    "created_at": tx.created_at,
                }
            )

        return result
