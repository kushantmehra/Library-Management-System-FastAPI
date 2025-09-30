from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")
def ist_now():
    return datetime.now(IST)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index= True)
    username= Column(String, unique= True, index = True)
    email = Column(String, unique=True, index= True)
    hashed_password = Column (String)

    loans= relationship("loan",back_populates ="user")

class books(Base):
    __tablename__ = "books"

    id = Column (Integer, primary_key=True, index=True)
    title = Column(String,index=True)
    author= Column (String, index=True)
    available = Column(Boolean, default=True)

    loans= relationship("loan", back_populates = "book")

class loan(Base):
    __tablename__= "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id= Column(Integer, ForeignKey("users.id"))
    book_id= Column(Integer,ForeignKey("books.id"))
    borrowed_at = Column(DateTime, default=ist_now)
    due_date = Column(DateTime, default=lambda: datetime.now(IST))
    returned_at= Column(DateTime, nullable=True)
    fine = Column(Float, default=0.0)

    user = relationship("User", back_populates="loans")
    book = relationship("books",back_populates="loans")
