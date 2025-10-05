def recommend_similar(data, query):
    """
    Placeholder for ML-based similarity.
    Currently uses keyword matching.
    """
    q = query.lower()
    results = []
    for d in data:
        score = 0
        if q in d["title"].lower():
            score += 2
        if q in d.get("description", "").lower():
            score += 1
        if any(q in kw.lower() for kw in d.get("keywords", [])):
            score += 1
        if score > 0:
            results.append((score, d))
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results[:5]]

