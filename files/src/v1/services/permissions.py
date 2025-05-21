from uuid import UUID

from ..clients.bases import BasesClient, PermissionCheck
from ..repositories.permissions import PermissionRepository
from ..schemas.files import AuthorizationContext


class PermissionService:
    def __init__(self, repo: PermissionRepository):
        self.repo = repo

    def check_file_permission(self, file_id: UUID, user_id: UUID) -> bool:

        with self.repo as repo:
            if repo.check_file_permission(user_id=user_id, file_id=file_id):
                return True

        return False

    def check_file_permission_with_context(
        self, file_id: UUID, user_id: UUID, context: AuthorizationContext
    ) -> bool:
        with self.repo as repo:
            if repo.check_file_permission(user_id=user_id, file_id=file_id):
                return True

        client = BasesClient()
        if client.check_permissions(
            user_id=user_id,
            data=PermissionCheck(
                principal_id=user_id,
                base_id=context.base_id,
                folder_id=context.folder_id,
                attachment_id=context.attachment_id,
                object_id=file_id,
            ),
        ):
            return True

        return False
