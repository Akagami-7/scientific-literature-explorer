import redis
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class HistoryManager:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379"),
            decode_responses=True
        )

    def _get_user_key(self, user_id, category):
        return f"history:{user_id}:{category}"

    def add_search(self, user_id, query):
        key = self._get_user_key(user_id, "search")
        data = {
            "query": query,
            "timestamp": datetime.now().isoformat()
        }
        self.redis_client.lpush(key, json.dumps(data))
        self.redis_client.ltrim(key, 0, 49) # Keep last 50 searches

    def add_upload(self, user_id, filename):
        key = self._get_user_key(user_id, "upload")
        data = {
            "filename": filename,
            "timestamp": datetime.now().isoformat()
        }
        self.redis_client.lpush(key, json.dumps(data))
        self.redis_client.ltrim(key, 0, 19) # Keep last 20 uploads

    def get_history(self, user_id, category):
        key = self._get_user_key(user_id, category)
        items = self.redis_client.lrange(key, 0, -1)
        return [json.loads(item) for item in items]
