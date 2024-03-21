from fastapi import APIRouter, status, Depends, HTTPException


from db import get_db
from sqlalchemy.orm import Session
import schemas
import service


router = APIRouter(prefix="/sensor-types", tags=["sensor-types"])


@router.get("/", response_model= list[schemas.SensorType])
def get_sensor_types(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    sensor_types = service.get_all_sensor_types(db, skip=skip, limit=limit)
    return sensor_types

@router.get("/{sensor_type_id}", response_model=schemas.SensorType)
async def get_sensor_type_by_id(sensor_type_id: str, db: Session = Depends(get_db)):
    db_sensor_type = service.get_sensor_type_by_id(db, sensor_type_id)
    if not db_sensor_type:
        raise HTTPException(status_code=404, detail="sensor type not exists")
    return db_sensor_type

@router.post("/", response_model=schemas.SensorType, status_code=status.HTTP_201_CREATED)
async def create_sensor_type(sensor_type: schemas.SensorTypeCreate, db: Session = Depends(get_db)):
    db_sensor_type = service.get_sensor_type_by_id(db, sensor_type.id)
    if db_sensor_type:
        raise HTTPException(status_code=400, detail="sensor type already in use")
    db_sensor_type = service.create_sensor_type(db, sensor_type)
    return db_sensor_type

@router.put("/{sensor_type_id}", response_model=schemas.SensorType)
async def update_sensor_type(sensor_type_id: str, sensor_type: schemas.SensorTypeUpdate, db: Session = Depends(get_db)):
    db_sensor_type = service.get_sensor_type_by_id(db, sensor_type_id)
    if not db_sensor_type:
        raise HTTPException(status_code=404, detail="sensor type not exists")
    db_sensor_type = service.update_sensor_type(db, db_sensor_type, sensor_type)
    return db_sensor_type