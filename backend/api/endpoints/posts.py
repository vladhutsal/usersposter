from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db import crud, models, schemas
from backend.security import get_current_user

router = APIRouter()


@router.post('/create', response_model=schemas.Post)
@crud.track_activity
def create_user_post( 
    post: schemas.PostCreate, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_post(db=db, post=post, user_id=current_user.id)


@router.get('/', response_model=List[schemas.Post])
@crud.track_activity
def read_posts(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@router.post('/switch-like')
@crud.track_activity
def like_unlike_post(
    like: schemas.LikeCreate, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> Union[schemas.Like, schemas.LikeRemove]:
    db_like = crud.get_user_like_by_post(db, like.post_id, current_user.id)
    if db_like:
        return crud.remove_like(db, db_like.id)
    return crud.create_like(db, like, current_user.id)
