# predictor/serve.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import joblib, pandas as pd, numpy as np
from common.auth import get_current_user_optional
from pathlib import Path
from .train import train_and_save

app = FastAPI(title="PredictorAgent", version="0.2")
MODEL_PATH = Path("predictor/models/model.joblib")
COMMON_MODELS = Path("common/models")

# Lazy loaders
_model_artifact = None
_encoders = None
_imputer = None
_scaler = None
_feature_columns = None
_num_cols = None

def _load_artifact():
    global _model_artifact, _encoders, _imputer, _scaler, _feature_columns, _num_cols
    if _model_artifact is None and MODEL_PATH.exists():
        _model_artifact = joblib.load(MODEL_PATH)
        _feature_columns = _model_artifact.get("feature_columns")
        # artifact may contain preprocessor or we fallback to common/models
        pre = _model_artifact.get("preprocessor", {})
        _encoders = pre.get("encoders") or (joblib.load(COMMON_MODELS / "encoders.joblib") if (COMMON_MODELS / "encoders.joblib").exists() else {})
        _imputer = pre.get("imputer") or (joblib.load(COMMON_MODELS / "imputer.joblib") if (COMMON_MODELS / "imputer.joblib").exists() else None)
        _scaler = pre.get("scaler") or (joblib.load(COMMON_MODELS / "scaler.joblib") if (COMMON_MODELS / "scaler.joblib").exists() else None)
        _num_cols = pre.get("num_cols") or (joblib.load(COMMON_MODELS / "num_cols.joblib") if (COMMON_MODELS / "num_cols.joblib").exists() else None)
    return _model_artifact, _encoders, _imputer, _scaler, _feature_columns, _num_cols

class PredictSingle(BaseModel):
    Region: str | None = None
    Soil_Type: str | None = None
    Crop: str | None = None
    Rainfall_mm: float | None = None
    Temperature_Celsius: float | None = None
    Fertilizer_Used: bool | None = None
    Irrigation_Used: bool | None = None
    Weather_Condition: str | None = None
    Days_to_Harvest: float | None = None

@app.get("/health")
def health():
    model_loaded = MODEL_PATH.exists()
    return {"status": "ok", "service": "predictor", "model_loaded": model_loaded}

def _apply_preprocessor(row: pd.DataFrame, encoders, imputer, scaler, num_cols, feature_columns):
    # map encoders
    if encoders:
        for c, mapping in encoders.items():
            if c in row.columns:
                # convert to str and map unknown -> -1
                row[c] = row[c].astype(str).map(mapping).fillna(-1).astype(float)
    # booleans -> numeric
    for col in ["Fertilizer_Used", "Irrigation_Used"]:
        if col in row.columns:
            row[col] = row[col].map({True:1, False:0, "True":1, "False":0}).fillna(0).astype(float)
    
    # Remove target column if present (should not be in feature_columns but just in case)
    target_cols = ["Yield_tons_per_hectare", "yield"]
    for target in target_cols:
        if target in row.columns:
            row = row.drop(columns=[target])
    
    # ensure all model feature columns present
    for c in feature_columns:
        if c not in row.columns:
            row[c] = 0.0
    row = row[feature_columns].astype(float)

    # impute + scale only numeric columns if artifacts present
    if imputer is not None and num_cols:
        # Filter num_cols to only include columns that exist in the row
        available_num_cols = [c for c in num_cols if c in row.columns]
        if available_num_cols:
            row[available_num_cols] = imputer.transform(row[available_num_cols])
    if scaler is not None and num_cols:
        # Filter num_cols to only include columns that exist in the row
        available_num_cols = [c for c in num_cols if c in row.columns]
        if available_num_cols:
            row[available_num_cols] = scaler.transform(row[available_num_cols])
    return row

@app.post("/predict")
def predict_one(payload: PredictSingle, user: str | None = Depends(get_current_user_optional)):
    global _model_artifact
    artifact, encoders, imputer, scaler, feature_columns, num_cols = _load_artifact()
    if artifact is None:
        raise HTTPException(500, "Model not trained")
    model = artifact["model"]
    # convert to dataframe (single-row)
    row = pd.DataFrame([payload.dict()])
    # Apply preprocessor (safe)
    row = _apply_preprocessor(row, encoders or {}, imputer, scaler, num_cols or [], feature_columns)
    preds = model.predict(row)
    return {"predicted_yield": float(preds[0])}

@app.post("/train")
def train(user: str | None = Depends(get_current_user_optional)):
    try:
        metrics = train_and_save()
        # clear lazy cache so subsequent predictions load fresh artifact
        global _model_artifact, _encoders, _imputer, _scaler, _feature_columns, _num_cols
        _model_artifact = None
        _encoders = None
        _imputer = None
        _scaler = None
        _feature_columns = None
        _num_cols = None
        return {"status": "ok", **metrics}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
