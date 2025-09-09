from typing import Optional
from pydantic import BaseModel, field_serializer, ConfigDict

class DeviceCreate(BaseModel):
    name: str
    description: str
    serial_number: str
    units: int
    power: int
    rack_id: Optional[int] = None

class DeviceResponse(DeviceCreate):
    id: int
    power: int

    @field_serializer("power")
    def serialize_power(self, power: int) -> str:
        return f"{power}W"

    class Config:
        model_config = ConfigDict(from_attributes=True)