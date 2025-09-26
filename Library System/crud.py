from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import model, schemas, auth
from fastapi import HTTPException, status

#USERS
async def create_user(db:AsyncSession, user: schemas.UserCreate):
    hashed_pw = auth.hash_password(user.password)
    db_user= model.User(username = user.username, email = user.email, hashed_password = hashed_pw)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Username or Email already Exists.")

async def get_user_by_username(db:AsyncSession, username:str):
    result = await db.execute(select(model.User).where(model.User.username == username))
    return result.scalar_one_or_none()

async def get_user_id(db: AsyncSession, user_id : int):
    result = await db.execute(select(model.User).where(model.User.id == user_id))
    return result.scalar_one_or_none()

async def update_user(db: AsyncSession, user_id: int, user_in: schemas.UserUpdate):
    db_user = await get_user_id(db,user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")
    update_data=user_in.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = auth.hash_password(update_data.pop("password"))
    for key, value in update_data.items():
        setattr(db_user,key,value)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id :int):
    db_user = await get_user_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User Not Found")
    await db.delete(db_user)
    await db.commit()
    return{"OK":True}

#BOOKS
async def create_book(db:AsyncSession, book: schemas.BooksCreate):
    db_book = model.books(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_books(db:AsyncSession):
    result = await db.execute(select(model.books))
    return result.scalars().all()

async def get_book_by_id(db: AsyncSession, book_id: int):
    result = await db.execute(select(model.books).where(model.books.id == book_id))
    return result.scalar_one_or_none()

async def update_book(db:AsyncSession, book_id : int,book_in :schemas.BookUpdate):
    db_book= await get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Book Not Found")
    update_data =book_in.dict(exclude_unset= True)
    for key,value in update_data.items():
        setattr(db_book,key,value)
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id : int):
    db_book = await get_book_by_id(db, book_id)
    if not db_book :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")
    await db.delete(db_book)
    await db.commit()
    return{"OK",True}

