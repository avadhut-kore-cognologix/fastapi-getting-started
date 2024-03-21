from fastapi import APIRouter, status, Depends, HTTPException


from db import get_db
from sqlalchemy.orm import Session
import schemas
import service


router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model= list[schemas.Device])
def get_devices(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    devices = service.get_all_devices(db, skip=skip, limit=limit)
    return devices

@router.get("/{device_id}", response_model=schemas.Device)
async def get_device_by_id(device_id: str, db: Session = Depends(get_db)):
    db_device = service.get_device_by_id(db, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="device not exists")
    return db_device

@router.get("/sensors/{device_id}", response_model= list[schemas.Sensor])
async def get_device_sensors(device_id: str, db: Session = Depends(get_db)):
    db_sensors = service.get_device_sensors(db, device_id)
    return db_sensors

@router.post("/", response_model=schemas.Device, status_code=status.HTTP_201_CREATED)
async def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_device = service.get_device_by_id(db, device.id)
    if db_device:
        raise HTTPException(status_code=400, detail="device already in use")
    db_device = service.create_device(db, device)
    return db_device

@router.put("/{device_id}", response_model=schemas.Device)
async def update_device(device_id: str, device: schemas.DeviceUpdate, db: Session = Depends(get_db)):
    db_device = service.get_device_by_id(db, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="device not exists")
    db_device = service.update_device(db, db_device, device)
    return db_device