import json
from http import HTTPStatus
from uuid import UUID
from typing import Type, Optional
from typing import List, Union


from . import ErrorRegistry


@ErrorRegistry.register(
    code="FileNotExists",
    http_status=HTTPStatus.NOT_FOUND,
    description="",
    is_technical=False,
    # i18n_key="user.not_found"
)
class FileNotExists(Exception):
    def __init__(self, id: UUID):
        self.id = id
        self.details = json.dumps({"id": str(self.id)})
        super().__init__()


@ErrorRegistry.register(
    code="FileNotFound",
    http_status=HTTPStatus.NOT_FOUND,
    description="",
    is_technical=False,
    # i18n_key="user.not_found"
)
class FileNotFound(Exception):
    def __init__(self, file_id: UUID, user_id: UUID | None = None):
        self.file_id = file_id
        self.user_id = user_id
        self.details = json.dumps(
            {"file_id": str(file_id), "user_id": str(user_id) if user_id else None}
        )
        super().__init__()


@ErrorRegistry.register(
    code="FiletypeNotAllowed",
    http_status=HTTPStatus.BAD_REQUEST,
    description="",
    is_technical=False,
    # i18n_key="user.not_found"
)
class FiletypeNotAllowed(Exception):
    def __init__(self, current: str, supported: Optional[list[str]] = None):
        self.supported = supported
        self.current = current
        self.details = json.dumps({"current": current, "supported": self.supported})
        super().__init__()


@ErrorRegistry.register(
    code="FileTooLarge",
    http_status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
    description="",
    is_technical=False,
    # i18n_key="user.not_found"
)
class FileTooLarge(Exception):
    def __init__(self, limit: int, size: int):
        self.limit = limit
        self.size = size
        self.details = json.dumps({"limit": limit, "size": size})
        super().__init__()


@ErrorRegistry.register(
    code="InvalidJSONContent",
    http_status=HTTPStatus.BAD_REQUEST,
    description="",
    is_technical=False,
    # i18n_key="user.not_found"
)
class InvalidJSONContent(Exception):
    pass
