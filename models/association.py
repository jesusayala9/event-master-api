from sqlalchemy import Table, Column, Integer, ForeignKey
from config.database import Base

association = Table(
    'association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('event_id', Integer, ForeignKey('event.id'), primary_key=True)
) 
   