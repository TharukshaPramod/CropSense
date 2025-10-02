# data_collector/app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from .collector import save_raw_from_path, save_raw_from_upload
from pathlib import Path

app = FastAPI(title="DataCollectorAgent", version="0.1")
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

class CollectRequest(BaseModel):
    source: str = "local"
    path: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "collector"}

@app.post("/collect")
def collect(req: CollectRequest):
    if req.source == "local":
        src = req.path or "data/crop_yield.csv"
        # Let save_raw_from_path handle missing files by creating synthetic data
        dst = save_raw_from_path(src)
        return {"status": "collected", "path": dst}
    else:
        raise HTTPException(400, "Unsupported source")

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only CSV allowed")
    dst = await save_raw_from_upload(file)
    return {"status": "uploaded", "path": dst}

@app.get("/list")
def list_raws():
    files = sorted([str(p) for p in RAW_DIR.glob("*.csv")])
    return {"files": files}
