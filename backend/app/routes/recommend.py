from fastapi import APIRouter, Query, HTTPException
from app.database import DATA

router = APIRouter(prefix="/recommend", tags=["Recommend"])

@router.get("/")
def recommend(q: str = Query(
    ..., 
    description="Keyword or dataset ID",
    min_length=1,
    max_length=200,
    pattern="^[a-zA-Z0-9\\s\\-_]+$"
)):
    """
    Recommend similar datasets based on keyword overlap.
    """
    q = q.strip().lower()
    
    if not q:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    results = []
    for d in DATA:
        score = 0
        if q in d["id"].lower():
            score += 3
        if q in d["title"].lower():
            score += 2
        if q in d.get("description", "").lower():
            score += 1
        if any(q in kw.lower() for kw in d.get("keywords", [])):
            score += 1
        if score > 0:
            results.append((score, d))

    results.sort(key=lambda x: x[0], reverse=True)
    
    if not results:
        return {
            "query": q, 
            "message": "No recommendations found",
            "results": []
        }
    
    return {
        "query": q, 
        "results": [r[1] for r in results[:5]]
    }

