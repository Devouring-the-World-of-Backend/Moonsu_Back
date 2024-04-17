from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from db.database import Base, engine

lib_category = Table(
    'lib_category',
    Base.metadata,
    Column('lib_id', Integer, ForeignKey('libs.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    
    uuid = Column(Integer, primary_key=True)
    id = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    libs_borrowed = relationship("Libs", back_populates="borrowed_by")
    
class Libs(Base):
    __tablename__ = 'libs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.uuid'), nullable=True)
    
    borrowed_by = relationship("User", back_populates="libs_borrowed")
    
class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    libs = relationship("Libs", secondary=lib_category, back_populates="categories")
    
