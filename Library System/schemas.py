from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")

class UserCreate(BaseModel):
    username: str
    email : str
    password : str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    class Config :
        from_attributes = True

class BooksCreate(BaseModel):
    author: str
    title : str

class BooksOut(BaseModel):
    id : int
    author: str
    title : str
    available : bool
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str]= None
    email: Optional[str]= None
    password: Optional[str]= None

class BookUpdate(BaseModel):
    author:Optional[str]= None
    title: Optional[str]= None
    available : Optional[bool]= None

class LoanBase(BaseModel):
    book_id:int
    due_date: datetime = Field(default_factory=lambda: datetime.now(IST))

class LoanOut(BaseModel):
    id : int
    user_id:int
    book_id: int
    borrowed_at : datetime
    due_date : datetime
    returned_at: datetime| None
    fine: float

    class Config:
        from_attributes = True
