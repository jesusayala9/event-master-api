from config.database import Base
from sqlalchemy.orm  import relationship
from sqlalchemy import ARRAY, Column, Integer, String


class Users(Base):    
    __tablename__= 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    events = Column(ARRAY(String), nullable=False)
    created_events = Column(ARRAY(String), nullable=False)
    
    user_events = relationship("Event", back_populates="owner")
    