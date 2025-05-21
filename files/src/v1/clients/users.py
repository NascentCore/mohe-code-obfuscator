import json
from urllib.parse import urljoin
from uuid import UUID

import httpx

from . import api_config
from ..exceptions.authorization import AuthorizationInvalid
from ..exceptions.services import UsersServiceNotAvailable


class UsersClient:

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or api_config.users_base_url

    async def get_user_id(self, authorization: str) -> UUID:
        """
        Validate the Authorization header with the Users service.

        Args:
            authorization (str): The Authorization header

        Returns:
            str: The user ID

        Raises:
            UsersServiceNotAvailable: If the Users service is not available
            AuthorizationInvalid: If the Authorization header is invalid
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    urljoin(self.base_url, "/v1/users/validate"),
                    headers={"Authorization": authorization},
                )

                if response.status_code >= 500:
                    raise UsersServiceNotAvailable()
                elif response.status_code == 401:
                    raise AuthorizationInvalid()

                try:
                    return UUID(response.json()["user_id"])
                except json.JSONDecodeError:
                    pass
        except httpx.RequestError as e:
            raise UsersServiceNotAvailable() from e
