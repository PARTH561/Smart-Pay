from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    mobile = Column(String)
    wallet_balance = Column(Float, default=0.0)
    kyc_status = Column(String, default="Pending")
    risk_score = Column(Integer, default=0)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    amount = Column(Float)
    txn_type = Column(String)
    country = Column(String, default="India")   # NEW
    fraud_flag = Column(Integer, default=0)
    risk_score = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
