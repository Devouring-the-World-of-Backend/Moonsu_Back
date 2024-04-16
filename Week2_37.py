from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    published_year: int


fake_id = 1
fake_data = {
    "id": fake_id,
    "title": "노인",
    "author": "나",
    "description": "자고 싶어요..",
    "published_year": 2024,
}
fake_id += 1


books = [Book(**fake_data)]


@app.get("/book")
async def read_book():
    return books

