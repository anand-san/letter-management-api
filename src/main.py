from src.utils.logging import init_sentry
from src.db.postgres.migrate import migrate_pg
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from src.api.schema import schema
from src.auth.middleware import get_context
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()
init_sentry()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generic exception handler


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred."},
    )

graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")


@app.on_event("startup")
async def startup():
    await migrate_pg()


def start():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)


if __name__ == "__main__":
    start()
