from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import search, recommend, describe
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
    try:
        from app.utils.summarizer import summarizer
        summarizer_status = "loaded" if summarizer else "unavailable (using fallback)"
    except:
        summarizer_status = "error"
    
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


