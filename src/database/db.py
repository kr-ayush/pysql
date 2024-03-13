"""
Datbase Connection File
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database
engine = create_engine(
    "sqlite:///../hospital.db", connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """yields session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
