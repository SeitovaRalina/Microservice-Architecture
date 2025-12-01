from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth as auth_routes
from src.core.errors.handlers import setup_exception_handlers

app = FastAPI(
    title="Users Service API",
    version="1.0.0",
    description="Отдельный микросервис для управления пользователями",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    root_path="/api/users"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_exception_handlers(app)
app.include_router(auth_routes.router)

@app.get("/health", tags=["health"],
         summary="Проверить состояние сервиса", description="Возвращает статус работы сервиса.")
def health():
    return {"status": "ok"}