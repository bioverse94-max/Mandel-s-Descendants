from functools import wraps
from typing import Callable, Optional
import hashlib
import json
from redis import Redis
from app.config import settings

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)

def cache_response(
    prefix: str,
    ttl: int = 3600,
    key_generator: Optional[Callable] = None
):
    """
    Decorator to cache endpoint responses in Redis
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            if key_generator:
                cache_key = f"{prefix}:{key_generator(*args, **kwargs)}"
            else:
                # Default key generation using args and kwargs
                key_parts = [prefix]
                key_parts.extend(str(arg) for arg in args)
                key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
                cache_key = ":".join(key_parts)
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # If not in cache, execute function
            result = await func(*args, **kwargs)
            
            # Cache the result
            redis_client.setex(
                cache_key,
                ttl,
                json.dumps(result)
            )
            
            return result
        return wrapper
    return decorator

def generate_search_key(query: str) -> str:
    """Generate a cache key for search queries"""
    return hashlib.md5(query.lower().encode()).hexdigest()

def generate_recommend_key(query: str) -> str:
    """Generate a cache key for recommendation queries"""
    return hashlib.md5(f"rec:{query.lower()}".encode()).hexdigest()

# Specialized caching strategies
def cache_search_results(ttl: int = 3600):
    """Cache decorator specifically for search results"""
    return cache_response(
        prefix="search",
        ttl=ttl,
        key_generator=generate_search_key
    )

def cache_recommendations(ttl: int = 7200):
    """Cache decorator specifically for recommendations"""
    return cache_response(
        prefix="recommend",
        ttl=ttl,
        key_generator=generate_recommend_key
    )

def cache_descriptions(ttl: int = 86400):
    """Cache decorator specifically for descriptions"""
    return cache_response(
        prefix="describe",
        ttl=ttl
    )