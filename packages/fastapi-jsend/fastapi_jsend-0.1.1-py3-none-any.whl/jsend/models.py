from pydantic import BaseModel
from typing import Any, Optional


class JSendSuccessResponse(BaseModel):
    status: str = "success"
    data: Any


class JSendFailResponse(BaseModel):
    status: str = "fail"
    data: Any


class JSendErrorResponse(BaseModel):
    status: str = "error"
    message: str
    code: Optional[int] = None
    data: Optional[Any] = None