from fastapi import APIRouter
from app.crud.profiles import get_profile, insert_profile, update_profile, delete_profile
from app.schemas.profiles import InsertProfileRequest, UpdateProfileRequest


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{user_id}")
async def get_profile_route(user_id: str):
    response = get_profile(user_id=user_id)
    return {
        "user_id": response["user_id"],
        "name": response["name"],
        "email": response["email"],
    }


@router.post("/")
async def insert_profile_route(profile_request: InsertProfileRequest):
    insert_profile(
        user_id=profile_request.user_id,
        name=profile_request.name,
        email=profile_request.email
    )


@router.put("/{user_id}")
async def update_profile_route(user_id: str, profile_request: UpdateProfileRequest):
    update_profile(
        user_id=user_id,
        name=profile_request.name,
        email=profile_request.email
    )


@router.delete("/{user_id}")
async def delete_profile_route(user_id: str):
    delete_profile(user_id=user_id)
