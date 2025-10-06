from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Model Configuration
    MODEL_MAX_LENGTH: int = 512
    BATCH_SIZE: int = 32
    NUM_WORKERS: int = 2
    USE_CUDA: bool = True
    
    # Optimization Settings
    ENABLE_TORCH_SCRIPT: bool = True
    QUANTIZATION: bool = True
    HALF_PRECISION: bool = True
    
    # Cache Settings
    CACHE_SIZE: int = 1000
    CACHE_TTL: int = 3600  # 1 hour
    
    # Redis Configuration
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()