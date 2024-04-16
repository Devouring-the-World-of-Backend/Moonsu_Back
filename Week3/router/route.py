from fastapi import APIRouter, HTTPException, Depends
from schema import schema
from crud import crud
from db.database import Session
from typing import List, Optional

router = APIRouter()
"""
def get_db(): # 나중에 비동기 설정할 에정.
    asnyc_session = SessionLocal()
    try:
        yield asnyc_session
    finally:
        asnyc_session.close()
"""     

@router.post("/users/", status_code=201, response_model=schema.UserCreate)
def create_user(user: schema.UserCreate):
    db = Session()
    db_user = crud.create_user(db, user)
    db.close()
    return db_user

@router.get("/users/", response_model=List[schema.User])
def get_users():
    db = Session()
    db_user = crud.get_all_users(db)
    db.close()
    return [schema.User(uuid=user.uuid, id=user.id, password=user.password, name=user.name, email=user.email) for user in db_user]

@router.get("/users/{user_id}", response_model=schema.Book)
def get_user(user_id: str):
    db = Session()
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.close()
    return schema.User(id=user.id, name=user.name, email=user.email) 

@router.delete("/users/{user_id}/", status_code=201)
def delete_user(user_id: str):
    db = Session()
    db_user = crud.delete_user(db=db, user_id = user_id)
    db.close()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_user
  
@router.get("/books/search/", response_model=List[schema.Book])
def router_search_book(
    title: Optional[str] = None, 
    author: Optional[str] = None
    ):
    db = Session()
    if title == None and author == None:
        raise HTTPException(status_code = 400, detail="There is No Keyword!")
    db_book = crud.search_book(db, title, author)
    if db_book is None:
        raise HTTPException(status_code= 404, detail="No books founded")
    db.close()
    return db_book

@router.post("/books/", status_code=201, response_model=schema.BookCreate)
def create_book(book: schema.BookCreate):
    db = Session()
    db_book = crud.create_book(db, book)
    db.close()
    return db_book

@router.get("/books/", response_model=List[schema.Book])
def get_books():
    db = Session()
    libraries = crud.get_all_books(db)
    db.close()
    return [schema.Book(id=lib.id, title=lib.title, author=lib.author) for lib in libraries]

@router.get("/books/{book_id}/", response_model=schema.Book)
def get_book(book_id: int):
    db = Session()
    book = crud.get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.close()
    return schema.Book(id=book.id, title=book.title, author=book.author)

# db에서 특정 도서를 업데이트
@router.put("/books/{book_id}/", response_model=schema.Book)
def update_book(book_id: int, updated_book: schema.Book):
    db = Session()
    book = crud.update_db_book(db, book_id, updated_book)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.close()
    return book.Book(id=book.id, title=book.title, author=book.author)


@router.delete("/books/{book_id}/", status_code=201)
def delete_book(book_id: int):
    db = Session()
    db_book = crud.delete_book(db=db, book_id = book_id)
    db.close()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
