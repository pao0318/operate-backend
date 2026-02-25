from pydantic import BaseModel
from typing import Any, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


class ResponseWrapper(BaseModel, Generic[T]):
    data: T


class ErrorResponse(BaseModel):
    error: Dict[str, Any]
