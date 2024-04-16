from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from db.database import Base, engine


class User(Base):
    __tablename__ = 'users'
    
    uuid = Column(Integer, primary_key=True)
    id = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    libs = relationship("Libs", back_populates="users")
    
class Libs(Base):
    __tablename__ = 'libs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.uuid'), nullable=True)
    
    users = relationship("User", back_populates="libs")
    
class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    
