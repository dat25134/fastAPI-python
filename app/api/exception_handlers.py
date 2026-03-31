from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from app.schemas.response import ResponseError, ErrorDetail

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle 422 Unprocessable Entity (Pydantic validation errors)
    """
    error = ErrorDetail(
        code="VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ",
        details=exc.errors()
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ResponseError(error=error).model_dump()
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle 4xx and other HTTPExceptions
    """
    error = ErrorDetail(
        code=exc.headers.get("X-Error-Code", "HTTP_EXCEPTION") if exc.headers else "HTTP_EXCEPTION",
        message=exc.detail,
        details=None
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseError(error=error).model_dump()
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handle 500 Internal Server Error (Unexpected errors)
    """
    # In production, log this error in detail!
    error = ErrorDetail(
        code="INTERNAL_SERVER_ERROR",
        message="Đã có lỗi hệ thống xảy ra, vui lòng thử lại sau.",
        details=str(exc) # Limit details in production for security!
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ResponseError(error=error).model_dump()
    )
