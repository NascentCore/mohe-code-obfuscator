from uuid import uuid4

from sqlalchemy import Column, DateTime, func, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase

from .constants import StringLength


class Base(DeclarativeBase):
    pass


class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    filename = Column(String(StringLength.FILE_FILENAME), nullable=False)
    path = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    extension = Column(String(StringLength.FILE_EXTENSION), nullable=False)
    extra = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)
