from cachetools import TTLCache, cached
from typing import Callable, Any, Optional
import hashlib
import time


class CacheManager:
    _instance = None
    caches = {}  # Словарь для хранения кешей разных функций

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_cache(cls, func_name: str) -> Optional[TTLCache]:
        return cls.caches.get(func_name)

    @classmethod
    def invalidate_cache(cls, func_name: str = None):
        """Очистка кеша для конкретной функции или всего кеша."""
        if func_name:
            if func_name in cls.caches:
                cls.caches[func_name].clear()
        else:
            for cache in cls.caches.values():
                cache.clear()


def api_cache(ttl: int = 3600) -> Callable:
    """Декоратор с возможностью инвалидации."""

    def decorator(func: Callable) -> Callable:
        cache = TTLCache(maxsize=100, ttl=ttl)
        CacheManager.caches[func.__name__] = cache

        @cached(cache, key=lambda *args, **kwargs: _generate_key(args, kwargs))
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs)

        wrapper.cache = cache  # Добавляем ссылку на кеш
        return wrapper

    return decorator


def _generate_key(args: tuple, kwargs: dict) -> str:
    """Генерация ключа с исключением незначимых параметров."""
    filtered_kwargs = {k: v for k, v in kwargs.items() if k not in ['cache']}
    key_data = str(args[1:]) + str(sorted(filtered_kwargs.items()))
    return hashlib.sha256(key_data.encode()).hexdigest()
