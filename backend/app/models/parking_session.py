from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from enum import Enum
import datetime

from app.database import Base

class ParkingStatus(Enum):
    PARKED = "parked"
    EXITED = "exited"
    PAID = "paid"

class ParkingSession(Base):
    __tablename__ = "parking_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    plate_number = Column(String, index=True, nullable=False)
    entry_time = Column(DateTime, default=datetime.datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)
    amount = Column(Float, nullable=True)
    status = Column(SQLEnum(ParkingStatus), default=ParkingStatus.PARKED)