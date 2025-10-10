from langchain.memory import RedisChatMessageHistory
from app.configs.settings import settings

def get_redis_memory(session_id: str):
    return RedisChatMessageHistory(
        url=settings.redis_url,
        session_id=session_id,
    )