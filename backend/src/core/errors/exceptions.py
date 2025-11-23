from fastapi import HTTPException, status

class CustomHTTPException(HTTPException):
    """Базовое исключение приложения с дополнительным кодом ошибки"""
    def __init__(self, status_code: int, detail: str, error_code: str = "ERROR"):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

class NotFoundException(CustomHTTPException):
    """Ресурс не найден"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status.HTTP_404_NOT_FOUND, detail, "NOT_FOUND")


class UnauthorizedException(CustomHTTPException):
    """Ошибка аутентификации"""
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, "UNAUTHORIZED")


class ForbiddenException(CustomHTTPException):
    """Нет доступа к ресурсу"""
    def __init__(self, detail: str = "Access denied"):
        super().__init__(status.HTTP_403_FORBIDDEN, detail, "FORBIDDEN")


class ConflictException(CustomHTTPException):
    """Конфликт данных (например, при уникальных полях)"""
    def __init__(self, detail: str = "Conflict with existing data"):
        super().__init__(status.HTTP_409_CONFLICT, detail, "CONFLICT")


class ValidationException(CustomHTTPException):
    """Ошибка валидации входных данных"""
    def __init__(self, detail: str = "Invalid input data"):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail, "VALIDATION_ERROR")


class DatabaseException(CustomHTTPException):
    """Ошибка работы с базой данных"""
    def __init__(self, detail: str = "Database error"):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail, "DB_ERROR")


class TokenExpiredException(CustomHTTPException):
    """Истёк срок действия JWT-токена"""
    def __init__(self, detail: str = "Token expired"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, "TOKEN_EXPIRED")


class JWTException(CustomHTTPException):
    """Ошибка при валидации JWT"""
    def __init__(self, detail: str = "Invalid JWT token"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, "INVALID_TOKEN")
