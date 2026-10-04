from sqlalchemy import Column, Integer, String
from app.database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

