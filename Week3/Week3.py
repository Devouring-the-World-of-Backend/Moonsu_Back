"""from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from databases import Database

import os

Base = declarative_base()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    libs = relationship("Libs", back_populates="owner")
    
class Libs(Base):
    __tablename__ = 'libs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    published_year = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    owner = relationship("User", back_populates="libs")


SQLALCHEMY_DB_URL = "sqlite:///./book.db"
engine = create_engine(
    SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False} # connect_args 는 SQLite가 기본적으로 단일 스레드에서만 데이터베이스 ㅇ녀결을 허용하기 때문에 필요한 설정.
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
# SessionLocal은 SQLAlchemy 세션을 생성하는 팩토리로, 데이터베이스와의 상호작용을 위해 사용됨.
    
Base.metadata.create_all(bind=engine)
database = Database(SQLALCHEMY_DB_URL)

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    published_year: int

    @field_validator("published_year")
    def validate_published_year(cls, value):
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError('published_year must not be in the future.')
        return value

def create_user(session, name, email):
    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()
    return new_user

def create_book(session, book: Book):
    library = Libs(title=book.title, author=book.author, published_year=book.published_year)
    session.add(library)
    session.commit()
    return library

def get_user(session, user_id):
    return session.query(User).filter(User.id == user_id).first()

def get_book_by_id(session, book_id: int):
    return session.query(Libs).filter(Libs.id == book_id).first()

def get_all_books(session):
    return session.query(Libs).all()

def update_user_name(session, user_id, new_name):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.name = new_name
        session.commit()
    return user

def update_db_book(session, book_id: int, New_book: Book):
    book = session.query(Libs).filter(Libs.id == book_id).first()
    if book:
        book.title = New_book.title
        book.author = New_book.author
        book.published_year = New_book.published_year
        session.commit()
    return book

def delete_user(session, user_id):
    user_to_delete = session.query(User).filter(User.id == user_id).first()
    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()

@app.exception_handler(HTTPException)
async def NoSearchWord_exception_handler(requset, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


@app.get("/books/search/", response_model=List[Book])
def search_book(
    title: Optional[str] = None, 
    author: Optional[str] = None, 
    published_year: Optional[int] = None
    ):
    if title == None and author == None and published_year == None:
        raise HTTPException(status_code = 400, detail="There is No Keyword!")
    query = db.query(Libs)
    
    if title:
        query = query.filter(Libs.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Libs.author.ilike(f"%{author}%"))
    if published_year:
       query = query.filter(Libs.published_year.ilike(f"%{published_year}%"))
    
    results = query.all()
    
    if results is None:
        raise HTTPException(status_code=404, datail="No books founded")
    
    return [Book(id=book.id, title=book.title, author=book.author, published_year=book.published_year) for book in results]
    
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

        
# db에 도서 추가
@app.post("/books/", status_code=201, response_model=Book)
def add_book(book: Book):
    create_book(db, book)
    return book
# db로부터 모든 도서 호출
@app.get("/books/", response_model=List[Book])
def read_books():
    libraries = get_all_books(db)
    return [Book(id=lib.id, title=lib.title, author=lib.author, published_year=lib.published_year) for lib in libraries]
# db로부터 특정 도서 호출
@app.get("/books/{book_id}/", response_model=Book)
def read_book(book_id: int):
    book = get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(id=book.id, title=book.title, author=book.author, published_year=book.published_year)
# db에서 특정 도서를 업데이트
@app.put("/books/{book_id}/", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    book = update_db_book(db, book_id, updated_book)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(id=book.id, title=book.title, author=book.author, published_year=book.published_year)

# db에서 특정 도서를 삭제
@app.delete("/books/{book_id}/", status_code=201)
async def delete_book(book_id: int):
    query = Libs.__table__.delete().where(Libs.id == book_id)
    result = await database.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}




"""