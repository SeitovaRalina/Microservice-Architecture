from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import auth as auth_routes
from src.routes import articles as articles_routes
from src.routes import comments as comments_routes

app = FastAPI(title="Simple Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router_prefix = "/api"

app.include_router(auth_routes.router, prefix="/api")
app.include_router(articles_routes.router, prefix="/api")
app.include_router(comments_routes.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
