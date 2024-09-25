from db.postgres.postgres import get_pg_connection
from db.postgres.schema import DOCUMENTS_INDEXES, DOCUMENTS_TABLE, ENABLE_UUID_EXTENSION, USER_TABLE


async def migrate_pg():
    try:
        conn = await get_pg_connection()
        await conn.execute(ENABLE_UUID_EXTENSION)
        await conn.execute(USER_TABLE)
        await conn.execute(DOCUMENTS_TABLE)
        await conn.execute(DOCUMENTS_INDEXES)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await conn.close()
