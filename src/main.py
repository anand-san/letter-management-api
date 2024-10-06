import os
import firebase_admin

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from src.api.schema import schema
from src.middlewares.auth import AuthMiddleware
from src.context.get_context import get_context
from src.utils.logging import init_sentry
from src.db.postgres.migrate import migrate_pg

load_dotenv()
init_sentry()
app = FastAPI()

firebase_admin.initialize_app()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)
# Generic exception handler


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    error_message = "An internal server error occurred."
    status_code = 500
    if (isinstance(exc, HTTPException)):
        error_message = exc.detail
        status_code = exc.status_code
    return JSONResponse(
        status_code=status_code,
        content={"data": error_message},
    )

graphql_app = GraphQLRouter(schema, context_getter=get_context, graphiql=False)
app.include_router(graphql_app, prefix="/graphql")


@app.on_event("startup")
async def startup():
    await migrate_pg()


def start():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)


if __name__ == "__main__":
    start()
