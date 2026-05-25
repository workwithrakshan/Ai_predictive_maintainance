from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio, json, random, time
from datetime import datetime
from app.api import predict, servers, analytics, alerts
from app.core.simulator import TelemetrySimulator
from app.core.ml_engine import MLEngine

app = FastAPI(
    title="NexusGuard AI — Predictive Maintenance API",
    description="Enterprise-grade ML-powered predictive maintenance for data center infrastructure",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/api/predict", tags=["Predictions"])
app.include_router(servers.router, prefix="/api/servers", tags=["Servers"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])

simulator = TelemetrySimulator()
ml_engine = MLEngine()

# In-memory alert log shared across WS clients
alert_store: list = []

class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, data: dict):
        dead = []
        for ws in self.active:
            try:
                await ws.send_json(data)
            except:
                dead.append(ws)
        for ws in dead:
            self.active.remove(ws)

manager = ConnectionManager()

@app.websocket("/ws/telemetry")
async def telemetry_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            batch = simulator.generate_batch()
            predictions = []
            for srv in batch:
                pred = ml_engine.predict(srv)
                if pred["risk_level"] in ("Warning", "Critical"):
                    alert = {
                        "id": f"ALT-{int(time.time()*1000)}",
                        "server_id": srv["server_id"],
                        "server_name": srv["server_name"],
                        "risk_level": pred["risk_level"],
                        "risk_score": pred["risk_score"],
                        "triggered_params": pred["triggered_params"],
                        "timestamp": datetime.utcnow().isoformat(),
                        "acknowledged": False
                    }
                    alert_store.insert(0, alert)
                    if len(alert_store) > 200:
                        alert_store.pop()
                predictions.append({**srv, **pred})

            await websocket.send_json({
                "type": "telemetry_batch",
                "timestamp": datetime.utcnow().isoformat(),
                "servers": predictions,
                "alert_count": len([a for a in alert_store if not a["acknowledged"]])
            })
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/health")
def health():
    return {"status": "online", "model": "RandomForest v2.0", "uptime": "operational"}

@app.get("/api/alerts/live")
def get_live_alerts():
    return {"alerts": alert_store[:50], "total": len(alert_store)}

@app.post("/api/alerts/{alert_id}/acknowledge")
def ack_alert(alert_id: str):
    for a in alert_store:
        if a["id"] == alert_id:
            a["acknowledged"] = True
            return {"status": "acknowledged"}
    return JSONResponse(status_code=404, content={"error": "Alert not found"})
