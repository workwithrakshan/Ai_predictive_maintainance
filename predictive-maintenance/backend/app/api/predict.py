from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.core.ml_engine import MLEngine

router = APIRouter()
ml = MLEngine()

class TelemetryInput(BaseModel):
    temperature: float = Field(..., ge=0, le=150)
    cpu_usage: float = Field(..., ge=0, le=100)
    memory_usage: float = Field(..., ge=0, le=100)
    power_consumption: float = Field(..., ge=0, le=1000)
    cooling_efficiency: float = Field(..., ge=0, le=100)
    network_load: float = Field(..., ge=0, le=100)
    disk_health: float = Field(..., ge=0, le=100)
    voltage_fluctuation: float = Field(..., ge=0, le=10)

class BatchInput(BaseModel):
    servers: list[TelemetryInput]

@router.post("/single")
def predict_single(data: TelemetryInput):
    result = ml.predict(data.dict())
    return {"input": data.dict(), "prediction": result}

@router.post("/batch")
def predict_batch(data: BatchInput):
    results = ml.batch_predict([s.dict() for s in data.servers])
    return {"count": len(results), "predictions": results}
























