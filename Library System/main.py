from fastapi import FastAPI, Depends, HTTPException,Path,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import model, schemas, crud, auth, dependencies
from database import engine, Base
from datetime import datetime

app = FastAPI(title="Library Management System")

# Create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def home():
    message = "Welcome to Library Management System"
    return message

# Auth token
@app.post("/token",tags=["Access Token"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(dependencies.get_db)):
    user = await crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "Bearer"}

# User
@app.post("/users/", response_model=schemas.UserOut, tags= ["User"])
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(dependencies.get_db)):
    db_user = await crud.create_user(db, user)
    return db_user

@app.put("/user/{user_id}", response_model=schemas.UserUpdate, tags= ["User"])
async def update_user(user_in : schemas.UserUpdate,
                    db: AsyncSession = Depends(dependencies.get_db),
                    current_user : model.User = Depends(dependencies.get_current_user)):
    updated = await crud.update_user(db, current_user.id, user_in)
    return updated

@app.delete("/user/{user_id}", tags= ["User"])
async def delete_user(db: AsyncSession = Depends(dependencies.get_db),
                      current_user: model.User = Depends(dependencies.get_current_user)):
    return await crud.delete_user(db, current_user.id)

# Books
@app.post("/books/", response_model=schemas.BooksOut, tags= ["Book"])
async def add_book(book: schemas.BooksCreate, db: AsyncSession = Depends(dependencies.get_db), current_user: model.User = Depends(dependencies.get_current_user)):
    return await crud.create_book(db, book)

@app.get("/books/", response_model=list[schemas.BooksOut], tags= ["Book"])
async def list_books(db: AsyncSession = Depends(dependencies.get_db)):
    return await crud.get_books(db)

@app.put("/books/{book_id}", response_model=schemas.BookUpdate, tags= ["Book"])
async def update_book(
    book_id:int = Path(...,ge=1),
    book_in : schemas.BookUpdate = Depends(),
    db:AsyncSession= Depends(dependencies.get_db),
    current_user : model.User = Depends(dependencies.get_current_user)
):
    updated = await crud.update_book(db, book_id, book_in)
    return updated

@app.delete("/books/{book_id}", tags= ["Book"])
async def delete_book(book_id : int = Path(..., ge=1),
                      db:AsyncSession= Depends(dependencies.get_db),
                      current_user: model.User =  Depends(dependencies.get_current_user)):
    return await crud.delete_book(db, book_id)

# Borrow

@app.post("/borrow/", response_model=schemas.LoanOut, tags=["Borrow"])
async def borrow_book(
    loan_in : schemas.LoanBase,
    db : AsyncSession = Depends(dependencies.get_db),
    current_user: model.User = Depends(dependencies.get_current_user)
):
    return await crud.borrow_book(db,current_user.id, loan_in)

@app.post("/return/{loan_id}", response_model =  schemas.LoanOut, tags=["Borrow"])
async def return_book( loan_id: int = Path(...,ge =1),
                      db:AsyncSession = Depends(dependencies.get_db),
                      current_user: model.User = Depends(dependencies.get_current_user)):
    return await crud.return_book(db,current_user.id, loan_id)

@app.get("/my-loans/",response_model=list[schemas.LoanOut], tags=["User"])
async def my_loans(
    db:AsyncSession= Depends(dependencies.get_db),
    current_user: model.User = Depends(dependencies.get_current_user)):
    
    return await crud.get_user_loans(db, current_user.id)
