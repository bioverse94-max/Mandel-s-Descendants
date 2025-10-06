from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "BioVerse API"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list[str] = ["*"]  # In production, replace with specific origins
    
    # Cache Configuration
    CACHE_TTL: int = 3600  # Cache time to live in seconds
    
    # Rate Limiting
    RATE_LIMIT_PER_SECOND: int = 10
    
    # SciBERT Service
    SCIBERT_URL: str = "http://scibert:8080"
    
    # Model Configuration
    MODEL_BATCH_SIZE: int = 32
    MODEL_MAX_LENGTH: int = 512
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()pip