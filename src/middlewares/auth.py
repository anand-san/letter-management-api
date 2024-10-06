import json

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from firebase_admin.auth import verify_id_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.db.postgres.postgres import get_pg_connection


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.bearer_scheme = HTTPBearer(auto_error=False)

    async def dispatch(self, request: Request, call_next):
        token: HTTPAuthorizationCredentials | None = await self.bearer_scheme(request)

        if token:
            credentials = token.credentials
            try:
                request.state.user = verify_id_token(credentials)
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Auth Header Missing",
                headers={"WWW-Authenticate": "Bearer"},
            )
        response = await call_next(request)
        return response

    async def user_exists_in_db(self, user):
        conn = await get_pg_connection()

        try:
            # Check if user exists in the database
            existing_user = await conn.fetchrow('''
                    SELECT * FROM users WHERE clerk_user_id = $1
                ''', user["id"])
            return True if existing_user else False
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await conn.close()

    async def add_user_to_db(self, user):
        conn = await get_pg_connection()

        try:
            await conn.execute('''
                    INSERT INTO users (clerk_user_id, clerk_metadata, created_at, updated_at)
                    VALUES ($1, $2, NOW(), NOW())
                ''', user["id"], json.dumps(user))
            pass
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await conn.close()
