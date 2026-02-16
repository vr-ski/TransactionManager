from dataclasses import dataclass


@dataclass(frozen=True)
class StatusPresentation:
    code: str
    display_name: str
    color: str


@dataclass(frozen=True)
class TransactionTypePresentation:
    code: str
    display_name: str


@dataclass(frozen=True)
class StatusOption:
    status_id: int
    code: str
    display_name: str
    color: str


@dataclass(frozen=True)
class TransactionTypeOption:
    type_id: int
    code: str
    display_name: str
