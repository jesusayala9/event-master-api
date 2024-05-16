from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



database_url = 'postgresql://postgres:12345678@localhost:5432/event-master'
# database_url = 'postgresql://demo1linkisite_adminP:Munivalle@demo1.linkisite.com:5432/demo1linkisite_Event_Master2024'

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
