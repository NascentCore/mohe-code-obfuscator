from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from src import __title__, __version__
from src.v1.api import router as v1_router
from src.v1.schemas.errors import Error
from src.v1.exceptions import ErrorRegistry

app = FastAPI()


@app.get("/")
def index():
    return JSONResponse({"title": __title__, "version": __version__})


@app.get("/healthz")
def healthz():
    return JSONResponse({"status": "ok"})


@app.get("/readyz")
def readyz():
    return JSONResponse({"status": "ok"})


app.include_router(v1_router)


async def global_exception_handler(request: Request, exc: Exception):
    try:
        meta = ErrorRegistry.get_meta_by_class(exc)
    except KeyError:
        # Unknown error
        return JSONResponse(
            content=Error(code="UnknownError", message="").model_dump(), status_code=500
        )

    if meta.is_technical:
        return JSONResponse(
            content=Error(
                code="InternalServerError",
                message="Internal server error, please try again later.",
                details=getattr(exc, "details", None),
            ).model_dump(),
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    return JSONResponse(
        content=Error(
            code=meta.code,
            message=str(exc),
            details=getattr(exc, "details", None),
        ).model_dump(),
        status_code=meta.http_status,
    )


app.add_exception_handler(Exception, global_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app:app", host="0.0.0.0", port=8005, reload=False)