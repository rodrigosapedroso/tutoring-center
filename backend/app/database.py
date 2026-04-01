import os

from dotenv import load_dotenv
load_dotenv()  
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL connection 
DATABASE_URL = os.getenv("DATABASE_URL")

# The engine is the core connection interface to the database
engine = create_engine(DATABASE_URL)

# Each request will create its own database session using this
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Every model (table) will inherit from this
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()