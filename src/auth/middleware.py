import json
from src.auth.clerk_auth import ClerkAuth
from src.db.postgres.postgres import get_pg_connection
from fastapi import Request


async def get_context(request: Request):
    try:
        auth_token = request.headers.get("Authorization")
        user = {}
        if not auth_token:
            is_authenticated = False
        else:
            clerk = ClerkAuth()
            key = clerk.get_jwks()
            user_id = clerk.validate_bearer_token(auth_token, key)
            user = clerk.get_user(user_id)
            is_authenticated = "errors" not in user
            await check_if_user_exists_in_db(user)
        return {"user": user, "is_authenticated": is_authenticated}
    except Exception as e:
        raise Exception(str(e))


async def check_if_user_exists_in_db(user):
    try:
        # Check if user exists in the database
        conn = await get_pg_connection()
        existing_user = await conn.fetchrow('''
                SELECT * FROM users WHERE clerk_user_id = $1
            ''', user["id"])
        if not existing_user:
            await conn.execute('''
                INSERT INTO users (clerk_user_id, clerk_metadata, created_at, updated_at)
                VALUES ($1, $2, NOW(), NOW())
            ''', user["id"], json.dumps(user))
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await conn.close()
