from fastapi import FastAPI
from app.core.db import engine

app = FastAPI(title="GeoTasker Back-End")

@app.get("/")
def read_root():
    return {"message": "Welcome to GeoTasker"}
