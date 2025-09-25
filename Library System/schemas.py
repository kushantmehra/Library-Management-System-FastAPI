from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email : str
    password : str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    class Config :
        orm_mode = True

class BooksCreate(BaseModel):
    author: str
    title : str

class BooksOut(BaseModel):
    id : int
    author: str
    title : str
    available : bool
    class Config:
        orm_mode = True
