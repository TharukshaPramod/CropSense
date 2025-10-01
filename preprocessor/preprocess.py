# preprocessor/preprocess.py
import pandas as pd
import numpy as np
import os, math, joblib
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
MODEL_COMMON_DIR = Path("common/models")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
MODEL_COMMON_DIR.mkdir(parents=True, exist_ok=True)

def _find_latest_raw():
    files = sorted(RAW_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError("No raw CSVs in data/raw")
    return files[-1]

def _clean_chunk(df: pd.DataFrame) -> pd.DataFrame:
    # Remove repeated header rows
    if "Region" in df.columns:
        df = df[df["Region"].astype(str).str.strip().str.lower() != "region"]
    # Strip whitespace in object columns
    obj_cols = df.select_dtypes(include="object").columns
    for c in obj_cols:
        df[c] = df[c].astype(str).str.strip()
    # Convert TRUE/FALSE to bool
    for col in ["Fertilizer_Used", "Irrigation_Used"]:
        if col in df.columns:
            df[col] = df[col].replace({"TRUE": True, "FALSE": False, "True": True, "False": False}).astype("boolean")
    # Numeric coercion
    for num in ["Rainfall_mm", "Temperature_Celsius", "Days_to_Harvest", "Yield_tons_per_hectare"]:
        if num in df.columns:
            df[num] = pd.to_numeric(df[num], errors="coerce")
    # Mark impossible rainfall as NaN (negative extreme)
    if "Rainfall_mm" in df.columns:
        df.loc[df["Rainfall_mm"] < -50, "Rainfall_mm"] = np.nan  # threshold -50 mm
    # Feature engineering
    if "Rainfall_mm" in df.columns and "area" in df.columns:  # if area exists
        df["rainfall_per_area"] = df["Rainfall_mm"] / df["area"].replace({0: np.nan})
    # Simple encoded categorical mapping (keep categories)
    for c in ["Region", "Soil_Type", "Crop", "Weather_Condition"]:
        if c in df.columns:
            df[c] = df[c].astype("category")
    return df

def run_preprocessing(raw_path: str | None = None) -> str:
    raw = Path(raw_path) if raw_path else _find_latest_raw()
    # If huge file, read by chunks and process -> write to parquet in chunks
    CHUNKSIZE = 250_000
    parts = []
    reader = pd.read_csv(raw, chunksize=CHUNKSIZE, low_memory=False)
    for i, chunk in enumerate(reader):
        chunk = _clean_chunk(chunk)
        part_path = PROCESSED_DIR / f"part_{i}.parquet"
        chunk.to_parquet(part_path, index=False)
        parts.append(part_path)
    # Concatenate parts into final parquet (pyarrow)
    dfs = [pd.read_parquet(p) for p in parts]
    full = pd.concat(dfs, ignore_index=True)
    # Final imputation & scaling (fit on full)
    num_cols = full.select_dtypes(include=["number"]).columns.tolist()
    # Impute numeric with median
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    imputer = SimpleImputer(strategy="median")
    full[num_cols] = imputer.fit_transform(full[num_cols])
    scaler = StandardScaler()
    full[num_cols] = scaler.fit_transform(full[num_cols])
    # Save artifacts
    joblib.dump(imputer, MODEL_COMMON_DIR / "imputer.joblib")
    joblib.dump(scaler, MODEL_COMMON_DIR / "scaler.joblib")
    out = PROCESSED_DIR / "features.parquet"
    full.to_parquet(out, index=False)
    # cleanup parts
    for p in parts:
        try: p.unlink()
        except: pass
    return str(out)

# standalone API wrapper
if __name__ == "__main__":
    print("Running preprocessing...")
    print(run_preprocessing())
