from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logger import get_logger


logger = get_logger()

async def http_exception_handler(request: Request, exc: Exception):
    # Optional: check type if needed
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": exc.detail, "path": str(request.url.path)},
        )
    # fallback
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"},
    )




async def validation_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"success": False, "error": "Validation failed", "details": exc.errors(), "path": str(request.url.path)},
        )
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"},
    )



async def unhandled_exception_handler(
    request: Request,
    exc: Exception
):
    user_id = getattr(request.state, "user_id", None)
    tenant_id = getattr(request.state, "tenant_id", None)

    logger.exception(
        f"Unhandled error | "
        f"{request.method} {request.url.path} | "
        f"user_id={user_id} | tenant_id={tenant_id}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error"
        }
    )
