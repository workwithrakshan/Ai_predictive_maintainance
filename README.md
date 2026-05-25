# NexusGuard AI - Predictive Maintenance System

An enterprise-grade ML-powered predictive maintenance system for data center infrastructure monitoring and failure prediction.

## 🏗️ Project Structure

```
NexusGuard-AI-Predictive-Maintenance/
├── venv/                           # Python virtual environment
├── predictive-maintenance/
│   ├── backend/                    # FastAPI backend server
│   │   ├── app/
│   │   │   ├── api/               # API endpoints
│   │   │   │   ├── alerts.py      # Alert management
│   │   │   │   ├── analytics.py   # Analytics & metrics
│   │   │   │   ├── predict.py     # ML predictions
│   │   │   │   └── servers.py     # Server monitoring
│   │   │   ├── core/              # Core business logic
│   │   │   │   ├── ml_engine.py   # ML model engine
│   │   │   │   └── simulator.py   # Telemetry simulator
│   │   │   ├── ml/                # Pre-trained ML models
│   │   │   │   ├── rf_model.pkl   # Random Forest model
│   │   │   │   ├── scaler.pkl     # Feature scaler
│   │   │   │   └── metrics.json   # Model performance
│   │   │   └── main.py            # FastAPI application
│   │   └── requirements.txt       # Python dependencies
│   └── frontend/
│       └── index.html             # Web dashboard (standalone)
├── requirements.txt               # Project dependencies
├── setup-venv.bat                # Windows setup script
└── README.md                     # This file
```

## 🚀 Quick Start

### Option 1: Automated Setup (Windows)
```bash
# Run the setup script
setup-venv.bat
```

### Option 2: Manual Setup
```bash
# 1. Activate virtual environment
venv\Scripts\activate.bat

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start backend
cd predictive-maintenance\backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 4. Open frontend\index.html in browser
```

## 🌐 Access Points

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc
- **WebSocket**: ws://localhost:8000/ws/telemetry
- **Dashboard**: Open `frontend/index.html` in browser

## 🔧 System Features

### Backend (FastAPI)
- **Real-time telemetry simulation** for 16 servers across 6 racks
- **ML-powered predictions** using Random Forest classifier
- **WebSocket streaming** for live data updates
- **RESTful API** for server monitoring and predictions
- **Alert management** with acknowledgment system

### Frontend (Vanilla JS)
- **Real-time dashboard** with live telemetry visualization
- **Risk assessment** with color-coded server status
- **Interactive charts** using Chart.js
- **Alert management** with real-time notifications
- **Manual prediction** interface for testing

### ML Engine
- **Random Forest classifier** with 100% accuracy on test data
- **8 telemetry features**: temperature, CPU, memory, power, cooling, network, disk, voltage
- **3-class prediction**: Normal, Warning, Critical
- **Real-time risk scoring** and time-to-failure estimation

## 📊 Monitored Parameters

| Parameter | Normal Range | Warning Threshold | Critical Threshold |
|-----------|--------------|-------------------|-------------------|
| Temperature | 35-62°C | >70°C | >85°C |
| CPU Usage | 15-65% | >78% | >90% |
| Memory Usage | 25-72% | >80% | >92% |
| Power Consumption | 260-490W | >580W | >640W |
| Cooling Efficiency | 65-92% | <50% | <38% |
| Network Load | 12-62% | >75% | >90% |
| Disk Health | 75-98% | <55% | <35% |
| Voltage Fluctuation | 0.05-0.7V | >1.2V | >2.0V |

## 🔄 Workflow

1. **Telemetry Generation**: Simulator creates realistic server metrics
2. **ML Processing**: Random Forest model analyzes telemetry data
3. **Risk Assessment**: System classifies servers as Normal/Warning/Critical
4. **Alert Generation**: Automatic alerts for Warning/Critical servers
5. **Real-time Updates**: WebSocket streams data to dashboard
6. **User Interaction**: Operators can acknowledge alerts and run manual predictions

## 🛠️ Development

### Adding New Features
- **API endpoints**: Add to `backend/app/api/`
- **ML models**: Place in `backend/app/ml/`
- **Business logic**: Implement in `backend/app/core/`

### Testing Predictions
Use the manual prediction interface in the dashboard or API:
```bash
curl -X POST "http://localhost:8000/api/predict/single" \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 95,
    "cpu_usage": 92,
    "memory_usage": 94,
    "power_consumption": 660,
    "cooling_efficiency": 28,
    "network_load": 93,
    "disk_health": 22,
    "voltage_fluctuation": 2.3
  }'
```

## 📈 Performance Metrics

- **Model Accuracy**: 100% on test dataset
- **Real-time Processing**: <50ms prediction latency
- **Concurrent Users**: Supports multiple WebSocket connections
- **Data Throughput**: 16 servers × 8 metrics × 20 updates/minute

## 🔒 Security Notes

- No authentication implemented (development only)
- CORS enabled for all origins
- WebSocket connections are unencrypted
- For production: Add authentication, HTTPS, and input validation

## 🐛 Troubleshooting

### Common Issues
1. **Import errors**: Ensure virtual environment is activated
2. **Port conflicts**: Change port in uvicorn command
3. **WebSocket connection failed**: Check if backend is running
4. **Charts not loading**: Ensure internet connection for CDN resources

### Logs
- Backend logs appear in terminal where uvicorn is running
- Frontend logs available in browser developer console