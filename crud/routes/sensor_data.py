from fastapi import APIRouter, status, Depends, HTTPException


from db import get_db
from sqlalchemy.orm import Session
import schemas
import service


router = APIRouter(prefix="/sensor-data", tags=["sensor-data"])


@router.get("/", response_model= list[schemas.SensorData])
def get_sensor_data(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    sensordata = service.get_all_sensor_data(db, skip=skip, limit=limit)
    return sensordata

@router.get("/{sensor_data_id}", response_model=schemas.SensorData)
async def get_sensor_data_by_id(sensor_data_id: str, db: Session = Depends(get_db)):
    db_sensor_data = service.get_sensor_data_by_id(db, sensor_data_id)
    if not db_sensor_data:
        raise HTTPException(status_code=404, detail="sensor data not exists")
    return db_sensor_data

@router.post("/", response_model=schemas.SensorData, status_code=status.HTTP_201_CREATED)
async def create_sensor_data(sensor_data: schemas.SensorDataCreate, db: Session = Depends(get_db)):
    db_sensor_data = service.get_sensor_data_by_id(db, sensor_data.id)
    if db_sensor_data:
        raise HTTPException(status_code=400, detail="sensor data with id already in use")
    db_sensor_data = service.create_sensor_data(db, sensor_data)
    return db_sensor_data

@router.put("/{sensor_data_id}", response_model=schemas.SensorData)
async def update_sensor_data(sensor_data_id: str, sensor_data: schemas.SensorDataUpdate, db: Session = Depends(get_db)):
    db_sensor_data = service.get_sensor_data_by_id(db, sensor_data_id)
    if not db_sensor_data:
        raise HTTPException(status_code=404, detail="sensor data not exists")
    db_sensor_data = service.update_sensor_data(db, db_sensor_data, sensor_data)
    return db_sensor_data