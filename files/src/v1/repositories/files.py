import math
from pathlib import Path
from typing import Literal
from uuid import UUID

from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session

from . import Pagination, Repository
from ..exceptions.files import FileNotExists
from ...models import File


class FileRepository(Repository):
    def __init__(self, session: Session | None = None):
        super().__init__(session)

    def get(self, id: UUID, include_soft_deleted: bool = True) -> File:
        query = self.session.query(File).filter(File.id == id)

        if not include_soft_deleted:
            query = query.filter(File.deleted_at.is_(None))

        file = query.one_or_none()

        if file is None:
            raise FileNotExists(id)

        return file

    def get_by_user_id(
        self,
        user_id: UUID,
        include_soft_deleted: bool = True,
    ) -> list[File]:
        query = self.session.query(File).filter(File.user_id == user_id)

        if not include_soft_deleted:
            query = query.filter(File.deleted_at.is_(None))

        return query.all()

    def get_by_ids(
        self,
        ids: list[UUID],
        include_soft_deleted: bool = True,
    ) -> list[File]:
        query = self.session.query(File).filter(File.id.in_(ids))

        if not include_soft_deleted:
            query = query.filter(File.deleted_at.is_(None))

        return query.all()

    def get_by_ids_and_user_id(
        self,
        ids: list[UUID],
        user_id: UUID,
        include_soft_deleted: bool = True,
    ) -> list[File]:
        query = self.session.query(File).filter(
            File.id.in_(ids), File.user_id == user_id
        )

        if not include_soft_deleted:
            query = query.filter(File.deleted_at.is_(None))

        return query.all()

    def get_by_user_id_page_paginated(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 10,
        order_by: Literal["created_at", "updated_at"] = "updated_at",
        order: Literal["asc", "desc"] = "desc",
        include_soft_deleted: bool = True,
    ) -> Pagination:
        query = self.session.query(File).filter(File.user_id == user_id)

        if not include_soft_deleted:
            query = query.filter(File.deleted_at.is_(None))

        total = query.count()
        pages = math.ceil(total / page_size)

        column = getattr(File, order_by)
        if order == "asc":
            query = query.order_by(asc(column))
        elif order == "desc":
            query = query.order_by(desc(column))

        query = query.limit(page_size).offset((page - 1) * page_size)

        return Pagination(
            total=total,
            pages=pages,
            page=page,
            page_size=page_size,
            items=query.all(),
        )

    def create(
        self,
        path: Path,
        user_id: UUID,
        filename: str | None = None,
        extra: dict | None = None,
        commit: bool = True,
    ) -> File:
        file = File(
            user_id=user_id,
            filename=filename if filename else path.name,
            path=str(path.absolute()),  # path is absolute
            size_bytes=path.stat().st_size,
            extension=path.suffix.lstrip("."),
            extra=extra,
        )

        self.session.add(file)

        if commit:
            self.session.commit()

        return file

    def update(self, id: UUID, extra: dict, commit: bool = True):
        file = self.get(id)

        file.extra = extra

        if commit:
            self.session.commit()

        return file

    def delete(self, id: UUID, commit: bool = True) -> None:
        file = self.get(id)

        self.session.delete(file)

        if commit:
            self.session.commit()

    def soft_delete(self, id: UUID, commit: bool = True) -> File:
        """
        Mark a file as deleted in the database.
        """
        file = self.get(id)

        if file.deleted_at is None:
            file.deleted_at = func.now()

        if commit:
            self.session.commit()

        return file

    def restore(self, id: UUID, commit: bool = True) -> File:
        file = self.get(id)

        if file.deleted_at is not None:
            file.deleted_at = None

        if commit:
            self.session.commit()

        return file
