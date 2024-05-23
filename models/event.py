from config.database import Base
from sqlalchemy.orm import relationship
from models.association import association
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey



class Event(Base):
    
    __tablename__= 'event'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    finish_time = Column(DateTime, nullable=False)
    category = Column(String(255))
    audience = Column(Integer, default=0)
    type = Column(String(255))
    location = Column(String(255))    
    # Relación muchos a muchos con usuarios
    attendees = relationship("Users", secondary=association, back_populates="events")    
    # Relación uno a muchos con usuarios para el creador del evento
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("Users", back_populates="created_events")
    
   
    
    