# import os
# import redis.asyncio as redis

# redis_client = None


# async def init_redis():
#     global redis_client
#     redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
#     redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)


# def get_redis_client():
#     return redis_client
