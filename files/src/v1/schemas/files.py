from typing import Any, Literal
from uuid import UUID

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class File(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    filename: str
    path: str
    size_bytes: int
    extension: str
    extra: Any | None

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    @field_serializer("created_at", "updated_at", "deleted_at")
    def serialize_datetime(self, value: datetime | None) -> int:
        return int(value.timestamp()) if value is not None else None


class LocalFileCreateRequest(BaseModel):
    path: str
    filename: str | None = None
    extra: Any | None = None


class FileUpdateRequest(BaseModel):
    extra: Any


class FileListRequest(BaseModel):
    page: int = 1
    page_size: int = 10
    order_by: Literal["created_at", "updated_at"] = "updated_at"
    order: Literal["asc", "desc"] = "desc"


class FileListResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    total: int
    pages: int
    page: int
    page_size: int
    items: list[File]


class FileBatchGetItem(BaseModel):
    file_id: UUID
    attachment_id: UUID | None = None
    folder_id: UUID | None = None
    base_id: UUID | None = None


class FileBatchGet(BaseModel):
    items: list[FileBatchGetItem]


class FileBatchGetResponse(BaseModel):
    items: list[File]


class FileDetailsRequest(BaseModel):
    ids: list[UUID]


class FileDetailsResponse(BaseModel):
    items: list[File]


class AuthorizationContext(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    base_id: UUID | None = None
    folder_id: UUID | None = None
    attachment_id: UUID
