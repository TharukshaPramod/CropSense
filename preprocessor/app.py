# preprocessor/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from .preprocess import run_preprocessing

app = FastAPI(title="PreprocessorAgent", version="0.1")


@app.get("/health")
def health():
    return {"status": "ok", "service": "preprocessor"}


class PreprocessRequest(BaseModel):
    raw_path: str | None = None

@app.post("/preprocess")
def preprocess(req: PreprocessRequest):
    raw = req.raw_path or None
    try:
        out = run_preprocessing(raw_path=raw)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "ok", "features_path": out}
