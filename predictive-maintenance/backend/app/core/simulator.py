import random
import math
import time
from datetime import datetime

SERVER_NAMES = [
    "PROD-SRV-01", "PROD-SRV-02", "PROD-SRV-03", "PROD-SRV-04",
    "DB-MASTER-01", "DB-SLAVE-01", "DB-SLAVE-02",
    "CACHE-NODE-01", "CACHE-NODE-02",
    "API-GW-01", "API-GW-02",
    "ML-COMPUTE-01", "ML-COMPUTE-02",
    "STOR-NODE-01", "STOR-NODE-02", "STOR-NODE-03",
]

RACK_MAP = {
    "PROD-SRV-01": "RACK-A1", "PROD-SRV-02": "RACK-A1",
    "PROD-SRV-03": "RACK-A2", "PROD-SRV-04": "RACK-A2",
    "DB-MASTER-01": "RACK-B1", "DB-SLAVE-01": "RACK-B1", "DB-SLAVE-02": "RACK-B2",
    "CACHE-NODE-01": "RACK-C1", "CACHE-NODE-02": "RACK-C1",
    "API-GW-01": "RACK-D1", "API-GW-02": "RACK-D1",
    "ML-COMPUTE-01": "RACK-E1", "ML-COMPUTE-02": "RACK-E1",
    "STOR-NODE-01": "RACK-F1", "STOR-NODE-02": "RACK-F1", "STOR-NODE-03": "RACK-F2",
}

class ServerState:
    """Maintains smooth, realistic telemetry evolution for each server."""
    def __init__(self, name: str, server_id: str):
        self.name = name
        self.server_id = server_id
        self.mode = random.choices(["normal", "warning", "critical"], weights=[0.65, 0.25, 0.10])[0]
        self.step = 0
        self._init_state()

    def _init_state(self):
        if self.mode == "normal":
            self.temp = random.uniform(35, 62)
            self.cpu = random.uniform(15, 65)
            self.mem = random.uniform(25, 72)
            self.power = random.uniform(260, 490)
            self.cooling = random.uniform(65, 92)
            self.net = random.uniform(12, 62)
            self.disk = random.uniform(75, 98)
            self.volt = random.uniform(0.05, 0.7)
        elif self.mode == "warning":
            self.temp = random.uniform(66, 82)
            self.cpu = random.uniform(70, 87)
            self.mem = random.uniform(76, 90)
            self.power = random.uniform(505, 615)
            self.cooling = random.uniform(42, 62)
            self.net = random.uniform(66, 86)
            self.disk = random.uniform(42, 68)
            self.volt = random.uniform(0.85, 1.6)
        else:
            self.temp = random.uniform(86, 105)
            self.cpu = random.uniform(89, 99)
            self.mem = random.uniform(91, 99)
            self.power = random.uniform(625, 695)
            self.cooling = random.uniform(22, 40)
            self.net = random.uniform(87, 99)
            self.disk = random.uniform(12, 38)
            self.volt = random.uniform(1.85, 2.9)

    def _drift(self, val, min_v, max_v, drift=1.5):
        val += random.uniform(-drift, drift)
        return round(max(min_v, min(max_v, val)), 2)

    def tick(self) -> dict:
        self.step += 1
        # Occasionally shift mode
        if self.step % 20 == 0:
            self.mode = random.choices(["normal", "warning", "critical"], weights=[0.65, 0.25, 0.10])[0]
            self._init_state()

        self.temp = self._drift(self.temp, 20, 110, 2.0)
        self.cpu = self._drift(self.cpu, 5, 100, 3.0)
        self.mem = self._drift(self.mem, 10, 100, 2.0)
        self.power = self._drift(self.power, 200, 700, 10.0)
        self.cooling = self._drift(self.cooling, 20, 100, 2.5)
        self.net = self._drift(self.net, 5, 100, 3.0)
        self.disk = self._drift(self.disk, 10, 100, 1.0)
        self.volt = self._drift(self.volt, 0.0, 3.0, 0.15)

        return {
            "server_id": self.server_id,
            "server_name": self.name,
            "rack": RACK_MAP.get(self.name, "RACK-X"),
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": round(self.temp, 2),
            "cpu_usage": round(self.cpu, 2),
            "memory_usage": round(self.mem, 2),
            "power_consumption": round(self.power, 2),
            "cooling_efficiency": round(self.cooling, 2),
            "network_load": round(self.net, 2),
            "disk_health": round(self.disk, 2),
            "voltage_fluctuation": round(self.volt, 3),
        }


class TelemetrySimulator:
    def __init__(self):
        self.servers = {
            name: ServerState(name, f"SRV-{str(i+1).zfill(3)}")
            for i, name in enumerate(SERVER_NAMES)
        }

    def generate_batch(self) -> list[dict]:
        return [srv.tick() for srv in self.servers.values()]

    def get_server_telemetry(self, server_id: str) -> dict | None:
        for srv in self.servers.values():
            if srv.server_id == server_id:
                return srv.tick()
        return None
