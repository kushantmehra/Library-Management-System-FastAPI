from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index= True)
    username= Column(String, unique= True, index = True)
    email = Column(String, unique=True, index= True)
    hashed_password = Column (String)

class books(Base):
    __tablename__ = "books"

    id = Column (Integer, primary_key=True, index=True)
    title = Column(String,index=True)
    author= Column (String, index=True)
    available = Column(Boolean, default=True)

