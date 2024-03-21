from db import Base
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(String, primary_key=True)
    name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    # 1:M mapping : one device can own multiple notes
    sensors = relationship("Sensor", back_populates="device")

class SensorType(Base):
    __tablename__ = "sensor_types"

    id = Column(String, primary_key=True)
    name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(String, primary_key=True)
    name = Column(String)
    sensor_type_id = Column(String, ForeignKey("sensor_types.id"))
    device_id = Column(String, ForeignKey("devices.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # 1:1 mapping : one sensor owned by one device
    device = relationship("Device", back_populates="sensors")
    # 1:1 mapping : one sensor is of type one device
    sensor_type = relationship("SensorType")
    # 1:M mapping : one sensor can have multiple data values
    sensor_data = relationship("SensorData", back_populates="sensor")

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(String, primary_key=True)
    value = Column(String)
    sensor_id = Column(String, ForeignKey("sensors.id"))
    timestamp = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # 1:1 mapping : one sensordata relates to one sensor
    sensor = relationship("Sensor", back_populates="sensor_data")