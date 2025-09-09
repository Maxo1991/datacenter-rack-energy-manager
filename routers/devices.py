from fastapi import APIRouter, HTTPException
from models.devices import DeviceUpdate
from schemas.devices import DeviceCreate, DeviceResponse
from crud import devices as crud_devices
from database import create_connection
from typing import List

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/", response_model=DeviceResponse)
def create_device(device: DeviceCreate):
    conn = create_connection()
    try:
        device_id = crud_devices.create_device(conn, device)
        return {**device.dict(), "id": device_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@router.get("/", response_model=List[DeviceResponse])
def list_devices():
    conn = create_connection()
    try:
        devices = crud_devices.get_devices(conn)
        return devices
    finally:
        conn.close()

@router.get("/{device_id}", response_model=DeviceResponse)
def get_device_endpoint(device_id: int):
    conn = create_connection()
    try:
        device = crud_devices.get_device(conn, device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        return device
    finally:
        conn.close()

@router.put("/{device_id}", response_model=DeviceResponse)
def update_device_endpoint(device_id: int, device: DeviceUpdate):
    conn = create_connection()
    try:
        existing = crud_devices.get_device(conn, device_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Device not found")

        update_data = device.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(existing, key, value)

        updated = crud_devices.update_device(conn, device_id, existing)
        if not updated:
            raise HTTPException(status_code=404, detail="Device not found")
        return {**existing.dict(), "id": device_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@router.delete("/{device_id}")
def delete_device_endpoint(device_id: int):
    conn = create_connection()
    try:
        deleted = crud_devices.delete_device(conn, device_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Device not found")
        return {"detail": "Device deleted"}
    finally:
        conn.close()