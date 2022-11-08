from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


class CreateUser(BaseModel):
    email:EmailStr
    password:str

class ResponseUser(BaseModel):
    email:EmailStr
    id:int
    created_at:datetime

    class Config:
        orm_mode = True

class User(BaseModel):
    id:int

class PostBase(BaseModel):
    title:str
    content:str
    published:bool =True 
    likes: Optional[int] = 0


class CreatePost(PostBase):
    pass

class ResponsePost(PostBase):
    published:bool
    id:int
    likes: int
    created_at:datetime
    user_id:int
    owner: ResponseUser

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id : Optional[str]=None


