from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


# -------------------------
# Users
# -------------------------
@dataclass
class User:
    user_id: int
    username: str
    password_hash: str


# -------------------------
# Languages
# -------------------------
@dataclass
class Language:
    language_code: str
    name: str


# -------------------------
# Contractors
# -------------------------
@dataclass
class Contractor:
    contractor_id: int
    user_id: int
    name: str


# -------------------------
# Transaction Status System
# -------------------------
@dataclass
class TransactionStatus:
    status_id: int
    code: str


@dataclass
class TransactionStatusColor:
    status_id: int
    color: str


@dataclass
class TransactionStatusTranslation:
    status_id: int
    language_code: str
    display_name: str


# -------------------------
# Transaction Types
# -------------------------
@dataclass
class TransactionType:
    transaction_type_id: int
    code: str


@dataclass
class TransactionTypeTranslation:
    transaction_type_id: int
    language_code: str
    display_name: str


# -------------------------
# Transactions
# -------------------------
@dataclass
class Transaction:
    transaction_id: int
    user_id: int
    contractor_from_id: int
    contractor_to_id: int
    amount: Decimal
    transaction_type_id: int
    status_id: int
    created_at: datetime
    updated_at: datetime

    # Enriched fields (resolved by service layer)
    transaction_type_code: str | None = None
    transaction_type_display_name: str | None = None

    status_code: str | None = None
    status_display_name: str | None = None
    status_color: str | None = None
