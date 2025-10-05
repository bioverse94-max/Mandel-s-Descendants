from fastapi import APIRouter, Query, HTTPException
from app.database import DATA
from app.utils.summarizer import summarize_text

router = APIRouter(prefix="/describe", tags=["Describe"])

@router.get("/")
def describe(q: str = Query(
    ..., 
    description="Topic or keyword to summarize",
    min_length=1,
    max_length=200,
    pattern="^[a-zA-Z0-9\\s\\-_]+$"
)):
    """
    Combine descriptions of top-matching datasets and return AI-generated summary.
    """
    q = q.strip().lower()
    
    if not q:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    matched = [
        d for d in DATA
        if q in d["title"].lower()
        or q in d.get("description", "").lower()
        or any(q in kw.lower() for kw in d.get("keywords", []))
    ]

    if not matched:
        raise HTTPException(
            status_code=404, 
            detail=f"No datasets found matching '{q}'"
        )

    # Combine top few descriptions with null checks
    descriptions = []
    for d in matched[:5]:
        desc = d.get("description")
        if desc and desc.strip():  # Null check
            descriptions.append(desc.strip())
    
    if not descriptions:
        return {
            "query": q,
            "summary": "Datasets found but no descriptions available.",
            "sources": matched[:5]
        }
    
    combined_text = " ".join(descriptions)

    # Generate summary using AI
    summary = summarize_text(combined_text)

    return {
        "query": q,
        "summary": summary,
        "sources": matched[:5],
        "source_count": len(matched)
    }
