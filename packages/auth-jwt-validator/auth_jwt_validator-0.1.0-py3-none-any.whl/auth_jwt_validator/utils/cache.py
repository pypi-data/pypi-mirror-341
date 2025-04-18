# jwt_auth_validator/utils/cache.py

import time
from typing import Any, Dict

class Cache:
    def __init__(self, ttl: int):
        self.ttl = ttl  # زمان انقضا کش به ثانیه
        self.cache: Dict[str, Dict[str, Any]] = {}

    def _is_expired(self, timestamp: float) -> bool:
        """بررسی اینکه آیا داده‌ها منقضی شدن یا نه"""
        return (time.time() - timestamp) > self.ttl

    def get(self, key: str) -> Any:
        """دریافت داده از کش"""
        cache_item = self.cache.get(key)
        
        if cache_item and not self._is_expired(cache_item["timestamp"]):
            return cache_item["data"]
        
        return None

    def set(self, key: str, data: Any):
        """ذخیره داده در کش"""
        self.cache[key] = {
            "data": data,
            "timestamp": time.time()  # زمان ذخیره‌سازی داده
        }

    def clear(self, key: str):
        """حذف داده از کش"""
        if key in self.cache:
            del self.cache[key]

    def clear_all(self):
        """حذف تمام داده‌ها از کش"""
        self.cache.clear()