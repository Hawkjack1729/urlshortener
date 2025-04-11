from fastapi import HTTPException, status


class URLShortenerException(Exception):
    """Base exception for URL Shortener application"""

    pass


class URLNotFoundException(URLShortenerException):
    """Raised when a URL with the given short code is not found"""

    pass


class DatabaseException(URLShortenerException):
    """Raised when a database operation fails"""

    pass


class InvalidURLException(URLShortenerException):
    """Raised when the provided URL is invalid"""

    pass


# HTTP Exception Factories
def url_not_found_exception() -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")


def database_error_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database error occurred",
    )


def invalid_url_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL provided"
    )
