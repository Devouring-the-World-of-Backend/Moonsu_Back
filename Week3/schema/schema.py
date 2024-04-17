from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    id: int
    title: str
    author: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    
class Book(BaseModel):
    id: int
    title: str
    author: str
    user_id: Optional[int] = None

class UserCreate(BaseModel):
    uuid: int
    id: str
    password: str
    name: str
    email: str
        
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    
class UserPublic(BaseModel):
    id: str
    name: str
    email: str

class User(BaseModel):
    uuid: int
    id: str
    password: str
    name: str
    email: str

    