from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

from .utils import fail, error

class ExceptionMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app
        self.add_handlers()

    def add_handlers(self):
        @self.app.exception_handler(StarletteHTTPException)
        async def http_exception_handler(request: Request, exc: StarletteHTTPException):
            # Convert to fail response and wrap in JSONResponse with the actual status code
            fail_response = fail({"detail": exc.detail})
            return JSONResponse(
                status_code=exc.status_code,
                content=fail_response.dict()
            )

        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            fail_response = fail({"validation_errors": exc.errors()})
            return JSONResponse(
                status_code=422,
                content=fail_response.dict()
            )

        @self.app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception):
            # This handles unhandled errors, wrapped as JSendErrorResponse
            error_response = error(str(exc), code=500)
            return JSONResponse(
                status_code=500,
                content=error_response.dict()
            )
