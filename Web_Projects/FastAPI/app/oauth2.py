from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schema,models
from .database import get_db
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_schema=OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,[ALGORITHM])
        id:str=payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data=schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    print(token_data)
    return token_data

def get_current_user(token:str=Depends(oauth2_schema),db: Session = Depends(get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="could not validate credentials",headers={"WWW-Authenticate":"Bearer"})

    token_data=verify_access_token(token,credentials_exception)
    
    return db.query(models.User).filter(models.User.id==token_data.id).first()
     