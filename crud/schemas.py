from pydantic import BaseModel
from datetime import datetime

class DeviceBase(BaseModel):
    id: str
    name: str
    is_active: bool

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(DeviceBase):
    pass

class Device(DeviceBase):
    created_at: datetime
    updated_at: datetime
    # sensors: list[Sensor] = []
    class config:
        orm_mode = True

class SensorTypeBase(BaseModel):
    id: str
    name: str
    is_active: bool

class SensorTypeCreate(SensorTypeBase):
    pass

class SensorTypeUpdate(SensorTypeBase):
    pass

class SensorType(SensorTypeBase):
    created_at: datetime
    updated_at: datetime

    class config:
        orm_mode = True

class SensorBase(BaseModel):
    id: str
    name: str
    is_active: bool
    sensor_type_id: str
    device_id: str

class SensorCreate(SensorBase):
    pass

class SensorUpdate(SensorBase):
    pass

class Sensor(SensorBase):
    created_at: datetime
    updated_at: datetime
    device: Device
    sensor_type: SensorType

    class config:
        orm_mode = True

class SensorDataBase(BaseModel):
    id: str
    value: str
    sensor_id: str
    timestamp: datetime

class SensorDataCreate(SensorDataBase):
    pass

class SensorDataUpdate(SensorDataBase):
    pass

class SensorData(SensorDataBase):
    created_at: datetime
    updated_at: datetime
    sensor: Sensor

    class config:
        orm_mode = True