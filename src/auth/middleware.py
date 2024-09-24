from fastapi import Request


async def get_context(request: Request):
    # This is a placeholder. Implement your actual authentication logic here.
    is_authenticated = "Authorization" in request.headers

    return {"is_authenticated": not is_authenticated}
