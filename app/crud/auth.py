from app.services.supabase import get_supabase


def sign_up(email: str, password: str = "password"):
    supabase = get_supabase()
    return supabase.auth.sign_up(
        {
            "email": email,
            "password": password
        }
    )


def sign_in(email: str, password: str = "password"):
    supabase = get_supabase()
    return supabase.auth.sign_in_with_password(
        {
            "email": email,
            "password": password
        }
    )
    
def sign_out():
    supabase = get_supabase()
    supabase.auth.sign_out()
        
def update_phone(phone: str):
    supabase = get_supabase()
    supabase.auth.update_user({
        "phone": phone
    })
    
def send_phone_otp(phone: str):
    supabase = get_supabase()
    supabase.auth.sign_in_with_otp({
        "phone": phone
    })

def verify_phone_otp(phone: str, token: str):
    supabase = get_supabase()
    return supabase.auth.verify_otp({
        "phone": phone,
        "token": token,
        "type": "sms"
    })