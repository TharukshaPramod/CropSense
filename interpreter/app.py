from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from pathlib import Path
from common.auth import get_current_user_optional

app = FastAPI(title="InterpreterAgent", version="0.2")
MODEL_PATH = Path("predictor/models/model.joblib")

class ExplainRequest(BaseModel):
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
    return {"status": "ok", "service": "interpreter", "model_exists": MODEL_PATH.exists()}

@app.post("/explain")
def explain(req: ExplainRequest, user: str | None = Depends(get_current_user_optional)):
    from .explain import explain_sample
    res = explain_sample(req.dict())
    if res.get("status") != "ok":
        raise HTTPException(status_code=503, detail=res.get("detail"))
    return res
