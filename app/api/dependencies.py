from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.repositories.url_repository import URLRepository
from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Get a database session

    Yields:
        A database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_url_repository(db: Session = Depends(get_db)) -> URLRepository:
    """
    Get a URL repository instance

    Args:
        db: Database session

    Returns:
        A URL repository instance
    """
    return URLRepository(db)
