from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.services.transaction_service import TransactionService


def test_create_transaction_success():
    tx_repo = MagicMock()
    contractor_repo = MagicMock()
    status_repo = MagicMock()
    type_repo = MagicMock()

    # Sender contractor belongs to user
    contractor_repo.get_by_id.side_effect = [
        MagicMock(user_id=1),  # sender
        MagicMock(user_id=1),  # receiver
    ]

    status_repo.get_by_id.return_value = MagicMock()
    type_repo.get_by_id.return_value = MagicMock()

    service = TransactionService(tx_repo, contractor_repo, status_repo, type_repo)

    service.create_transaction(
        user_id=1,
        contractor_from_id=10,
        contractor_to_id=20,
        amount=Decimal("50.00"),
        status_id=1,
        transaction_type_id=1,
    )

    tx_repo.create.assert_called_once()


def test_create_transaction_invalid_sender():
    tx_repo = MagicMock()
    contractor_repo = MagicMock()
    status_repo = MagicMock()
    type_repo = MagicMock()

    # Sender does NOT belong to user
    contractor_repo.get_by_id.side_effect = [
        MagicMock(user_id=999),  # sender
    ]

    service = TransactionService(tx_repo, contractor_repo, status_repo, type_repo)

    with pytest.raises(ValueError):
        service.create_transaction(1, 10, 20, Decimal("10"), 1, 1)


def test_create_transaction_receiver_diff_user():
    tx_repo = MagicMock()
    contractor_repo = MagicMock()
    status_repo = MagicMock()
    type_repo = MagicMock()

    contractor_repo.get_by_id.side_effect = [
        MagicMock(user_id=1),  # sender
        MagicMock(user_id=2),  # receiver (invalid)
    ]

    service = TransactionService(tx_repo, contractor_repo, status_repo, type_repo)

    with pytest.raises(ValueError):
        service.create_transaction(1, 10, 20, Decimal("10"), 1, 1)
