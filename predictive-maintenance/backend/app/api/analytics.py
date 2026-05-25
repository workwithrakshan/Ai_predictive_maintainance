from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()
METRICS_PATH = Path(__file__).parent.parent / "ml" / "metrics.json"

@router.get("/model-metrics")
def model_metrics():
    with open(METRICS_PATH) as f:
        return json.load(f)

@router.get("/infrastructure-summary")
def infra_summary():
    from app.core.simulator import TelemetrySimulator
    from app.core.ml_engine import MLEngine
    import random
    sim = TelemetrySimulator()
    ml = MLEngine()
    batch = sim.generate_batch()
    preds = [ml.predict(t) for t in batch]
    
    normal = sum(1 for p in preds if p["risk_level"] == "Normal")
    warning = sum(1 for p in preds if p["risk_level"] == "Warning")
    critical = sum(1 for p in preds if p["risk_level"] == "Critical")
    avg_score = round(sum(p["risk_score"] for p in preds) / len(preds), 1)
    
    return {
        "total_servers": len(batch),
        "normal": normal,
        "warning": warning,
        "critical": critical,
        "avg_risk_score": avg_score,
        "infrastructure_health": round((normal / len(batch)) * 100, 1),
        "alerts_last_hour": random.randint(warning + critical, warning + critical + 5),
    }

@router.get("/rack-summary")
def rack_summary():
    from app.core.simulator import TelemetrySimulator, RACK_MAP
    from app.core.ml_engine import MLEngine
    from collections import defaultdict
    sim = TelemetrySimulator()
    ml = MLEngine()
    batch = sim.generate_batch()
    preds = [ml.predict(t) for t in batch]
    
    racks = defaultdict(lambda: {"normal": 0, "warning": 0, "critical": 0, "servers": 0})
    for t, p in zip(batch, preds):
        rack = t["rack"]
        racks[rack]["servers"] += 1
        racks[rack][p["risk_level"].lower()] += 1
    
    return {"racks": dict(racks)}
