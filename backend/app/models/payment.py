from sqlalchemy import Column, Integer, DateTime, String, Float, Enum as SQLEnum, ForeignKey
from enum import Enum
from app.database import Base
import datetime 

class PaymentMethod(Enum):
    UPI = "UPI",
    CASH = "Cash"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    session_id = Column(Integer, ForeignKey("parking_sessions.id"), nullable=False)
    amount = Column(Float, nullable = False)
    method = Column(SQLEnum(PaymentMethod), nullable = False)
    paid_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="pending")