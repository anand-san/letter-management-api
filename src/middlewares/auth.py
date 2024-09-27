import json
import jwt
import requests

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jwt.algorithms import RSAAlgorithm
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from src.utils.get_env import get_env_var
from src.db.postgres.postgres import get_pg_connection

JWKS_KEY_CACHE = {}


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.clerk = ClerkAuth()

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user_id = await self.verify_token(auth_header)

        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = self.clerk.get_user(user_id)

        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        self.add_user_to_db(user) if not await self.user_exists_in_db(user) else None

        request.state.user = user

        response = await call_next(request)
        return response

    async def verify_token(self, auth_header: str) -> str:
        key = self.clerk.get_jwks()
        return self.clerk.validate_bearer_token(auth_header, key)

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


class ClerkAuth:
    def __init__(self):
        self.api_url = get_env_var('CLERK_API_URL')
        self.jwks_url = get_env_var('CLERK_JWKS_URL')
        self.secret_key = get_env_var('CLERK_SECRET_KEY')

    def get_user(self, user_id: str):
        try:
            api_path = f"{self.api_url}/users/{user_id}"
            return requests.get(
                api_path,
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.secret_key}",
                },
            ).json()
        except Exception:
            raise Exception("Error fetching User details")

    def get_jwks(self) -> RSAPublicKey:
        try:
            if "key" in JWKS_KEY_CACHE:
                print("Using cached key")
                return JWKS_KEY_CACHE["key"]

            print("Fetching new key")
            jwks = requests.get(
                self.jwks_url,
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.secret_key}",
                },
            ).json()

            key = RSAAlgorithm.from_jwk(jwks["keys"][0])
            JWKS_KEY_CACHE["key"] = key
            return key  # type: ignore
        except Exception as e:
            raise Exception(f"Error fetching Auth Signing Key: {str(e)}")

    def validate_bearer_token(self, auth_header: str, public_key: RSAPublicKey) -> str:
        try:
            try:
                token = auth_header.split(" ")[1]
            except (AttributeError, KeyError):
                raise Exception("No authentication token provided")

            try:
                payload = jwt.decode(token, key=public_key, algorithms=[
                    'RS256'], options={"verify_signature": False})
            except jwt.ExpiredSignatureError:
                raise Exception("Token has expired.")
            except jwt.DecodeError:
                raise Exception("Token decode error.")
            except jwt.InvalidTokenError:
                raise Exception("Invalid token.")
            except Exception as e:
                raise Exception(str(e))
            user_id = payload.get("sub")
            return user_id
        except Exception as e:
            raise Exception(f"Error Validating User: {str(e)}")
