from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from database import Base

#importing Base class (database.py)
class Temptest(Base):
    __tablename__ = "temptest"
    id = Column(Integer, primary_key=True, index=True)
    tempreg = Column(String(255))
    status = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
