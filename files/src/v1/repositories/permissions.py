from uuid import UUID

from sqlalchemy.orm import Session

from . import Repository
from ...models import File


class PermissionRepository(Repository):
    def __init__(self, session: Session | None = None):
        super().__init__(session)

    def check_file_permission(self, user_id: UUID, file_id: UUID) -> bool:
        file = (
            self.session.query(File)
            .filter(File.id == file_id, File.user_id == user_id)
            .first()
        )

        return file is not None
