import secrets
import string
from typing import Optional

from .config import Settings


def generate_short_code(length: Optional[int] = None) -> str:
    """
    Generate a random short code for URL shortening

    Args:
        length: Length of the short code. Defaults to the value from settings.

    Returns:
        A random string of specified length
    """
    if length is None:
        length = settings.SHORT_CODE_LENGTH

    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def generate_random_secret_key(length: int = 32) -> str:
    """
    Generate a random secret key

    Args:
        length: Length of the secret key

    Returns:
        A random string of specified length
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(chars) for _ in range(length))
