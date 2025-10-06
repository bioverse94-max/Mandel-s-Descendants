from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
from typing import List, Dict, Any
import redis
from functools import lru_cache
import json
import asyncio
from config import settings

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)

# Model initialization
@lru_cache()
def get_model():
    model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased')
    
    if settings.ENABLE_TORCH_SCRIPT:
        model = torch.jit.script(model)
    
    if settings.HALF_PRECISION and torch.cuda.is_available():
        model = model.half()
    
    if settings.USE_CUDA and torch.cuda.is_available():
        model = model.cuda()
    
    if settings.QUANTIZATION:
        model = torch.quantization.quantize_dynamic(
            model, {nn.Linear}, dtype=torch.qint8
        )
    
    model.eval()
    return model

@lru_cache()
def get_tokenizer():
    return AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')


class InferenceRequest(BaseModel):
    text: str

class BatchInferenceRequest(BaseModel):
    texts: List[str]

@app.post("/predict")
async def predict(request: InferenceRequest):
    # Try to get from cache first
    cache_key = f"predict:{hash(request.text)}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)
    
    # Get model and tokenizer
    model = get_model()
    tokenizer = get_tokenizer()
    
    # Tokenize
    inputs = tokenizer(
        request.text,
        max_length=settings.MODEL_MAX_LENGTH,
        truncation=True,
        return_tensors="pt"
    )
    
    # Move to GPU if available
    if settings.USE_CUDA and torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}
    
    # Inference
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Process results
    embeddings = outputs.last_hidden_state.mean(dim=1)
    result = {
        "embeddings": embeddings[0].cpu().numpy().tolist()
    }
    
    # Cache the result
    redis_client.setex(
        cache_key,
        settings.CACHE_TTL,
        json.dumps(result)
    )
    
    return result

@app.post("/batch_predict")
async def batch_predict(request: BatchInferenceRequest):
    if len(request.texts) > settings.BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Batch size cannot exceed {settings.BATCH_SIZE}"
        )
    
    model = get_model()
    tokenizer = get_tokenizer()
    
    # Tokenize all texts
    inputs = tokenizer(
        request.texts,
        max_length=settings.MODEL_MAX_LENGTH,
        truncation=True,
        padding=True,
        return_tensors="pt"
    )
    
    if settings.USE_CUDA and torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}
    
    # Inference
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Process results
    embeddings = outputs.last_hidden_state.mean(dim=1)
    results = [emb.cpu().numpy().tolist() for emb in embeddings]
    
    return {"embeddings": results}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "cuda_available": torch.cuda.is_available(),
        "model_loaded": get_model() is not None,
        "redis_connected": redis_client.ping(),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8080,
        workers=settings.NUM_WORKERS
    )
