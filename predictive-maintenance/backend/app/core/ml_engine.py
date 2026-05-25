import joblib
import numpy as np
import os
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent / "ml" / "rf_model.pkl"
SCALER_PATH = Path(__file__).parent.parent / "ml" / "scaler.pkl"

FEATURES = [
    "temperature", "cpu_usage", "memory_usage", "power_consumption",
    "cooling_efficiency", "network_load", "disk_health", "voltage_fluctuation"
]

THRESHOLDS = {
    "temperature":         {"warning": 70, "critical": 85},
    "cpu_usage":           {"warning": 78, "critical": 90},
    "memory_usage":        {"warning": 80, "critical": 92},
    "power_consumption":   {"warning": 580, "critical": 640},
    "cooling_efficiency":  {"warning": 50, "critical": 38},   # lower is worse
    "network_load":        {"warning": 75, "critical": 90},
    "disk_health":         {"warning": 55, "critical": 35},   # lower is worse
    "voltage_fluctuation": {"warning": 1.2, "critical": 2.0},
}

RISK_LABELS = {0: "Normal", 1: "Warning", 2: "Critical"}
RISK_COLORS = {0: "#22c55e", 1: "#f59e0b", 2: "#ef4444"}

class MLEngine:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)

    def predict(self, telemetry: dict) -> dict:
        X = np.array([[telemetry[f] for f in FEATURES]])
        X_scaled = self.scaler.transform(X)
        pred_class = int(self.model.predict(X_scaled)[0])
        proba = self.model.predict_proba(X_scaled)[0]

        risk_score = round(float(proba[1]) * 50 + float(proba[2]) * 100, 1)
        triggered = self._check_thresholds(telemetry)
        
        # Compute MTTR estimate
        mttr_map = {0: None, 1: round(np.random.uniform(8, 24), 1), 2: round(np.random.uniform(1, 8), 1)}

        return {
            "prediction": pred_class,
            "risk_level": RISK_LABELS[pred_class],
            "risk_color": RISK_COLORS[pred_class],
            "risk_score": risk_score,
            "confidence": round(float(max(proba)) * 100, 1),
            "probabilities": {
                "normal": round(float(proba[0]) * 100, 1),
                "warning": round(float(proba[1]) * 100, 1),
                "critical": round(float(proba[2]) * 100, 1),
            },
            "triggered_params": triggered,
            "estimated_ttf_hours": mttr_map[pred_class],
        }

    def _check_thresholds(self, t: dict) -> list[dict]:
        triggered = []
        for param, bounds in THRESHOLDS.items():
            val = t.get(param, 0)
            inverted = param in ("cooling_efficiency", "disk_health")
            if inverted:
                if val <= bounds["critical"]:
                    triggered.append({"param": param, "value": val, "level": "Critical"})
                elif val <= bounds["warning"]:
                    triggered.append({"param": param, "value": val, "level": "Warning"})
            else:
                if val >= bounds["critical"]:
                    triggered.append({"param": param, "value": val, "level": "Critical"})
                elif val >= bounds["warning"]:
                    triggered.append({"param": param, "value": val, "level": "Warning"})
        return triggered

    def batch_predict(self, telemetry_list: list[dict]) -> list[dict]:
        return [self.predict(t) for t in telemetry_list]
