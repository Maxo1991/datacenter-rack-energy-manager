import pytest
from services.allocations import allocate_devices

class Device:
    def __init__(self, name, units, power):
        self.name = name
        self.units = units
        self.power = power

@pytest.fixture
def racks():
    return [
        (1, "Rack A", "desc", "SN1", 10, 100),
        (2, "Rack B", "desc", "SN2", 10, 100)
    ]

@pytest.fixture
def devices_small():
    return [
        Device("Device 1", 5, 50),
        Device("Device 2", 4, 30)
    ]

@pytest.fixture
def devices_large():
    return [
        Device("Device 1", 5, 50),
        Device("Device 2", 6, 60),
        Device("Device 3", 15, 120)
    ]

@pytest.fixture
def empty_racks():
    return []

@pytest.fixture
def empty_devices():
    return []

def test_allocate_basic(devices_small, racks):
    result = allocate_devices(devices_small, racks)
    assert "allocations" in result
    assert "unallocated_devices" in result
    assert len(result["allocations"]) == len(racks)
    assert len(result["unallocated_devices"]) == 0

def test_allocate_with_unallocated(devices_large, racks):
    result = allocate_devices(devices_large, racks)
    assert "Device 3" in result["unallocated_devices"]
    allocated_devices = [d for r in result["allocations"] for d in r["devices"]]
    assert "Device 1" in allocated_devices
    assert "Device 2" in allocated_devices

def test_allocate_no_racks(devices_small, empty_racks):
    result = allocate_devices(devices_small, empty_racks)
    assert result["allocations"] == []
    assert set(result["unallocated_devices"]) == {"Device 1", "Device 2"}

def test_allocate_no_devices(empty_devices, racks):
    result = allocate_devices(empty_devices, racks)
    for r in result["allocations"]:
        assert r["devices"] == []
        assert r["used_units"] == 0
        assert r["used_power"] == 0
        assert r["power_usage_percent"] == 0
    assert result["unallocated_devices"] == []

def test_allocate_no_racks_no_devices(empty_racks, empty_devices):
    result = allocate_devices(empty_devices, empty_racks)
    assert result["allocations"] == []
    assert result["unallocated_devices"] == []

def test_allocate_edge_case_exact_fit():
    racks = [
        (1, "Rack A", "desc", "SN1", 10, 100),
        (2, "Rack B", "desc", "SN2", 10, 100)
    ]
    devices = [
        Device("Device 1", 10, 50),
        Device("Device 2", 10, 50)
    ]
    result = allocate_devices(devices, racks)
    for r in result["allocations"]:
        assert r["used_units_percent"] <= 100
        assert r["power_usage_percent"] <= 100
    assert result["unallocated_devices"] == []
