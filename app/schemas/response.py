from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None

class ResponseSuccess(BaseModel, Generic[T]):
    success: bool = True
    data: T
    metadata: Optional[dict[str, Any]] = None

class ResponseError(BaseModel):
    success: bool = False
    error: ErrorDetail
