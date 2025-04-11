from sqlalchemy import Column, DateTime, Integer, String, func

from app.db.session import Base


class URLMap(Base):
    __tablename__ = "url_mappings"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String, unique=True, index=True, nullable=False)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_accessed = Column(DateTime, nullable=True)
    access_count = Column(Integer, default=0, nullable=False)
