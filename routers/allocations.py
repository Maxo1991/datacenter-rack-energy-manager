from fastapi import APIRouter
from database import create_connection
from crud.devices import get_devices
from crud.racks import get_all_racks
from services.allocations import allocate_devices

router = APIRouter(tags=["Allocate"])

@router.get("/allocate")
def allocate_devices_endpoint():
    conn = create_connection()
    devices = get_devices(conn)
    racks = get_all_racks(conn)
    conn.close()

    return allocate_devices(devices, racks)

