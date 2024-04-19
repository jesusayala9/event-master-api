from config.database import Base
from sqlalchemy.orm import  Session
from sqlalchemy import Column, Integer, String, DateTime


class Event(Base):
    
    __tablename__= 'event'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255))
    start_time = Column(DateTime, nullable=False)
    finish_time = Column(DateTime, nullable=False)
    category = Column(String(255))
    audience = Column(Integer)
    type = Column(String(255))
    location = Column(String(255))
    
    