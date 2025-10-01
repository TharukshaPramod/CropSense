# interpreter/app.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from common.auth import get_current_user
from .explain import explain_sample

app = FastAPI(title="InterpreterAgent")

class RequestModel(BaseModel):
    # provide flexible fields:
    Region: str | None = None
    Soil_Type: str | None = None
    Crop: str | None = None
    Rainfall_mm: float | None = None
    Temperature_Celsius: float | None = None
    Fertilizer_Used: bool | None = None
    Irrigation_Used: bool | None = None
    Weather_Condition: str | None = None
    Days_to_Harvest: float | None = None

@app.post("/explain")
def explain(req: RequestModel, user: str = Depends(get_current_user)):
    sample = req.dict()
    try:
        res = explain_sample(sample)
        return res
    except Exception as e:
        raise HTTPException(500, str(e))
