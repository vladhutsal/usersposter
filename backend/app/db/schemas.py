import datetime
from typing import List
from pydantic import BaseModel


class LikeBase(BaseModel):
    post_id: int

class LikeCreate(LikeBase):
    pass

class LikeRemove(BaseModel):
    status: bool

class Like(LikeBase):
    id: int
    user_id: int
    when_liked: datetime.date

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    post_likes: List[Like] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    last_login: datetime.datetime
    last_active: datetime.datetime
    posts: List[Post] = []

    class Config:
        orm_mode = True
    
class Token(BaseModel):
    access_token: str
    token_type: str
