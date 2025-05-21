from pathlib import Path
from uuid import UUID

from .storage import LocalStorageService
from ..exceptions.files import (
    FileNotExists,
    FileNotFound,
    FileTooLarge,
    FiletypeNotAllowed,
)
from ..repositories.files import FileRepository
from ..schemas.files import (
    AuthorizationContext,
    File,
    FileBatchGet,
    FileBatchGetResponse,
    FileDetailsRequest,
    FileDetailsResponse,
    FileListRequest,
    FileListResponse,
    FileUpdateRequest,
    LocalFileCreateRequest,
)
from ..services.permissions import PermissionService
from ...config import FilesConfig


class FileService:
    def __init__(
        self,
        config: FilesConfig,
        repo: FileRepository,
        storage: LocalStorageService,
        permission_service: PermissionService,
    ):
        self.config = config
        self.repo = repo
        self.storage = storage
        self.permission_service = permission_service

    def get(self, id: UUID) -> File:
        with self.repo as repo:
            try:
                file = repo.get(id)

                return File.model_validate(file)
            except FileNotExists:
                raise FileNotFound(id)

    def get_by_user_id_page_paginated(
        self, data: FileListRequest, user_id: UUID
    ) -> FileListResponse:
        with self.repo as repo:
            paginated = repo.get_by_user_id_page_paginated(
                user_id=user_id,
                page=data.page,
                page_size=data.page_size,
                order_by=data.order_by,
                order=data.order,
            )

            return FileListResponse.model_validate(paginated)

    def get_by_ids(
        self, data: FileDetailsRequest, user_id: UUID
    ) -> FileDetailsResponse:
        with self.repo as repo:
            files = repo.get_by_ids_and_user_id(ids=data.ids, user_id=user_id)

            return FileDetailsResponse(items=files)

    def batch_get(self, data: FileBatchGet, user_id: UUID) -> FileBatchGetResponse:
        with self.repo as repo:
            files = repo.get_by_ids(ids=[item.file_id for item in data.items])
            files_dict = {file.id: file for file in files}
            allowed_files = []

            for item in data.items:
                file = files_dict.get(item.file_id)
                if file is None:
                    continue

                # 根据是否有 attachment_id 执行不同的权限检查
                has_permission = False
                if item.attachment_id:
                    context = AuthorizationContext(
                        base_id=item.base_id,
                        folder_id=item.folder_id,
                        attachment_id=item.attachment_id,
                    )
                    has_permission = (
                        self.permission_service.check_file_permission_with_context(
                            file_id=file.id, user_id=user_id, context=context
                        )
                    )
                else:
                    has_permission = self.permission_service.check_file_permission(
                        file_id=file.id, user_id=user_id
                    )

                if has_permission:
                    allowed_files.append(file)

            return FileBatchGetResponse(items=allowed_files)

    def create_from_local(self, data: LocalFileCreateRequest, user_id: UUID) -> File:
        with self.repo as repo:
            path = Path(data.path)

            self.validate_size(size_bytes=path.stat().st_size)
            self.validate_extension(extension=path.suffix)
            if data.filename:
                self.validate_extension(extension=Path(data.filename).suffix)

            file = repo.create(
                path=path,
                user_id=user_id,
                filename=data.filename or path.name,
                extra=data.extra,
            )

            return File.model_validate(file)

    def create_from_binary(
        self,
        bytes: bytes,
        filename: str,
        size_bytes: int,
        user_id: UUID,
        extra: dict | None = None,
    ) -> File:
        with self.repo as repo:
            # Validate if allowed
            self.validate_size(size_bytes=size_bytes)
            self.validate_extension(extension=Path(filename).suffix)
            # Generate a new filename and save to storage
            path = self.storage.get_path(filename, user_id)
            self.storage.save_binary(bytes, path)
            # Create the file in the database
            file = repo.create(
                path=path,
                user_id=user_id,
                filename=filename,
                extra=extra,
            )

            return File.model_validate(file)

    def validate_size(self, size_bytes: int) -> None:
        if size_bytes > self.config.max_file_size:
            raise FileTooLarge(self.config.max_file_size, size_bytes)

    def validate_extension(self, extension: str) -> None:
        extension = extension.lstrip(".")
        if extension not in self.config.allowed_extensions:
            raise FiletypeNotAllowed(extension, self.config.allowed_extensions)

    def update(self, id: UUID, data: FileUpdateRequest) -> File:
        with self.repo as repo:
            file = repo.update(id, extra=data.extra)

            return File.model_validate(file)

    def delete(self, id: UUID) -> None:
        """
        Delete a file record from the database.
        """
        with self.repo as repo:
            file = repo.get(id)

            repo.delete(id, commit=False)

            self.storage.delete(Path(file.path))

            repo.commit()

            return

    def soft_delete(self, id: UUID) -> File:
        """
        Mark a file as deleted in the database.
        """
        with self.repo as repo:
            file = repo.soft_delete(id)

            return File.model_validate(file)

    def restore(self, id: UUID) -> File:
        """
        Mark a file as restored in the database.
        """
        with self.repo as repo:
            file = repo.restore(id)

            return File.model_validate(file)
