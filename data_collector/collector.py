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
    
    # Check if source exists, if not create synthetic data
    if not os.path.exists(src_path):
        print(f"Source file {src_path} not found, creating synthetic dataset...")
        # synthesize small demo dataset so pipeline can run end-to-end
        demo = pd.DataFrame({
            "Region": ["West", "East", "North", "South"] * 25,  # 100 rows
            "Soil_Type": ["Sandy", "Loam", "Clay", "Silt"] * 25,
            "Crop": ["Wheat", "Rice", "Soybean", "Barley"] * 25,
            "Rainfall_mm": [800, 1200, 600, 900] * 25,
            "Temperature_Celsius": [25, 28, 22, 26] * 25,
            "Fertilizer_Used": [True, True, False, True] * 25,
            "Irrigation_Used": [True, False, True, True] * 25,
            "Weather_Condition": ["Sunny", "Cloudy", "Rainy", "Sunny"] * 25,
            "Days_to_Harvest": [120, 140, 110, 130] * 25,
            "Yield_tons_per_hectare": [3.2, 4.1, 2.8, 3.6] * 25
        })
        demo.to_csv(dest, index=False)
        print(f"Created synthetic dataset at {dest}")
    else:
        shutil.copyfile(src_path, dest)
    # quick sanity check: try reading head
    try:
        _ = pd.read_csv(dest, nrows=5)
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
        pd.read_csv(dest, nrows=5)
    except Exception:
        os.remove(dest)
        raise
    return dest
