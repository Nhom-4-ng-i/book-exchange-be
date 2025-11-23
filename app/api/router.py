from fastapi import APIRouter
from app.api.routes import posts, auth, profiles, courses, locations, orders

api_router = APIRouter(prefix="/api")
api_router.include_router(posts.router)
api_router.include_router(auth.router)
api_router.include_router(profiles.router)
api_router.include_router(courses.router)
api_router.include_router(locations.router)
api_router.include_router(orders.router)
