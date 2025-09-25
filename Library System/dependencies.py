from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError, ExpiredSignatureError
from database import SessionLocal
import model, os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY","secret")
ALGORITHM = 'HS256'

async def get_db():
    async with SessionLocal() as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme),db: AsyncSession= Depends(get_db)):
    credential_exception=  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Invalid Credentials",
                                        headers= {"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode (token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credential_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credential_exception
    
    from crud import get_user_by_username
    user = await get_user_by_username(db, username)
    if user is None:
        raise credential_exception
    return user
