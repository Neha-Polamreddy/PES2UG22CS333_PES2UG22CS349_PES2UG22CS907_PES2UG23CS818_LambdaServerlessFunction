# backend/main.py

from fastapi import FastAPI
from .database import database, engine, metadata
from .models import functions  # Import your SQLAlchemy models

app = FastAPI()

# Create all tables
metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/ping")
def ping():
    return {"message": "pong"}