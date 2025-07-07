from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "mysql+mysqlconnector://USERNAME:Password@LOCAL_IP_DATABASE:3306/DB_TABLENAME"

#Init database engine
engine = create_engine(DB_URL,echo=True)

#Create session factory bound to engine
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

#Create base class for ORM models
Base = declarative_base()
