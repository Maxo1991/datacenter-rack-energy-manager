import pytest
from fastapi.testclient import TestClient
import routers.allocations as alloc_mod
from main import app

client = TestClient(app)

@pytest.fixture
def setup_data(monkeypatch):
    class MockDevice:
        def __init__(self, name, units, power):
            self.name = name
            self.units = units
            self.power = power

    devices = [
        MockDevice("Device 1", 5, 50),
        MockDevice("Device 2", 4, 30),
        MockDevice("Device 3", 10, 90) 
    ]

    racks = [
        (1, "Rack A", "desc", "SN1", 10, 100),
        (2, "Rack B", "desc", "SN2", 20, 150)
    ]

    monkeypatch.setattr(alloc_mod, "get_devices", lambda conn: devices)
    monkeypatch.setattr(alloc_mod, "get_all_racks", lambda conn: racks)

def test_allocate_endpoint_integration(setup_data):
    response = client.get("/allocate")
    assert response.status_code == 200

    data = response.json()
    assert "allocations" in data
    assert "unallocated_devices" in data

    all_allocated = [d for r in data["allocations"] for d in r["devices"]]
    for device_name in ["Device 1", "Device 2", "Device 3"]:
        if device_name not in data["unallocated_devices"]:
            assert device_name in all_allocated

    for r in data["allocations"]:
        assert r["used_units_percent"] <= 100
        assert r["power_usage_percent"] <= 100
