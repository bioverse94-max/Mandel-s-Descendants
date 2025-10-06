from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.routes import search, recommend, describe, scibert
from app.database import DATA
from app.config import settings
from app.monitoring import setup_monitoring, setup_logging, setup_elasticsearch
import sys
from typing import Callable
import time
import asyncio
from cachetools import TTLCache
import logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize cache
response_cache = TTLCache(maxsize=100, ttl=settings.CACHE_TTL)

# Rate limiting middleware
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        calls_per_second: int = settings.RATE_LIMIT_PER_SECOND
    ):
        super().__init__(app)
        self.calls_per_second = calls_per_second
        self.request_timestamps = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host
        now = time.time()
        
        # Clean old timestamps
        self.request_timestamps = {ip: ts for ip, ts in self.request_timestamps.items() 
                                 if now - ts[-1] < 1}
        
        # Get timestamps for this IP
        timestamps = self.request_timestamps.get(client_ip, [])
        
        # Remove timestamps older than 1 second
        timestamps = [ts for ts in timestamps if now - ts < 1]
        
        if len(timestamps) >= self.calls_per_second:
            return Response("Too many requests", status_code=429)
        
        timestamps.append(now)
        self.request_timestamps[client_ip] = timestamps
        
        response = await call_next(request)
        return response

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0",
    description="Backend for NASA BioVerse project 🚀",
)

# Add Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add rate limiting
app.add_middleware(RateLimitMiddleware)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up monitoring
setup_monitoring(app)

# Initialize Elasticsearch
es_client = setup_elasticsearch()

# Register all route modules
app.include_router(search.router)
app.include_router(recommend.router)
app.include_router(describe.router)
app.include_router(scibert.router)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    log_data = {
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "process_time": process_time,
        "client_ip": request.client.host
    }
    
    logger.info("Request processed", extra=log_data)
    return response


@app.get("/")
def root():
    return {
        "message": "BioVerse API is live 🚀",
        "version": "1.0",
        "endpoints": ["/search", "/recommend", "/describe", "/health"],
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify API status and data availability.
    """
    # Check summarizer availability: summarize_text uses HF API when token provided,
    # otherwise it falls back to a truncation behavior. We report availability accordingly.
    try:
        from app.utils.summarizer import summarize_text
        # If function exists, report loaded (but actual HF token may be missing)
        summarizer_status = "available" if callable(summarize_text) else "unavailable"
    except Exception:
        summarizer_status = "unavailable"
    
    return {
        "status": "healthy",
        "api_version": "1.0",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "datasets_loaded": len(DATA),
        "summarizer_status": summarizer_status,
        "endpoints": {
            "search": "/search?q=<keyword>",
            "recommend": "/recommend?q=<keyword>",
            "describe": "/describe?q=<keyword>"
        }
    }


