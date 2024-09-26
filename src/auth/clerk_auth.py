import jwt
import requests
from jwt.algorithms import RSAAlgorithm
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from src.utils.get_env import get_env_var

JWKS_KEY_CACHE = {}


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
