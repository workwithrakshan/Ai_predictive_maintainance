#!/bin/bash
# NexusGuard AI — Start Script
echo "========================================="
echo "  NexusGuard AI — Predictive Maintenance"
echo "========================================="

# Backend
echo ""
echo "[1/2] Starting FastAPI backend on http://localhost:8000 ..."
cd backend
pip install -r requirements.txt -q
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "      Backend PID: $BACKEND_PID"

# Frontend
echo ""
echo "[2/2] Frontend: open frontend/index.html in your browser"
echo "      Or serve it: python3 -m http.server 3000 -d frontend"
echo ""
echo "  API Docs:   http://localhost:8000/api/docs"
echo "  WebSocket:  ws://localhost:8000/ws/telemetry"
echo "  Dashboard:  frontend/index.html"
echo ""
echo "  Press Ctrl+C to stop."
wait $BACKEND_PID
