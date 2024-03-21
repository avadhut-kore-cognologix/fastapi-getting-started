from sqlalchemy.orm import Session
import schemas
from entities import Device, Sensor, SensorData, SensorType

# get device by device_id
def get_device_by_id(db: Session, device_id: str):
    return db.query(Device).filter(Device.id == device_id).first()

# get all devices
def get_all_devices(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Device).offset(skip).limit(limit).all()

# create device
def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = Device(**device.model_dump())
    db.add(db_device)
    db.commit()
    return db_device

# Update device
def update_device(db: Session, db_device: Device, device_update: schemas.DeviceUpdate):
    db_device.name = device_update.name or db_device.name
    db_device.is_active = device_update.is_active
    db.commit()
    db.refresh(db_device)
    return db_device

# get all sensor types
def get_all_sensor_types(db: Session, skip: int = 0, limit: int = 20):
    return db.query(SensorType).offset(skip).limit(limit).all()

# get sensor type by id
def get_sensor_type_by_id(db: Session, sensor_type_id: str):
    return db.query(SensorType).filter(SensorType.id == sensor_type_id).first()

# create sensor type
def create_sensor_type(db: Session, sensor_type: schemas.SensorTypeCreate):
    db_sensor_type = SensorType(**sensor_type.model_dump())
    db.add(db_sensor_type)
    db.commit()
    return db_sensor_type

# Update sensor type
def update_sensor_type(db: Session, db_sensor_type: SensorType, sensor_type_update: schemas.SensorTypeUpdate):
    db_sensor_type.name = sensor_type_update.name or db_sensor_type.name    
    db_sensor_type.is_active = sensor_type_update.is_active
    db.commit()
    db.refresh(db_sensor_type)
    return db_sensor_type

# get device sensors
def get_device_sensors(db: Session, device_id: str):
    return db.query(Sensor).filter(Sensor.device_id == device_id).all()

# get all sensors
def get_all_sensors(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Sensor).offset(skip).limit(limit).all()

# get sensor by id
def get_sensor_by_id(db: Session, sensor_id: str):
    return db.query(Sensor).filter(Sensor.id == sensor_id).first()

# create sensor
def create_sensor(db: Session, sensor: schemas.SensorCreate):
    db_sensor = Sensor(**sensor.model_dump())
    db.add(db_sensor)
    db.commit()
    return db_sensor

# Update sensor
def update_sensor(db: Session, db_sensor: Sensor, sensor_update: schemas.SensorUpdate):
    db_sensor.name = sensor_update.name or db_sensor.name
    db_sensor.sensor_type_id = sensor_update.sensor_type_id or db_sensor.sensor_type_id
    db_sensor.device_id = sensor_update.device_id or db_sensor.device_id
    db_sensor.is_active = sensor_update.is_active
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

# get all sensor_data
def get_all_sensor_data(db: Session, skip: int = 0, limit: int = 20):
    return db.query(SensorData).offset(skip).limit(limit).all()

# get sensor data by id
def get_sensor_data_by_id(db: Session, sensor_data_id: str):
    return db.query(SensorData).filter(SensorData.id == sensor_data_id).first()

# get sensor data by sensor id
def get_sensor_data_by_sensor_id(db: Session, sensor_id: str):
    return db.query(SensorData).filter(SensorData.sensor_id == sensor_id).all()

# create sensor data
def create_sensor_data(db: Session, sensor_data: schemas.SensorDataCreate):
    db_sensor_data = SensorData(**sensor_data.model_dump())
    db.add(db_sensor_data)
    db.commit()
    return db_sensor_data

# Update sensor data
def update_sensor_data(db: Session, db_sensor_data: SensorData, sensor_data_update: schemas.SensorDataUpdate):
    db_sensor_data.value = sensor_data_update.value or db_sensor_data.value
    db_sensor_data.sensor_id = sensor_data_update.sensor_id or db_sensor_data.sensor_id
    db.commit()
    db.refresh(db_sensor_data)
    return db_sensor_data