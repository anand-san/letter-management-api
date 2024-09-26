from src.db.postgres.postgres import get_pg_connection
from src.db.postgres.schema import DOCUMENTS_INDEXES, DOCUMENTS_TABLE, ENABLE_UUID_EXTENSION, USER_TABLE


async def migrate_pg():
    conn = await get_pg_connection()
    try:
        await conn.execute(ENABLE_UUID_EXTENSION)
        await conn.execute(USER_TABLE)
        await conn.execute(DOCUMENTS_TABLE)
        await conn.execute(DOCUMENTS_INDEXES)

    except Exception as e:
        print(f"Migration Failed {e}")
    finally:
        await conn.close()
