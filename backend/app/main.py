from fastapi import FastAPI
from app.core.db import engine
from app.routers.users import router as user_router


app = FastAPI(title="GeoTasker Back-End")
app.include_router(user_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to GeoTasker"}
