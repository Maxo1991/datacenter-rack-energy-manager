from fastapi import FastAPI
from routers import allocations, devices, racks

app = FastAPI(title="Data Center Devices API", version="1.0.0")

app.include_router(devices.router)
app.include_router(racks.router)
app.include_router(allocations.router)