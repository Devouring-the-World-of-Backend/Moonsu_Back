from sqlalchemy.orm import Session
from schema import schema
from db import model, database
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

async def create_user(db: AsyncSession, user: schema.UserCreate):
    db_user = model.User(
        uuid=user.uuid, 
        id=user.id, 
        password=user.password, 
        name=user.name, 
        email=user.email
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_id(db: AsyncSession, user_id: str):
    query = select(model.User).where(model.User.id == user_id)
    
    res = await db.execute(query)
    return res.scalars().first()

async def get_all_users(db: AsyncSession):
    skip: int = 0
    limit: int = 100
    query = select(model.User).offset(skip).limit(limit)
    
    res = await db.execute(query)
    return res.scalars().all()

async def delete_user(db: AsyncSession, user_id: str):
    query = select(model.User).where(model.User.id == user_id)
    tmp = await db.execute(query)
    res = tmp.scalars().first()
    
    if res:
        await db.delete(res)
        await db.commit()
        return res
    else:
        return None
    
async def create_book(db: AsyncSession, book: schema.BookCreate):
    db_book = model.Libs(
        id=book.id, 
        title=book.title, 
        author=book.author
    )
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_book_by_id(db: AsyncSession, book_id: int):
    query = select(model.Libs).where(model.Libs.id == book_id)
    
    res = await db.execute(query)
    return res.scalars().first()

async def get_all_books(db: AsyncSession):
    skip: int = 0 
    limit: int = 100
    query = select(model.Libs).offset(skip).limit(limit)
    
    res = await db.execute(query)
    return res.scalars().all()

async def update_db_book(db: AsyncSession, book_id: int, New_book: schema.BookUpdate):
    query = select(model.Libs).where(model.Libs.id == book_id)
    tmp = await db.execute(query)
    res = tmp.scalars().first()
    
    if res:
        res.title = New_book.title
        res.author = New_book.author
        await db.commit()
        await db.refresh(res)
        return res
    return None

async def delete_book(db: AsyncSession, book_id: int):
    query = select(model.Libs).where(model.Libs.id == book_id)
    tmp = await db.execute(query)
    res = tmp.scalars().first()
    
    if res:
        await db.delete(res)
        await db.commit()
        return res
    else:
        return None

async def search_book(db: AsyncSession,
    title: Optional[str] = None, 
    author: Optional[str] = None
    ):

    query = select(model.Libs)
    
    if title:
        query = query.filter(model.Libs.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(model.Libs.author.ilike(f"%{author}%"))
    
    res = await db.execute(query)
    books = res.scalars().all()

    if not books:
        raise HTTPException(status_code=404, datail="No books founded")

    return [schema.Book(id=book.id, title=book.title, author=book.author) for book in books]
