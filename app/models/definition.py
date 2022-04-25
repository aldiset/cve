from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from app.database.engine import Base

class Definition(Base):
    __tablename__ = "definition"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String)
    value = Column(String)
    source = Column(String)
    created_date = Column(DateTime, default=datetime.now)
    updated_date = Column(DateTime, onupdate=datetime.now)
    deleted_date = Column(DateTime)