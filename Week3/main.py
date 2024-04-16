from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.staticfiles import StaticFiles
from router import route
from db.model import Base
from router import route
from db.database import engine

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(route.router)


