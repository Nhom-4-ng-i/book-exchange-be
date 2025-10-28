from fastapi import APIRouter, HTTPException
from app.schemas.auth import SignUpRequest, SignInRequest, SignInResponse
from app.services.supabase import get_supabase


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-up")
async def sign_up(auth_request: SignUpRequest):
    supabase = get_supabase()
    email = auth_request.email
    password = auth_request.password
    name = auth_request.name

    try:
        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    user_id = getattr(response.user, "id", None)
    if user_id:
        supabase.table("profiles").insert({"id": user_id, "email": email, "name": name}).execute()


@router.post("/sign-in", response_model=SignInResponse)
async def sign_in(auth_request: SignInRequest):
    supabase = get_supabase()
    email = auth_request.email
    password = auth_request.password

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )
        
        access_token = getattr(response.session, "access_token", None)
        id = getattr(response.user, "id", None)
        user_profile = supabase.table("profiles").select("*").eq("id", id).single().execute()
        name = user_profile.data.get("name")
        role = user_profile.data.get("role")

        return SignInResponse(
            access_token=access_token,
            id=id,
            email=email,
            name=name,
            role=role
        )

    except:
        raise HTTPException(status_code=401, detail="Invalid email or password")