from fastapi import APIRouter

from .files import router as files_router
from .internal import router as internal_router

router = APIRouter(prefix="/v1")
router.include_router(files_router)
router.include_router(internal_router)

