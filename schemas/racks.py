from pydantic import BaseModel, field_serializer, ConfigDict
from typing import List

class RackCreate(BaseModel):
    name: str
    description: str
    serial_number: str
    capacity_units: int
    max_power: int

class DeviceInRack(BaseModel):
    id: int
    name: str
    description: str | None = None
    serial_number: str
    units: int
    power: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class RackResponse(RackCreate):
    id: int
    devices: List[DeviceInRack] = []
    used_units: int = 0 
    used_power: int = 0
    used_units_percent: float = 0.0
    used_power_percent: float = 0.0
    capacity_units: int
    max_power: int

    @field_serializer("max_power")
    def serialize_max_power(self, max_power: int) -> str:
        return f"{max_power}W"

    @field_serializer("capacity_units")
    def serialize_capacity_units(self, capacity_units: int) -> str:
        return f"{capacity_units}U"

    model_config = ConfigDict(from_attributes=True)