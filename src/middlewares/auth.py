from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from firebase_admin.auth import verify_id_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.bearer_scheme = HTTPBearer(auto_error=False)

    async def dispatch(self, request: Request, call_next):
        try:
            token: HTTPAuthorizationCredentials | None = await self.bearer_scheme(request)

            if token:
                credentials = token.credentials
                try:
                    request.state.user = verify_id_token(credentials)
                except Exception:
                    raise
            else:
                raise
            response = await call_next(request)
            return response
        except Exception as e:
            print(f"Auth Error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"data": None, "errors": [{"message": "Unauthorized"}]},
            )
