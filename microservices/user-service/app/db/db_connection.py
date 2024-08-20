from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends
from contextlib import contextmanager
from typing import Annotated
from app import settings
import os

DATABASE_URL = os.getenv("DATABASE_URL")
connection_string: str = str(DATABASE_URL).replace("postgresql", "postgresql+psycopg")


# Create an SQLAlchemy engine
engine = create_engine(connection_string, connect_args={"sslmode": "disable"}, pool_recycle=3600, pool_size=10, echo=True)



# Function to create tables
def create_tables():
    SQLModel.metadata.create_all(engine)
    
def create_test_tables(eng):
    SQLModel.metadata.create_all(eng)

# Context manager for SQLModel session
def get_session():
    with Session(engine) as session:
        yield session

DB_SESSION = Annotated[Session, Depends(get_session)]