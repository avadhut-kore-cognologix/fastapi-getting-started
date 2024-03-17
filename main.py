from fastapi import FastAPI, Request, status
import uvicorn
from fastapi.responses import JSONResponse
from exceptions import MyException
from routes import router
from db import SessionLocal, engine
import models

models.Base.metadata.create_all(bind = engine)

app = FastAPI()
app.include_router(router)

@app.exception_handler(MyException)
async def my_exception_handler(request: Request, exec: MyException):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"my_detail":f"item with item_id = {exec.item_id} not found"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
