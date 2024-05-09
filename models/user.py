from config.database import Base
from sqlalchemy.orm import relationship
from models.association import association
from sqlalchemy import  Column, Integer, String



class Users(Base):    
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)    
     # Relación con eventos a los que asiste el usuario
    events = relationship("Event", secondary=association, back_populates="attendees")    
    # Relación con eventos creados por el usuario
    created_events = relationship("Event", back_populates="creator")

    
    