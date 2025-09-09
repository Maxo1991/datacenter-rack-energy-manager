from fastapi import APIRouter, HTTPException
from typing import List
from database import create_connection
from schemas.racks import RackCreate, RackResponse
from crud import racks as crud_racks

router = APIRouter(prefix="/racks", tags=["Racks"])

@router.post("/", response_model=RackResponse)
def create_new_rack(rack: RackCreate):
    conn = create_connection()
    try:
        rack_id = crud_racks.create_rack(conn, rack)
        return {**rack.dict(), "id": rack_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@router.get("/", response_model=List[RackResponse])
def list_racks():
    conn = create_connection()
    try:
        racks = crud_racks.get_racks_with_devices(conn)
        return racks
    finally:
        conn.close()

@router.get("/{rack_id}", response_model=RackResponse)
def get_rack_endpoint(rack_id: int):
    conn = create_connection()
    try:
        rack = crud_racks.get_rack_with_devices(conn, rack_id)
        if not rack:
            raise HTTPException(status_code=404, detail="Rack not found")
        return rack
    finally:
        conn.close()

@router.put("/{rack_id}", response_model=RackResponse)
def update_rack_endpoint(rack_id: int, rack: RackCreate):
    conn = create_connection()
    try:
        updated = crud_racks.update_rack(conn, rack_id, rack)
        if not updated:
            raise HTTPException(status_code=404, detail="Rack not found")
        return {**rack.dict(), "id": rack_id}
    finally:
        conn.close()

@router.delete("/{rack_id}")
def delete_rack_endpoint(rack_id: int):
    conn = create_connection()
    try:
        deleted = crud_racks.delete_rack(conn, rack_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Rack not found")
        return {"detail": "Rack deleted"}
    finally:
        conn.close()
