from enum import StrEnum
from http import HTTPStatus
from urllib.parse import urljoin
from uuid import UUID

import httpx
from pydantic import BaseModel

from . import api_config
from ..exceptions.services import BasesServiceNotAvailable


class PrincipalType(StrEnum):
    USER = "user"


class AttachmentObjectType(StrEnum):
    FILE = "file"


class PermissionCheck(BaseModel):

    principal_id: UUID
    attachment_id: UUID
    object_id: UUID

    base_id: UUID | None = None
    folder_id: UUID | None = None

    principal_type: PrincipalType = PrincipalType.USER
    object_type: AttachmentObjectType = AttachmentObjectType.FILE


class BasesClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or api_config.bases_base_url
        self.user_id_header = api_config.user_id_header

    def check_permissions(self, user_id: UUID, data: PermissionCheck) -> bool:
        try:
            with httpx.Client() as client:
                response = client.get(
                    urljoin(self.base_url, "/v1/permissions/check"),
                    headers={self.user_id_header: str(user_id)},
                    params=data.model_dump(mode="json", exclude_none=True),
                )

                if HTTPStatus(response.status_code).is_success:
                    return True
                elif HTTPStatus(response.status_code).is_client_error:
                    return False
                if HTTPStatus(response.status_code).is_server_error:
                    raise BasesServiceNotAvailable()

        except httpx.RequestError:
            raise BasesServiceNotAvailable()
