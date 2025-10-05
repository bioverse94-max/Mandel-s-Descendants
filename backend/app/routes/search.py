from fastapi import APIRouter, Query, HTTPException
from app.database import DATA
from app.models import Dataset

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/", response_model=dict)
def search(q: str = Query(
    ..., 
    description="Search keyword",
    min_length=1,
    max_length=200,
    pattern="^[a-zA-Z0-9\\s\\-_]+$"  # Only alphanumeric, spaces, hyphens, underscores
)):
    """
    Keyword-based search through title, description, and keywords.
    """
    q = q.strip().lower()
    
    if not q:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    results = [
        d for d in DATA
        if q in d["title"].lower()
        or q in d.get("description", "").lower()
        or any(q in kw.lower() for kw in d.get("keywords", []))
    ]
    
    return {
        "query": q,
        "count": len(results),
        "results": results[:25]
    }

