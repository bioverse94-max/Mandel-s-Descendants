from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import importlib

app = FastAPI()

# Try to import allennlp; if not available, expose a fallback endpoint
allennlp_available = False
try:
    allennlp = importlib.import_module('allennlp')
    from allennlp.models.archival import load_archive
    from allennlp.predictors import Predictor
    allennlp_available = True
except Exception:
    allennlp_available = False


MODEL_ARCHIVE_PATH = "results/your_model.tar.gz"
PREDICTOR_NAME = "text_classifier"

predictor = None
if allennlp_available:
    try:
        archive = load_archive(MODEL_ARCHIVE_PATH)
        predictor = Predictor.from_archive(archive, PREDICTOR_NAME)
    except Exception:
        predictor = None


class InferenceRequest(BaseModel):
    text: str


@app.post("/predict")
def predict(request: InferenceRequest):
    if not predictor:
        raise HTTPException(status_code=503, detail="Model not available")
    result = predictor.predict(request.text)
    return {"result": result}


@app.post("/ner")
def ner(request: InferenceRequest):
    # simple fallback for now
    if not allennlp_available:
        return {"entities": [], "warning": "allennlp not installed in this image"}
    # otherwise, you could route to a predictor if available
    if predictor:
        return predictor.predict(request.text)
    return {"entities": [], "warning": "predictor not loaded"}
