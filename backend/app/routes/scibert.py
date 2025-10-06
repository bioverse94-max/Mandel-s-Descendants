from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os

import httpx

# Add scibert-master to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'scibert-master')))

# try:
#     from allennlp.models.archival import load_archive
#     from allennlp.predictors import Predictor
# except ImportError:
#     raise RuntimeError("SciBERT dependencies are not installed. Please run 'pip install allennlp==0.9.0'")

router = APIRouter()

class NerRequest(BaseModel):
    text: str

SCIBERT_URL = os.getenv("SCIBERT_URL", "http://localhost:8080")

@router.post("/scibert/ner", tags=["scibert"])
async def ner(request: NerRequest):
    """
    Perform Named Entity Recognition using SciBERT.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{SCIBERT_URL}/ner", json={"text": request.text})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error connecting to SciBERT service: {e}")

