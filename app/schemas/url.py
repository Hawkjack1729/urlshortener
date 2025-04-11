from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, validator


class URLBase(BaseModel):
    """Base URL schema"""

    pass


class URLCreate(URLBase):
    """Schema for creating a new URL"""

    url: str = Field(..., description="The original URL to be shortened")
    custom_code: Optional[str] = Field(None, description="Optional custom short code")

    @validator("url")
    def ensure_scheme(cls, v):
        if not v.startswith(("http://", "https://")):
            return "http://" + v
        return v


class URLResponse(URLBase):
    """Schema for URL response"""

    short_code: str
    short_url: str
    original_url: str


class URLInfo(URLResponse):
    """Schema for detailed URL information"""

    created_at: datetime
    last_accessed: Optional[datetime] = None
    access_count: int

    class Config:
        from_attributes = True
