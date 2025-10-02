# preprocessor/preprocess.py
import pandas as pd
import numpy as np
import os, joblib
from pathlib import Path
from typing import Dict

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
MODEL_COMMON_DIR = Path("common/models")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
MODEL_COMMON_DIR.mkdir(parents=True, exist_ok=True)

# candidate categorical features (tweak if you have more/less)
CATEGORICAL_CANDIDATES = ["Region", "Soil_Type", "Crop", "Weather_Condition"]

def _find_latest_raw():
    files = sorted(RAW_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError("No raw CSVs in data/raw")
    return files[-1]

def _clean_chunk(df: pd.DataFrame) -> pd.DataFrame:
    # Remove repeated header rows like rows containing "Region" in Region column
    if "Region" in df.columns:
        df = df[df["Region"].astype(str).str.strip().str.lower() != "region"]

    # Strip whitespace for object columns
    obj_cols = df.select_dtypes(include="object").columns
    for c in obj_cols:
        df[c] = df[c].astype(str).str.strip()

    # Normalize boolean-ish columns
    for col in ["Fertilizer_Used", "Irrigation_Used"]:
        if col in df.columns:
            df[col] = df[col].replace(
                {"TRUE": True, "FALSE": False, "True": True, "False": False,
                 "true": True, "false": False, "1": True, "0": False}
            )
            # keep None for missing
            df[col] = df[col].where(pd.notna(df[col]), None)

    # Numeric coercion (coerce errors -> NaN)
    for num in ["Rainfall_mm", "Temperature_Celsius", "Days_to_Harvest", "Yield_tons_per_hectare", "area"]:
        if num in df.columns:
            df[num] = pd.to_numeric(df[num], errors="coerce")

    # invalid rainfall -> NaN
    if "Rainfall_mm" in df.columns:
        df.loc[df["Rainfall_mm"] < -50, "Rainfall_mm"] = np.nan

    # feature engineering example (if 'area' exists)
    if "Rainfall_mm" in df.columns and "area" in df.columns:
        df["rainfall_per_area"] = df["Rainfall_mm"] / df["area"].replace({0: np.nan})

    return df

def run_preprocessing(raw_path: str | None = None) -> str:
    raw = Path(raw_path) if raw_path else _find_latest_raw()
    CHUNKSIZE = 250_000
    parts = []

    reader = pd.read_csv(raw, chunksize=CHUNKSIZE, low_memory=False)
    for i, chunk in enumerate(reader):
        chunk = _clean_chunk(chunk)
        part_path = PROCESSED_DIR / f"part_{i}.parquet"
        chunk.to_parquet(part_path, index=False)
        parts.append(part_path)

    # combine
    dfs = [pd.read_parquet(p) for p in parts]
    full = pd.concat(dfs, ignore_index=True)

    # ---------- CATEGORICAL ENCODING (robust) ----------
    encoders: Dict[str, Dict[str, int]] = {}
    # only encode candidates present in the data
    categorical_cols = [c for c in CATEGORICAL_CANDIDATES if c in full.columns]
    for c in categorical_cols:
        # convert to string for stable mapping (NaN -> "nan" will be handled)
        s = full[c].astype(str).str.strip()
        # build mapping from actual non-null values seen
        vals = list(pd.Series(s).replace({"nan": None, "None": None}).dropna().unique())
        mapping = {v: i for i, v in enumerate(vals)}
        encoders[c] = mapping
        # map to ints, unknown/NaN -> -1
        full[c] = s.map(mapping).fillna(-1).astype(int)

    # ---------- BOOLEAN -> NUMERIC ----------
    for col in ["Fertilizer_Used", "Irrigation_Used"]:
        if col in full.columns:
            full[col] = full[col].map({True: 1, False: 0, "True": 1, "False": 0}).fillna(0).astype(int)

    # ---------- NUMERIC COLUMNS ----------
    # after mapping, categories are ints and booleans numeric
    num_cols = full.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remove target columns from numeric features for imputation/scaling
    target_cols = ["Yield_tons_per_hectare", "yield"]
    feature_num_cols = [col for col in num_cols if col not in target_cols]

    # Impute numeric (median) and scale
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler

    imputer = SimpleImputer(strategy="median")
    scaler = None
    if feature_num_cols:
        full[feature_num_cols] = imputer.fit_transform(full[feature_num_cols])
        scaler = StandardScaler()
        full[feature_num_cols] = scaler.fit_transform(full[feature_num_cols])
        joblib.dump(imputer, MODEL_COMMON_DIR / "imputer.joblib")
        joblib.dump(scaler, MODEL_COMMON_DIR / "scaler.joblib")
    else:
        # save placeholders so later code can load them safely
        joblib.dump(None, MODEL_COMMON_DIR / "imputer.joblib")
        joblib.dump(None, MODEL_COMMON_DIR / "scaler.joblib")

    # Save encoders and numeric column list (use feature columns, not all numeric)
    joblib.dump(encoders, MODEL_COMMON_DIR / "encoders.joblib")
    joblib.dump(feature_num_cols, MODEL_COMMON_DIR / "num_cols.joblib")

    # Write final features parquet
    out = PROCESSED_DIR / "features.parquet"
    full.to_parquet(out, index=False)

    # cleanup part files
    for p in parts:
        try:
            p.unlink()
        except Exception:
            pass

    return str(out)

if __name__ == "__main__":
    print("Running preprocessing...")
    print(run_preprocessing())
