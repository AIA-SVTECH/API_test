from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from datetime import datetime


class Transaction(Base):
    __tablename__ = "Transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    payer_id = Column(Integer, nullable=False)
    merchant_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime, default=datetime.now(), nullable=False)
    status = Column(String(50), nullable=False)
    transaction_description = Column(String(255), nullable=True)


class Merchant(Base):
    __tablename__ = "Merchants"

    merchant_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    merchant_type = Column(String(50), nullable=False)


class Payer(Base):
    __tablename__ = "Payers"

    payer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone_number = Column(String(15), nullable=False)
    account_balance = Column(Float, nullable=False)
