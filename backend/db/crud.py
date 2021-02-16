import datetime
from functools import wraps
from sqlalchemy.orm import Session

from . import models, schemas


# --- USERS
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, username: str, password: str):
    db_user = models.User(
        username=username,
        hashed_password=password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_last_login(db: Session, db_user: models.User):
    db_user.last_login = datetime.datetime.now()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_last_active(db: Session, db_user: models.User):
    db_user.last_active = datetime.datetime.now()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def track_activity(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        update_user_last_active(
            kwargs.get('db'), kwargs.get('current_user')
        )
        return func(*args, **kwargs)
    return wrapper


# --- POSTS
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# --- LIKES
def create_like(db: Session, like: schemas.LikeCreate, user_id):
    db_like = models.Like(**like.dict(), user_id=user_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def remove_like(db: Session, like_id: int):
    like = db.query(models.Like).filter(models.Like.id == like_id).first()
    assert like
    db.delete(like)
    db.commit()
    return {'deleted': True}


def get_user_like_by_post(db: Session, post_id: int, user_id: int):
    return db.query(models.Like).filter(
        models.Like.post_id == post_id, models.Like.user_id == user_id
    ).first()


# --- ANALYTICS
def get_likes_by_date(
    db: Session, date_from: datetime.date, date_to: datetime.date
):
    return db.query(models.Like).filter(
        models.Like.when_liked >= date_from
    ).filter(models.Like.when_liked <= date_to).all()
