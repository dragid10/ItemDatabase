from contextlib import asynccontextmanager

from fastapi import FastAPI

app: FastAPI = FastAPI()

# class

def create_db_and_tables():
    pass


@asynccontextmanager
async def lifecycle(app: FastAPI):
    create_db_and_tables()
    yield
    close_db_connection()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
