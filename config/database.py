from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.config_general import settings  # Importar la configuración




# Usar la URL de la base de datos desde la configuración
database_url = settings.database_url

# Crear el motor de la base de datos
engine = create_engine(database_url)

# Crear la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa
Base = declarative_base()
