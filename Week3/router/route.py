from fastapi import APIRouter, HTTPException, Depends
from schema import schema
from crud import crud
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from typing import List, Optional

router = APIRouter()


@router.post("/users/", status_code=201, response_model=schema.UserCreate)
async def create_user(user: schema.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.create_user(db, user)
    return db_user

@router.get("/users/", response_model=List[schema.User])
async def get_users(db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_all_users(db)
    return [schema.User(uuid=user.uuid, id=user.id, password=user.password, name=user.name, email=user.email) for user in db_user]

@router.get("/users/{user_id}", response_model=schema.UserPublic)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schema.UserPublic(id=user.id, name=user.name, email=user.email) 

@router.delete("/users/{user_id}/", status_code=201)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    db_user = await crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_user
  
@router.get("/books/search/", response_model=List[schema.Book])
async def router_search_book(
    title: Optional[str] = None, 
    author: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    ):
    if title == None and author == None:
        raise HTTPException(status_code = 400, detail="There is No Keyword!")
    db_book = await crud.search_book(db, title, author)
    if db_book is None:
        raise HTTPException(status_code= 404, detail="No books founded")
    return db_book

@router.post("/books/", status_code=201, response_model=schema.BookCreate)
async def create_book(book: schema.BookCreate, db: AsyncSession = Depends(get_db)):
    db_book = await crud.create_book(db, book)
    return db_book

@router.get("/books/", response_model=List[schema.Book])
async def get_books(db: AsyncSession = Depends(get_db)):
    libraries = await crud.get_all_books(db)
    return [schema.Book(id=lib.id, title=lib.title, author=lib.author, user_id=lib.user_id) for lib in libraries]

@router.get("/books/{book_id}/", response_model=schema.Book)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await crud.get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return schema.Book(id=book.id, title=book.title, author=book.author, user_id=book.user_id)

# db에서 특정 도서를 업데이트
@router.put("/books/{book_id}/")
async def update_book(book_id: int, updated_book: schema.BookUpdate, db: AsyncSession = Depends(get_db)):
    book = await crud.update_db_book(db, book_id, updated_book)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return schema.Book(id=book.id, title=book.title, author=book.author)


@router.delete("/books/{book_id}/", status_code=201)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.delete_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.put("/books/{book_id}/borrow/")
async def borrow_book(book_id: int, user_uuid: int, db: AsyncSession = Depends(get_db)):
    return await crud.borrow_book(db, book_id, user_uuid)

@router.put("/books/{book_id}/return/")
async def return_book(book_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.return_book(db, book_id, user_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book