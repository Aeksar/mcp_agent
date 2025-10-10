from redis.asyncio.client import Redis
from app.configs.settings import settings


def get_redis():
    return Redis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)