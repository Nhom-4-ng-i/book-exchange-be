from fastapi import APIRouter
from app.api.routes import search, auth

api_router = APIRouter(prefix="/api")
api_router.include_router(search.router)
api_router.include_router(auth.router)