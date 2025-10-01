# collector.py
# data_collector/collector.py
import os
import shutil
from fastapi import UploadFile
from datetime import datetime
import pandas as pd

RAW_DIR = "data/raw"

def _dest_filename():
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    return f"raw_crop_{ts}.csv"

def save_raw_from_path(src_path: str) -> str:
    os.makedirs(RAW_DIR, exist_ok=True)
    dest = os.path.join(RAW_DIR, _dest_filename())
    shutil.copyfile(src_path, dest)
    # quick sanity check: try reading head
    try:
        df = pd.read_csv(dest, nrows=5)
    except Exception:
        os.remove(dest)
        raise
    return dest

async def save_raw_from_upload(file: UploadFile) -> str:
    os.makedirs(RAW_DIR, exist_ok=True)
    dest = os.path.join(RAW_DIR, _dest_filename())
    with open(dest, "wb") as f:
        contents = await file.read()
        f.write(contents)
    # validate CSV
    try:
        import pandas as pd
        pd.read_csv(dest, nrows=5)
    except Exception:
        os.remove(dest)
        raise
    return dest
