from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class Event(Base):
    
    __tablename__= 'event'
    
    id = Column(Integer, primary_key=True,  autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    startTime = Column(DateTime, nullable=False)
    finishTime = Column(DateTime, nullable=False)
    category = Column(String(255))
    audience = Column(Integer)
    type = Column(String(255))
    location = Column(String(255))
    
    