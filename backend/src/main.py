from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth as auth_routes
from src.routers import articles as articles_routes
from src.routers import comments as comments_routes
from src.core.errors.handlers import setup_exception_handlers

app = FastAPI(title="Simple Blog API", version="1.0.0", description="API для управления пользователями, статьями и комментариями в блог-платформе.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_exception_handlers(app)

app.include_router(auth_routes.router)
app.include_router(articles_routes.router)
app.include_router(comments_routes.router)

@app.get("/health", tags=["health"],
         summary="Проверить состояние сервиса", description="Возвращает статус работы сервиса.")
def health():
    return {"status": "ok"}