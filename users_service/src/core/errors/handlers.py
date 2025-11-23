from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from jose import JWTError, ExpiredSignatureError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.core.errors.exceptions import CustomHTTPException, DatabaseException, JWTException, TokenExpiredException
import logging

logger = logging.getLogger(__name__)


async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    logger.warning(f"Custom error: {exc.error_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.detail,
                "code": exc.error_code
            }
        },
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Обработка стандартных HTTP ошибок"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"type": "HTTPException", "message": exc.detail}},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Ошибки валидации Pydantic"""
    return JSONResponse(
        status_code=422,
        content={"error": {"type": "ValidationError", "details": exc.errors()}},
    )

async def jwt_error_handler(request: Request, exc: JWTError):
    """Обработка JWT ошибок"""
    logger.warning(f"JWT error: {exc}")
    raise JWTException(str(exc))

async def jwt_expired_handler(request: Request, exc: ExpiredSignatureError):
    """Обработка просроченного токена"""
    raise TokenExpiredException()

async def sqlalchemy_integrity_handler(request: Request, exc: IntegrityError):
    """Обработка ошибок целостности данных"""
    logger.error(f"Integrity error: {exc}")
    raise DatabaseException("Integrity constraint violated")

async def sqlalchemy_general_handler(request: Request, exc: SQLAlchemyError):
    """Обработка общих ошибок SQLAlchemy"""
    logger.error(f"SQLAlchemy error: {exc}")
    raise DatabaseException("Internal database error")

async def global_exception_handler(request: Request, exc: Exception):
    """Обработка неожиданных исключений"""
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": exc.__class__.__name__,
                "message": "Internal server error",
                "path": str(request.url.path),
            }
        },
    )

def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(JWTError, jwt_error_handler)
    app.add_exception_handler(ExpiredSignatureError, jwt_expired_handler)
    app.add_exception_handler(IntegrityError, sqlalchemy_integrity_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_general_handler)
    app.add_exception_handler(Exception, global_exception_handler)
