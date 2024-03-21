from fastapi import APIRouter, status, Depends, HTTPException


from db import get_db
from sqlalchemy.orm import Session
import schemas
import service


router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.get("/", response_model= list[schemas.Sensor])
def get_sensors(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    sensors = service.get_all_sensors(db, skip=skip, limit=limit)
    return sensors

@router.get("/{sensor_id}", response_model=schemas.Sensor)
async def get_sensor_by_id(sensor_id: str, db: Session = Depends(get_db)):
    db_sensor = service.get_sensor_by_id(db, sensor_id)
    if not db_sensor:
        raise HTTPException(status_code=404, detail="sensor not exists")
    return db_sensor

@router.get("/data/{sensor_id}", response_model= list[schemas.SensorData])
async def get_sensor_data_by_sensor_id(sensor_id: str, db: Session = Depends(get_db)):
    db_sensor_data = service.get_sensor_data_by_sensor_id(db, sensor_id)
    return db_sensor_data

@router.post("/", response_model=schemas.Sensor, status_code=status.HTTP_201_CREATED)
async def create_sensor(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    db_sensor = service.get_sensor_by_id(db, sensor.id)
    if db_sensor:
        raise HTTPException(status_code=400, detail="sensor already in use")
    db_sensor = service.create_sensor(db, sensor)
    return db_sensor

@router.put("/{sensor_id}", response_model=schemas.Sensor)
async def update_sensor(sensor_id: str, sensor: schemas.SensorUpdate, db: Session = Depends(get_db)):
    db_sensor = service.get_sensor_by_id(db, sensor_id)
    if not db_sensor:
        raise HTTPException(status_code=404, detail="sensor not exists")
    db_sensor = service.update_sensor(db, db_sensor, sensor)
    return db_sensor