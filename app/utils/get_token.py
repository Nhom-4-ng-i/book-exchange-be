from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.supabase import get_supabase

security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Dependency to extract user_id from Bearer token using Supabase auth.

    Expects header: Authorization: Bearer <access_token>
    Returns the user_id string or raises 401.
    """
    token = credentials.credentials
    print("token", token)
    supabase = get_supabase()

    # Try to get user info from Supabase using the access token
    try:
        # supabase client provides auth.get_user(token) in newer versions
        user_resp = None
        try:
            user_resp = supabase.auth.get_user(token)
        except Exception:
            # fallback: some clients expose get_user via auth.api
            try:
                user_resp = supabase.auth.api.get_user(token)
            except Exception:
                user_resp = None

        if not user_resp:
            raise HTTPException(status_code=401, detail="Invalid token")

        # user_resp may be object with 'user' attr or a dict with 'data'
        user = None
        if hasattr(user_resp, 'user'):
            user = getattr(user_resp, 'user')
        elif isinstance(user_resp, dict) and 'data' in user_resp:
            user = user_resp['data']
        else:
            user = user_resp

        user_id = None
        if isinstance(user, dict):
            user_id = user.get('id') or user.get('user_id')
        else:
            # try attribute
            user_id = getattr(user, 'id', None) or getattr(
                user, 'user_id', None)

        if not user_id:
            raise HTTPException(
                status_code=401, detail="Unable to resolve user from token")

        return user_id

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
