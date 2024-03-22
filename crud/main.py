from fastapi import APIRouter, FastAPI
import uvicorn
from db import engine
import entities
from routes.devices import router as devices_router
from routes.sensor_types import router as sensor_types_router
from routes.sensors import router as sensors_router
from routes.sensor_data import router as sensor_data_router
from logger import logger
from middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware

router = APIRouter(prefix="/v1")
router.include_router(devices_router)
router.include_router(sensor_types_router)
router.include_router(sensors_router)
router.include_router(sensor_data_router)

entities.Base.metadata.create_all(bind = engine)

app = FastAPI()
app.include_router(router)

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

logger.info('Starting API')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
