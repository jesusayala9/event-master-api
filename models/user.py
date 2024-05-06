from config.database import Base
from sqlalchemy import ARRAY, Column, Integer, String

class User(Base):    
    __tablename__= 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)
    events = Column(ARRAY(String), nullable=False)
    created_events = Column(ARRAY(String), nullable=False)