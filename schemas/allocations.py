from pydantic import BaseModel
from typing import List

class RackAllocation(BaseModel):
    rack_id: int
    rack_name: str
    devices: List[str]
    power_usage_percent: float
