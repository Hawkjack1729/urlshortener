from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from app.api.dependencies import get_url_repository
from app.core.config import settings
from app.core.exceptions import (
    DatabaseException,
    URLNotFoundException,
    database_error_exception,
    url_not_found_exception,
)
from app.db.repositories.url_repository import URLRepository
from app.schemas.url import URLCreate, URLInfo, URLResponse

router = APIRouter()


@router.post(
    "/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED
)
def shorten_url(
    url_data: URLCreate, url_repo: URLRepository = Depends(get_url_repository)
):
    """
    Create a shortened URL

    Args:
        url_data: URL to shorten
        url_repo: URL repository

    Returns:
        Shortened URL information

    Raises:
        HTTPException: If the URL cannot be shortened
    """
    try:
        url_map = url_repo.create_url(
            original_url=str(url_data.url), custom_code=url_data.custom_code
        )

        short_url = f"{settings.BASE_URL}/{url_map.short_code}"

        return URLResponse(
            short_code=url_map.short_code,
            short_url=short_url,
            original_url=url_map.original_url,
        )

    except DatabaseException as e:
        raise database_error_exception()


@router.get("/{short_code}")
def redirect_to_url(
    short_code: str, url_repo: URLRepository = Depends(get_url_repository)
):
    """
    Redirect to the original URL

    Args:
        short_code: Short code of the URL
        url_repo: URL repository

    Returns:
        Redirect to the original URL

    Raises:
        HTTPException: If the URL is not found
    """
    try:
        url_map = url_repo.get_by_short_code(short_code)

        # Update access statistics
        url_repo.update_access_stats(short_code)

        return RedirectResponse(url=url_map.original_url)

    except URLNotFoundException:
        raise url_not_found_exception()
    except DatabaseException:
        raise database_error_exception()


@router.get("/info/{short_code}", response_model=URLInfo)
def get_url_info(
    short_code: str, url_repo: URLRepository = Depends(get_url_repository)
):
    """
    Get information about a shortened URL

    Args:
        short_code: Short code of the URL
        url_repo: URL repository

    Returns:
        Information about the URL

    Raises:
        HTTPException: If the URL is not found
    """
    try:
        url_map = url_repo.get_by_short_code(short_code)

        short_url = f"{settings.BASE_URL}/{url_map.short_code}"

        return URLInfo(
            short_code=url_map.short_code,
            short_url=short_url,
            original_url=url_map.original_url,
            created_at=url_map.created_at,
            last_accessed=url_map.last_accessed,
            access_count=url_map.access_count,
        )

    except URLNotFoundException:
        raise url_not_found_exception()
    except DatabaseException:
        raise database_error_exception()
