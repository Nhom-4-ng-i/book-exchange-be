from fastapi import APIRouter
from app.api.routes import posts, auth

api_router = APIRouter(prefix="/api")
api_router.include_router(posts.router)
api_router.include_router(auth.router)