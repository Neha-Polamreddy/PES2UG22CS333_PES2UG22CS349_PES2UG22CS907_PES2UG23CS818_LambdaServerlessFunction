# backend/main.py

from fastapi import FastAPI, HTTPException
from .database import database, engine, metadata
from typing import List
from pydantic import BaseModel
from sqlalchemy.sql import select, insert, update, delete
from .models import functions
# from fastapi import  Depends

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


# Define Pydantic models for request/response


class FunctionBase(BaseModel):
    name: str
    route: str
    language: str
    timeout: int


class FunctionCreate(FunctionBase):
    pass


class Function(FunctionBase):
    id: int

    class Config:
        orm_mode = True


# CRUD endpoints


@app.post("/functions/", response_model=Function)
async def create_function(function: FunctionCreate):
    query = insert(functions).values(**function.dict())
    last_record_id = await database.execute(query)

    # Return the created function
    return {**function.dict(), "id": last_record_id}


@app.get("/functions/", response_model=List[Function])
async def read_functions():
    query = select(functions)
    return await database.fetch_all(query)


@app.get("/functions/{function_id}", response_model=Function)
async def read_function(function_id: int):
    query = select(functions).where(functions.c.id == function_id)
    function = await database.fetch_one(query)

    if function is None:
        raise HTTPException(status_code=404, detail="Function not found")

    return function


@app.put("/functions/{function_id}", response_model=Function)
async def update_function(function_id: int, function: FunctionBase):
    # Check if function exists
    query = select(functions).where(functions.c.id == function_id)
    existing_function = await database.fetch_one(query)

    if existing_function is None:
        raise HTTPException(status_code=404, detail="Function not found")

    # Update function
    query = (
        update(functions).where(functions.c.id == function_id).values(**function.dict())
    )
    await database.execute(query)

    # Return updated function
    return {**function.dict(), "id": function_id}


@app.delete("/functions/{function_id}", response_model=Function)
async def delete_function(function_id: int):
    # Check if function exists
    query = select(functions).where(functions.c.id == function_id)
    existing_function = await database.fetch_one(query)

    if existing_function is None:
        raise HTTPException(status_code=404, detail="Function not found")

    # Delete function
    query = delete(functions).where(functions.c.id == function_id)
    await database.execute(query)

    # Return deleted function
    return existing_function


# <--- Add a blank line here!
