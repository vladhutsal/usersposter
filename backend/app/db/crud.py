import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def create_like(db: Session, like: schemas.LikeCreate):
    db_like = models.Like(**like.dict())
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def get_likes_by_post(db: Session, post_id: int):
    return db.query(models.Like).filter(
        models.Like.post_id == post_id
    ).first()


def get_likes_by_date(db: Session, 
    date_from: datetime.date, date_to: datetime.date
):
    return db.query(models.Like).filter(
        models.Like.when_liked.between(date_from, date_to)
    )
