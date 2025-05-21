from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from .dependencies import get_file_internal_service, validate_allowed_host

router = APIRouter(prefix="/internal")


@router.get("/files/{file_id}/content")
async def get_file_content(
    file_id: UUID,
    _=Depends(validate_allowed_host),
):
    svc = get_file_internal_service()

    file = svc.get(file_id)

    return FileResponse(
        file.path, media_type="application/octet-stream", filename=file.filename
    )
