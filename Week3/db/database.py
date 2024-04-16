import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine



database_URL = 'sqlite:///./book.db'

engine = create_engine(
    database_URL, echo=False # connect_args 는 SQLite가 기본적으로 단일 스레드에서만 데이터베이스 연결을 허용하기 때문에 필요한 설정.
)

Session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()

Base.metadata.create_all(bind=engine)
