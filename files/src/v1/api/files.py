import json
from datetime import datetime
from http import HTTPStatus
from uuid import UUID


from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import FileResponse
from pydantic import ValidationError

from .dependencies import (
    check_authorization,
    check_authorization_with_context,
    get_file_service,
    get_user_id,
)
from ..exceptions.files import InvalidJSONContent
from ..schemas.files import (
    AuthorizationContext,
    FileBatchGet,
    FileDetailsRequest,
    FileDetailsResponse,
    FileListRequest,
    FileUpdateRequest,
    LocalFileCreateRequest,
)

router = APIRouter(prefix="/files")


@router.get("")
async def list_files(
    data: FileListRequest = Depends(),
    user_id: UUID = Depends(get_user_id),
):
    svc = get_file_service()

    return svc.get_by_user_id_page_paginated(data, user_id=user_id)


@router.post("/details")
async def get_files_details(
    data: FileDetailsRequest,
    user_id: UUID = Depends(get_user_id),
):
    DEPRECATION = datetime(2025, 5, 31, 23, 59, 59)

    if datetime.now() > DEPRECATION:
        raise Response(status_code=HTTPStatus.GONE)

    svc = get_file_service()

    return Response(
        content=svc.get_by_ids(data=data, user_id=user_id).model_dump_json(),
        media_type="application/json",
        headers={"Deprecation": f"@{int(DEPRECATION.timestamp())}"},
    )


@router.post("/batch-get")
async def batch_get_files(
    data: FileBatchGet,
    user_id: UUID = Depends(get_user_id),
):
    svc = get_file_service()

    return svc.batch_get(data=data, user_id=user_id)


@router.post("")
async def create_files(
    request: Request,
    user_id: UUID = Depends(get_user_id),
):
    svc = get_file_service()
    created = []

    if request.headers.get("Content-Type") == "application/json":
        json_data = [
            LocalFileCreateRequest.model_validate(obj) for obj in await request.json()
        ]

        for req in json_data:
            file = svc.create_from_local(data=req, user_id=user_id)

            created.append(file)
    else:
        form_data = await request.form()
        files = form_data.getlist("files")
        extra = form_data.get("extra")

        if extra:
            try:
                extra = json.loads(extra)
            except json.JSONDecodeError as e:
                raise InvalidJSONContent(details=e.msg)

        for file in files:
            file = svc.create_from_binary(
                bytes=file.file,
                size_bytes=file.size,
                filename=file.filename,
                user_id=user_id,
                extra=extra,
            )

            created.append(file)

    return created


@router.get("/{file_id}")
async def get_file(
    file_id: UUID,
    request: Request,
    user_id: UUID = Depends(get_user_id),
):
    try:
        context = AuthorizationContext.model_validate(request.query_params)
    except ValidationError:
        context = None

    if context:
        check_authorization_with_context(
            user_id=user_id, file_id=file_id, context=context
        )
    else:
        check_authorization(user_id=user_id, file_id=file_id)

    svc = get_file_service()

    return svc.get(file_id)


@router.get("/{file_id}/content")
async def get_file_content(
    file_id: UUID,
    request: Request,
    user_id: UUID = Depends(get_user_id),
):
    try:
        context = AuthorizationContext.model_validate(request.query_params)
    except ValidationError:
        context = None

    if context:
        check_authorization_with_context(
            user_id=user_id, file_id=file_id, context=context
        )
    else:
        check_authorization(user_id=user_id, file_id=file_id)

    svc = get_file_service()

    file = svc.get(file_id)

    if file.extension == "wav":
        media_type = "audio/wav"
    else:
        media_type = "application/octet-stream"

    return FileResponse(file.path, media_type=media_type, filename=file.filename)


@router.put("/{file_id}")
async def update_file(
    file_id: UUID,
    data: FileUpdateRequest,
    user_id: UUID = Depends(get_user_id),
):
    check_authorization(user_id=user_id, file_id=file_id)

    svc = get_file_service()

    return svc.update(file_id, data)


@router.delete("/{file_id}")
async def delete_file(
    file_id: UUID,
    user_id: UUID = Depends(get_user_id),
):
    check_authorization(user_id=user_id, file_id=file_id)

    svc = get_file_service()

    svc.delete(file_id)

    return Response(status_code=204)


@router.post("/{file_id}/soft-delete")
async def soft_delete_file(
    file_id: UUID,
    user_id: UUID = Depends(get_user_id),
):
    check_authorization(user_id=user_id, file_id=file_id)

    svc = get_file_service()

    svc.soft_delete(file_id)

    return Response(status_code=204)


@router.post("/{file_id}/restore")
async def restore_file(
    file_id: UUID,
    user_id: UUID = Depends(get_user_id),
):
    check_authorization(user_id=user_id, file_id=file_id)

    svc = get_file_service()

    return svc.restore(file_id)
