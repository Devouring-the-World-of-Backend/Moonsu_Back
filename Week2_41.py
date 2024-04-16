from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

app = FastAPI()


class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    description: str
    published_year: int

    @field_validator("published_year")
    def validate_published_year(cls, value):
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError('published_year must not be in the future.')
        return value
        
        
fake_data = {
    "id": 1,
    "title": "노인",
    "author": "나",
    "description": "자고 싶어요..",
    "published_year": 2024,
}


books_db: List[Book] = [Book(**fake_data)]  # Fake DB

@app.exception_handler(HTTPException)
async def NoSearchWord_exception_handler(requset, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )
    
# 심화 기능 - 도서 검색 대충 인터넷 검색 해보니까 경로가 겹치는 문제가 있었음...
@app.get("/books/search/", response_model=List[Book])
def search_book(
    title: Optional[str] = None, 
    author: Optional[str] = None, 
    published_year: Optional[int] = None
    ):
    if title == None and author == None and published_year == None:
        raise HTTPException(status_code = 400, detail="There is No Keyword!")
    results = books_db
    if title:
        tempresult = []
        for data in results:
            if title.lower() in data.title.lower():
                tempresult.append(data)
        results = tempresult
    if author:
        tempresult = []
        for data in results:
            if author.lower() in data.author.lower():
                tempresult.append(data)
        results = tempresult
    if published_year:
        tempresult = []
        for data in results:
            if published_year == data.published_year:
                tempresult.append(data)
        results = tempresult
    return results
    


@app.post("/books/", status_code=201, response_model=Book)
def add_book(book: Book):
    book.id = len(books_db) + 1
    books_db.append(book)
    return book


@app.get("/books/", response_model=List[Book])
def read_books():
    return books_db


@app.get("/books/{book_id}/", response_model=Book)
def read_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}/", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            updated_book.id = book_id
            books_db[index] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}/")
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[index]
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")






