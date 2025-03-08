import redis
import json

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def set_cache(key: str, value: dict, ttl: int = 86400):
    redis_client.setex(key, ttl, json.dumps(value))
    
def get_cache(key: str):
    data = redis_client.get(key)
    return json.loads(data) if data else None

def clear_cache(key: str):
    redis_client.delete(key)