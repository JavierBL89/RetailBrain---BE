import redis
import os
import json


# ----------------------------------------------------------------
# Redis connection
# ----------------------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # default to service name
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

rdb = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)



########## persist session/states in Redis ##########

SESSION_TTL = 3600  # 1 hour

def save_session(session_id: str, data: dict):
    """Store session data in Redis."""
    rdb.setex(f"session:{session_id}", SESSION_TTL, json.dumps(data))

def load_session(session_id: str) -> dict | None:
    """Load session data if present."""
    raw = rdb.get(f"session:{session_id}")
    return json.loads(raw) if raw else None

def delete_session(session_id: str):
    """Delete a session explicitly."""
    rdb.delete(f"session:{session_id}")

