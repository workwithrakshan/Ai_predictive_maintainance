from fastapi import APIRouter
from app.core.simulator import TelemetrySimulator, SERVER_NAMES, RACK_MAP
from app.core.ml_engine import MLEngine
#summa
router = APIRouter()
sim = TelemetrySimulator()
ml = MLEngine()

@router.get("/")
def list_servers():
    servers = []
    for i, name in enumerate(SERVER_NAMES):
        t = sim.get_server_telemetry(f"SRV-{str(i+1).zfill(3)}")
        if t:
            pred = ml.predict(t)
            servers.append({**t, **pred})
    return {"count": len(servers), "servers": servers}

@router.get("/{server_id}")
def get_server(server_id: str):
    t = sim.get_server_telemetry(server_id)
    if not t:
        return {"error": "Server not found"}
    pred = ml.predict(t)
    return {**t, **pred}

@router.get("/{server_id}/history")
def get_history(server_id: str, points: int = 20):
    """Simulate historical telemetry for trend charts."""
    import random, time
    from datetime import datetime, timedelta
    history = []
    base_t = datetime.utcnow()
    for i in range(points, 0, -1):
        ts = base_t - timedelta(minutes=i * 3)
        t = {
            "timestamp": ts.isoformat(),
            "temperature": round(random.uniform(40, 90), 2),
            "cpu_usage": round(random.uniform(20, 95), 2),
            "memory_usage": round(random.uniform(30, 95), 2),
            "power_consumption": round(random.uniform(300, 680), 2),
            "cooling_efficiency": round(random.uniform(30, 95), 2),
            "network_load": round(random.uniform(10, 95), 2),
            "disk_health": round(random.uniform(20, 98), 2),
            "voltage_fluctuation": round(random.uniform(0.1, 2.5), 3),
        }
        pred = ml.predict(t)
        history.append({**t, "risk_level": pred["risk_level"], "risk_score": pred["risk_score"]})
    return {"server_id": server_id, "history": history}
