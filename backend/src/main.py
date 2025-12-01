from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import articles as articles_routes
from src.routers import comments as comments_routes
from src.routers import internal as internal_routes
from src.core.errors.handlers import setup_exception_handlers

app = FastAPI(
    title="Simple Blog API",
    version="1.0.0",
    description="API для управления статьями и комментариями в блог-платформе.",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_exception_handlers(app)

app.include_router(articles_routes.router)
app.include_router(comments_routes.router)
app.include_router(internal_routes.router, include_in_schema=False)

@app.get("/health", tags=["health"],
         summary="Проверить состояние сервиса", description="Возвращает статус работы сервиса.")
def health():
    return {"status": "ok"}