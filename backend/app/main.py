from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import search, recommend, describe, scibert
from app.database import DATA
import sys
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="BioVerse API",
    version="1.0",
    description="Backend for NASA BioVerse project 🚀",
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Update this when frontend is ready
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all route modules
app.include_router(search.router)
app.include_router(recommend.router)
app.include_router(describe.router)
app.include_router(scibert.router)


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


