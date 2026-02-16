from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# -------------------------
# Users
# -------------------------
class UserORM(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)

    contractors = relationship("ContractorORM", back_populates="user")
    transactions = relationship("TransactionORM", back_populates="user")


# -------------------------
# Languages
# -------------------------
class LanguageORM(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "languages"

    language_code = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)

    status_translations = relationship(
        "TransactionStatusTranslationORM", back_populates="language"
    )
    type_translations = relationship(
        "TransactionTypeTranslationORM", back_populates="language"
    )


# -------------------------
# Contractors
# -------------------------
class ContractorORM(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "contractors"

    contractor_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    name = Column(Text, nullable=False)

    user = relationship("UserORM", back_populates="contractors")


# -------------------------
# Transaction Statuses
# -------------------------
class TransactionStatusORM(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "transaction_statuses"

    status_id = Column(Integer, primary_key=True)
    code = Column(Text, unique=True, nullable=False)

    color = relationship(
        "TransactionStatusColorORM", uselist=False, back_populates="status"
    )

    translations = relationship(
        "TransactionStatusTranslationORM", back_populates="status"
    )


class TransactionStatusColorORM(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "transaction_status_colors"

    status_id = Column(
        Integer, ForeignKey("transaction_statuses.status_id"), primary_key=True
    )
    color = Column(Text, nullable=False)

    status = relationship("TransactionStatusORM", back_populates="color")


class TransactionStatusTranslationORM(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "transaction_status_translations"

    status_id = Column(
        Integer, ForeignKey("transaction_statuses.status_id"), primary_key=True
    )
    language_code = Column(
        Text, ForeignKey("languages.language_code"), primary_key=True
    )
    display_name = Column(Text, nullable=False)

    status = relationship("TransactionStatusORM", back_populates="translations")
    language = relationship("LanguageORM", back_populates="status_translations")


# -------------------------
# Transactions
# -------------------------
class TransactionORM(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    contractor_from_id = Column(
        Integer, ForeignKey("contractors.contractor_id"), nullable=False
    )
    contractor_to_id = Column(
        Integer, ForeignKey("contractors.contractor_id"), nullable=False
    )
    amount = Column(Numeric(12, 2), nullable=False)
    transaction_type_id = Column(
        Integer, ForeignKey("transaction_types.transaction_type_id"), nullable=False
    )
    status_id = Column(
        Integer, ForeignKey("transaction_statuses.status_id"), nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user = relationship("UserORM", back_populates="transactions")
    contractor_from = relationship("ContractorORM", foreign_keys=[contractor_from_id])
    contractor_to = relationship("ContractorORM", foreign_keys=[contractor_to_id])
    status = relationship("TransactionStatusORM")
    transaction_type = relationship("TransactionTypeORM")


# -------------------------
# Transaction Types
# -------------------------
class TransactionTypeORM(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "transaction_types"

    transaction_type_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Text, unique=True, nullable=False)

    translations = relationship("TransactionTypeTranslationORM", back_populates="type")


# -------------------------
# TransactionsType Translations
# -------------------------
class TransactionTypeTranslationORM(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "transaction_type_translations"

    transaction_type_id = Column(
        Integer, ForeignKey("transaction_types.transaction_type_id"), primary_key=True
    )
    language_code = Column(
        Text, ForeignKey("languages.language_code"), primary_key=True
    )
    display_name = Column(Text, nullable=False)

    type = relationship("TransactionTypeORM", back_populates="translations")
    language = relationship("LanguageORM", back_populates="type_translations")
