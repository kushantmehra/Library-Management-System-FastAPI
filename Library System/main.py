from fastapi import FastAPI, Depends, HTTPException,Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import model, schemas, crud, auth, dependencies
from database import engine, Base

app = FastAPI(title="Library Management System")

# Create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Auth token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(dependencies.get_db)):
    user = await crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "Bearer"}

# User
@app.post("/users/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(dependencies.get_db)):
    db_user = await crud.create_user(db, user)
    return db_user

@app.put("/user/{id}", response_model=schemas.UserUpdate)
async def update_user(user_in : schemas.UserUpdate,
                    db: AsyncSession = Depends(dependencies.get_db),
                    current_user : model.User = Depends(dependencies.get_current_user)):
    updated = await crud.update_user(db, current_user.id, user_in)
    return updated

@app.delete("/user/{id}")
async def delete_book(db: AsyncSession = Depends(dependencies.get_db),
                      current_user: model.User = Depends(dependencies.get_current_user)):
    return await crud.delete_user(db, current_user.id)

# Books
@app.post("/books/", response_model=schemas.BooksOut)
async def add_book(book: schemas.BooksCreate, db: AsyncSession = Depends(dependencies.get_db), current_user: model.User = Depends(dependencies.get_current_user)):
    return await crud.create_book(db, book)

@app.get("/books/", response_model=list[schemas.BooksOut])
async def list_books(db: AsyncSession = Depends(dependencies.get_db)):
    return await crud.get_books(db)

@app.put("/books/{id}", response_model=schemas.BookUpdate)
async def update_book(
    book_id:int = Path(...,ge=1),
    book_in : schemas.BookUpdate = Depends(),
    db:AsyncSession= Depends(dependencies.get_db),
    current_user : model.User = Depends(dependencies.get_current_user)
):
    updated = await crud.update_book(db, book_id, book_in)
    return updated

@app.delete("/books/{id}")
async def delete_book(book_id : int = Path(..., ge=1),
                      db:AsyncSession= Depends(dependencies.get_db),
                      current_user: model.User =  Depends(dependencies.get_current_user)):
    return await crud.delete_book(db, book_id)
