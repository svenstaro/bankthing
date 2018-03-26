from decimal import Decimal

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils.models import Timestamp
from sqlalchemy.ext.declarative.api import declarative_base

Base = declarative_base()


class Account(Base, Timestamp):
    """A bank account."""

    __tablename__ = 'accounts'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    iban = Column(String(34), nullable=False, unique=True, index=True)
    bic = Column(String(11), nullable=False, index=True)

    def __init__(self, iban: str, bic: str):
        self.iban = iban
        self.bic = bic

    def __repr__(self):
        return f"<Account {self.id} with IBAN {self.iban}>"


class Balance(Base, Timestamp):
    """An immutable account balance at a certain point in time.

    Account balances may not be updated once they are created.
    """

    __tablename__ = 'balances'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    balance = Column(Numeric(), nullable=False, index=True)
    currency = Column(String(3), nullable=False, index=True)

    account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id'), nullable=False, index=True)
    account = relationship('Account', backref=backref('balances', cascade='all, delete-orphan'))

    def __init__(self, balance: str, currency: str, account: Account):
        self.balance = Decimal(balance)
        self.currency = currency
        self.account = account

    def __repr__(self):
        return f"<Balance {self.id} at {self.created_at} ({self.balance} {self.currency})"


class Transaction(Base, Timestamp):
    """A single transaction."""

    __tablename__ = 'transactions'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())

    account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id'), nullable=False, index=True)
    account = relationship('Account', backref=backref('transctions', cascade='all, delete-orphan'))

    def __init__(self, iban, bic):
        self.iban = iban
        self.bic = bic

    def __repr__(self):
        return f"{self.iban} {self.bic}"
