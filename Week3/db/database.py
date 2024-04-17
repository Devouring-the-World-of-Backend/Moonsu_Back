import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine



database_URL = 'sqlite+aiosqlite:///./book.db'

engine = create_async_engine(
    database_URL, echo=False, connect_args={"check_same_thread": False} # connect_args 는 SQLite가 기본적으로 단일 스레드에서만 데이터베이스 연결을 허용하기 때문에 필요한 설정.
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

async def get_db():
    async with SessionLocal() as Session:
        yield Session

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
# Base.metadata.create_all(bind=engine)
