from fastapi import FastAPI
import uvicorn
from auth import auth_router
from database import engine
import models

models.Base.metadata.create_all(bind = engine)

app = FastAPI()
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
