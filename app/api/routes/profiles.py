from fastapi import APIRouter, Depends
from app.crud.profiles import get_profile, update_profile
from app.schemas.profiles import UpdateProfileRequest
from app.utils.get_token import get_current_user_id


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{user_id}")
async def get_profile_route(user_id: str, _: str = Depends(get_current_user_id)):
    response = get_profile(user_id=user_id)
    return {
        "name": response["name"],
        "email": response["email"],
        "avatar_url": response["avatar_url"],
    }


@router.put("/{user_id}")
async def update_profile_route(user_id: str, profile_request: UpdateProfileRequest, _: str = Depends(get_current_user_id)):
    update_profile(
        user_id=user_id,
        name=profile_request.name,
        email=profile_request.email
    )
