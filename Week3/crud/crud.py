from sqlalchemy.orm import Session
from schema import schema
from db import model, database
from typing import Optional
from fastapi import HTTPException

def create_user(db: Session, user: schema.UserCreate):
    db_user = model.User(
        uuid=user.uuid, 
        id=user.id, 
        password=user.password, 
        name=user.name, 
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: str):
    return db.query(model.User).filter(model.User.id == user_id).first()

def get_all_users(db: Session):
    skip: int = 0
    limit: int = 100
    return db.query(model.User).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id: str):
    db_user = db.query(model.User).filter(model.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None

def create_book(db: Session, book: schema.BookCreate):
    db_book = model.Libs(id=book.id, title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book_by_id(db: Session, book_id: int):
    return db.query(model.Libs).filter(model.Libs.id == book_id).first()

def get_all_books(db: Session):
    skip: int = 0 
    limit: int = 100
    return db.query(model.Libs).offset(skip).limit(limit).all()

def update_db_book(db: Session, book_id: int, New_book: schema.Book):
    book_schema = db.query(model.Libs).filter(model.Libs.id == book_id).first()
    if book_schema:
        book_schema.title = New_book.title
        book_schema.author = New_book.author
        book_schema.published_year = New_book.published_year
        db.commit()
    return book_schema

def delete_book(db: Session, book_id: int):
    db_book = db.query(model.Libs).filter(model.Libs.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book
    return None

def search_book(db: Session,
    title: Optional[str] = None, 
    author: Optional[str] = None
    ):

    query = db.query(model.Libs)
    
    if title:
        query = query.filter(model.Libs.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(model.Libs.author.ilike(f"%{author}%"))
    
    results = query.all()
    
    """
    if results is None:
        raise HTTPException(status_code=404, datail="No books founded")
    """
    return [schema.Book(id=book.id, title=book.title, author=book.author) for book in results]
