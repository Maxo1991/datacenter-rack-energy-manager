from pydantic import BaseModel, ConfigDict
from typing import List
from models.devices import Device

class RackBase(BaseModel):
    name: str
    description: str
    serial_number: str
    capacity_units: int
    max_power: int

class RackCreate(RackBase):
    pass

class RackUpdate(RackBase):
    pass

class Rack(RackBase):
    id: int
    devices: List["Device"] = []

    class Config:
        model_config = ConfigDict(from_attributes=True)

class RackAllocation(BaseModel):
    rack_id: int
    rack_name: str
    devices: List[str]
    power_usage_percent: float
    
Rack.model_rebuild()