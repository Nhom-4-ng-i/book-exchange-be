from fastapi import APIRouter, HTTPException
from app.schemas.auth import SignUpRequest, SignInRequest, SignInResponse
from app.crud.profiles import create_profile, get_profile
from app.crud.auth import supabase_sign_up, supabase_sign_in

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-up")
async def sign_up(auth_request: SignUpRequest):
    email = auth_request.email
    name = auth_request.name
    
    try:
        response = supabase_sign_up(email=email)

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    user_id = getattr(response.user, "id", None)
    if user_id:
        create_profile(user_id=user_id, name=name, email=email)


@router.post("/sign-in", response_model=SignInResponse)
async def sign_in(auth_request: SignInRequest):
    email = auth_request.email

    try:
        response = supabase_sign_in(email=email)
        
        access_token = getattr(response.session, "access_token", None)
        user_id = getattr(response.user, "id", None)
        user_profile = get_profile(user_id=user_id)
        name = user_profile.data.get("name")
        role = user_profile.data.get("role")

        return SignInResponse(
            access_token=access_token,
            id=user_id,
            email=email,
            name=name,
            role=role
        )

    except:
        raise HTTPException(status_code=401, detail="Invalid email or password")