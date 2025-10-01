# data_collector/app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os, shutil, pandas as pd, json
from datetime import datetime
from pathlib import Path

app = FastAPI(title="DataCollectorAgent")

RAW_DIR = Path("data/raw")
METADATA_DIR = Path("data/metadata")
SAMPLE_SOURCE = Path("data/sample_data/sample_crop.csv")

RAW_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)

class CollectRequest(BaseModel):
    source: str = "local"   # "local" | "uploaded"
    path: str | None = None

def _dest_name():
    return f"raw_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.csv"

@app.post("/collect")
def collect(req: CollectRequest):
    if req.source == "local":
        src = Path(req.path) if req.path else SAMPLE_SOURCE
        if not src.exists():
            raise HTTPException(404, f"Source not found: {src}")
        dst = RAW_DIR / _dest_name()
        shutil.copy(src, dst)
        meta = {"source": str(src), "dst": str(dst), "time": datetime.utcnow().isoformat()}
        (METADATA_DIR / (dst.stem + ".json")).write_text(json.dumps(meta))
        return {"status": "collected", "path": str(dst), "meta": meta}
    else:
        raise HTTPException(400, "Use /upload for multipart uploads")

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only csv uploads supported")
    dest = RAW_DIR / _dest_name()
    content = await file.read()
    dest.write_bytes(content)
    meta = {"source": file.filename, "dst": str(dest), "time": datetime.utcnow().isoformat()}
    (METADATA_DIR / (dest.stem + ".json")).write_text(json.dumps(meta))
    return {"status": "uploaded", "path": str(dest)}
