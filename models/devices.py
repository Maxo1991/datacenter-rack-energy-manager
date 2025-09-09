from pydantic import BaseModel, ConfigDict
from typing import Optional

class DeviceBase(BaseModel):
    name: str
    description: str
    serial_number: str
    units: int
    power: int
    rack_id: Optional[int] = None 

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    name: str
    description: str
    serial_number: str
    units: int
    power: int
    rack_id: Optional[int] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)

class Device(DeviceBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)
