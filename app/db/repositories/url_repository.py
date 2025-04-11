from datetime import datetime
from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseException, URLNotFoundException
from app.core.security import generate_short_code
from app.models.url import URLMap


class URLRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_url(
        self, original_url: str, custom_code: Optional[str] = None
    ) -> URLMap:
        """
        Create a new URL mapping

        Args:
            original_url: The original URL to shorten
            custom_code: Optional custom short code

        Returns:
            The created URL mapping

        Raises:
            DatabaseException: If a database error occurs
        """
        try:
            # Generate or use custom short code
            short_code = custom_code if custom_code else self._generate_unique_code()

            url_map = URLMap(
                short_code=short_code,
                original_url=original_url,
            )

            self.db.add(url_map)
            self.db.commit()
            self.db.refresh(url_map)

            return url_map

        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(f"Error creating URL: {str(e)}")

    def get_by_short_code(self, short_code: str) -> URLMap:
        """
        Get URL mapping by short code

        Args:
            short_code: The short code to look up

        Returns:
            The URL mapping if found

        Raises:
            URLNotFoundException: If the URL is not found
        """
        url_map = self.db.query(URLMap).filter(URLMap.short_code == short_code).first()

        if not url_map:
            raise URLNotFoundException(f"URL with short code '{short_code}' not found")

        return url_map

    def update_access_stats(self, short_code: str) -> None:
        """
        Update access statistics for a URL

        Args:
            short_code: The short code of the URL

        Raises:
            DatabaseException: If a database error occurs
        """
        try:
            stmt = (
                update(URLMap)
                .where(URLMap.short_code == short_code)
                .values(
                    last_accessed=datetime.now(), access_count=URLMap.access_count + 1
                )
            )

            self.db.execute(stmt)
            self.db.commit()

        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(f"Error updating access stats: {str(e)}")

    def _generate_unique_code(self) -> str:
        """
        Generate a unique short code that doesn't exist in the database

        Returns:
            A unique short code
        """
        while True:
            short_code = generate_short_code()
            existing = (
                self.db.query(URLMap).filter(URLMap.short_code == short_code).first()
            )
            if not existing:
                return short_code
