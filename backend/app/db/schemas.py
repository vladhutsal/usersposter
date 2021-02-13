import datetime
from typing import List
from pydantic import BaseModel


class LikeBase(BaseModel):
    post_id: int
    user_id: int

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    id: int
    when_liked: datetime.datetime

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
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    last_login: datetime.datetime
    last_active: datetime.datetime
    posts: List[Post] = []

    class Config:
        orm_mode = True
