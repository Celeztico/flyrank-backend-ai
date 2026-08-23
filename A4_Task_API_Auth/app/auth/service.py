from app.auth.client import supabase

def signup_user(email: str, password: str):
    return supabase.auth.sign_up(
        {
            "email": email,
            "password": password,
        }
    )

def login_user(email: str, password: str):
    return supabase.auth.sign_in_with_password(
        {
            "email": email,
            "password": password,
        }
    )

def verify_access_token(access_token: str):
    return supabase.auth.get_user(access_token)

