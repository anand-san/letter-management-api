from auth.clerk_auth import ClerkAuth
from fastapi import Request


async def get_context(request: Request):
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        is_authenticated = False
    else:
        clerk = ClerkAuth()
        key = clerk.get_jwks()
        user_id = clerk.validate_bearer_token(auth_token, key)
        user = clerk.get_user(user_id)
        is_authenticated = "errors" not in user
    return {"user": user, "is_authenticated": is_authenticated}
