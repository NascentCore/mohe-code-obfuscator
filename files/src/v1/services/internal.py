from uuid import UUID

from ..repositories.files import FileRepository


class FileInternalService:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    def get(self, id: UUID):
        return self.repo.get(id)
