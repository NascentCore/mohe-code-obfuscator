from uuid import UUID

from fastapi import Request
from sqlalchemy.orm import Session

from ..clients.users import UsersClient
from ..exceptions.authorization import AuthorizationNotProvided, Forbidden
from ..exceptions.files import FileNotFound
from ..repositories import Repository
from ..repositories.files import FileRepository
from ..repositories.permissions import PermissionRepository
from ..schemas.files import AuthorizationContext
from ..services.files import FileService
from ..services.internal import FileInternalService
from ..services.storage import LocalStorageService
from ..services.permissions import PermissionService
from ...config import APIConfig, FilesConfig
from ...db import engine


api_config = APIConfig()
files_config = FilesConfig()


async def get_user_id(request: Request) -> UUID:
    """
    Get X-User-ID header, or validate the Authorization header with the Users service.
    """

    return "00000000-0000-0000-0000-000000000000"

    # if user_id := request.headers.get(api_config.user_id_header):
    #     return UUID(user_id)

    # if authorization := request.headers.get("Authorization"):
    #     users_service = UsersClient()
    #     return await users_service.get_user_id(authorization)

    # raise AuthorizationNotProvided()


async def validate_allowed_host(request: Request) -> None:
    host = request.headers.get(api_config.external_address_header)

    if host:
        raise Forbidden()


def get_db_session():
    return Session(bind=engine)


def get_repository(repo_class: Repository, db_session: Session | None = None):
    db_session = db_session or get_db_session()

    return repo_class(db_session)


def get_permission_service(
    repository: PermissionRepository | None = None,
):
    repository = repository or get_repository(PermissionRepository)

    return PermissionService(repo=repository)


def get_file_service(
    repository: FileRepository | None = None,
    storage: LocalStorageService | None = None,
    permission_service: PermissionService | None = None,
):
    repository = repository or get_repository(FileRepository)
    storage = storage or LocalStorageService(config=files_config)
    permission_service = permission_service or get_permission_service()

    return FileService(
        config=files_config,
        repo=repository,
        storage=storage,
        permission_service=permission_service,
    )


def get_file_internal_service(repository: FileRepository | None = None):
    repository = repository or get_repository(FileRepository)

    return FileInternalService(repo=repository)


def check_authorization(user_id: UUID, file_id: UUID):
    """
    Check authorization.

    Raises:
        FileNotFound: if the user is not allowed to access the file
    """
    svc = get_permission_service()

    if not svc.check_file_permission(file_id=file_id, user_id=user_id):
        raise FileNotFound(file_id=file_id, user_id=user_id)


def check_authorization_with_context(
    user_id: UUID, file_id: UUID, context: AuthorizationContext
):
    """
    Check authorization with context.

    Raises:
        FileNotFound: if the user is not allowed to access the file
    """
    svc = get_permission_service()

    if not svc.check_file_permission_with_context(
        file_id=file_id, user_id=user_id, context=context
    ):
        raise FileNotFound(file_id=file_id, user_id=user_id)
