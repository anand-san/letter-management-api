from fastapi import Request
from typing import Any, TypedDict


class ContextType(TypedDict):
    user: Any | None
    is_authenticated: bool


async def get_context(request: Request) -> ContextType:
    user = getattr(request.state, "user", None)
    return {"user": user, "is_authenticated": user is not None}
