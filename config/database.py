from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database_url = f'postgresql://postgres:12345678@localhost:5432/Databases'
engine = create_engine(database_url)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
