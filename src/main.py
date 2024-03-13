"""
Application File
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import models
from database.db import engine
from api.router import router
from utils.data_generator import DataGenerator
from utils.solutions import SolutionGenerator


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    await DataGenerator().init_db()
    await SolutionGenerator().generate_solutions_bank()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="SQL-Practice Project",
    description="SQL-Practice Project",
    version="0.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")


# include router
app.include_router(router, prefix="/api")


@app.get("/api")
def root():
    return {"message": "Hello World"}
