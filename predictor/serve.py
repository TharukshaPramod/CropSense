# predictor/serve.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import joblib, numpy as np, pandas as pd
from common.auth import get_current_user
from pathlib import Path

app = FastAPI(title="PredictorAgent")
MODEL_PATH = Path("predictor/models/model.joblib")
if MODEL_PATH.exists():
    artifact = joblib.load(MODEL_PATH)
    model = artifact["model"]
    feature_columns = artifact["feature_columns"]
else:
    model = None
    feature_columns = None

class PredictSingle(BaseModel):
    # Accept flexible fields — must match pipeline feature columns
    Region: str | None = None
    Soil_Type: str | None = None
    Crop: str | None = None
    Rainfall_mm: float | None = None
    Temperature_Celsius: float | None = None
    Fertilizer_Used: bool | None = None
    Irrigation_Used: bool | None = None
    Weather_Condition: str | None = None
    Days_to_Harvest: float | None = None

@app.post("/predict")
def predict_one(payload: PredictSingle, user: str = Depends(get_current_user)):
    if model is None:
        raise HTTPException(500, "Model not trained")
    # build df row
    row = pd.DataFrame([payload.dict()])
    # ensure same columns as training (simple alignment)
    for c in feature_columns:
        if c not in row.columns:
            row[c] = 0
    row = row[feature_columns]
    preds = model.predict(row)
    return {"predicted_yield": float(preds[0])}
