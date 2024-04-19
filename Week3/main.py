from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.staticfiles import StaticFiles
from router import route
from db.model import Base, engine
from router import route
from db.database import init_db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(route.router)

@app.on_event("startup")
async def on_startup():
    await init_db()