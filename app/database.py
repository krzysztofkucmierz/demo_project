"""Database configuration and connection management."""

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel

# Database URL from environment or default to local PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost:5431/demo_project"
)

# Create engine with connection pooling
engine: Engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,
    pool_recycle=3600,
)


def create_db_and_tables() -> None:
    """Create database tables based on SQLModel definitions."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session]:
    """Get database session for dependency injection."""
    with Session(engine) as session:
        yield session
