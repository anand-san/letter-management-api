import asyncpg

from utils.get_env import get_env_var


async def get_pg_connection():
    POSTGRES_USER = get_env_var("POSTGRES_USER")
    POSTGRES_PASSWORD = get_env_var("POSTGRES_PASSWORD")
    POSTGRES_DB = get_env_var("POSTGRES_DB")
    POSTGRES_HOST = get_env_var("POSTGRES_HOST")

    return await asyncpg.connect(user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                 database=POSTGRES_DB, host=POSTGRES_HOST)
