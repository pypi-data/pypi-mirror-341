from .models import JSendSuccessResponse, JSendFailResponse, JSendErrorResponse
from typing import Any

def success(data: Any):
    return JSendSuccessResponse(data=data)

def fail(data: Any):
    return JSendFailResponse(data=data)

def error(message: str, code: int = None, data: Any = None):
    return JSendErrorResponse(message=message, code=code, data=data)