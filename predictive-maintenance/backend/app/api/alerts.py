from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def alerts_placeholder():
    return {"message": "Use /api/alerts/live for live alerts or connect via WebSocket /ws/telemetry"}
