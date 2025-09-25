from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import model, schemas, auth

async def create_user(db:AsyncSession, user: schemas.UserCreate):
    hashed_pw = auth.hash_password(user.password)
    db_user= model.User(username = user.username, email = user.email, hashed_password = hashed_pw)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_username(db:AsyncSession, username:str):
    result = await db.execute(select(model.User).where(model.User.username == username))
    return result.scalar_one_or_none()

async def create_book(db:AsyncSession, book: schemas.BooksCreate):
    db_book = model.books(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_books(db:AsyncSession):
    result = await db.execute(select(model.books))
    return result.scalars().all()
