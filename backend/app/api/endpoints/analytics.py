import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import crud, models, schemas

router = APIRouter()


@router.post('/likes', description='Date format should be YYYY-MM-DD')
def analyse_likes_by_date(
    date_from: datetime.date, date_to: datetime.date, 
    db: Session = Depends(get_db)
) -> str:
    likes = crud.get_likes_by_date(
        db, date_from=date_from, date_to=date_to
    )
    return f'Likes between {date_from} and {date_to}: {len(likes)}'


@router.post('/user-activity')
def analyse_user_activity(user_id: int, db: Session = Depends(get_db)) -> str:
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, 
            detail='User doesn`t exists'
        )
    return f'Last login: {db_user.last_login}, Last active: {db_user.last_active}'


@router.get('/get-user-by-name', response_model=schemas.User)
def get_user_by_name(username: str, db: Session = Depends(get_db)) -> models.User:
    user = crud.get_user_by_name(db, username)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail='Wrong username'
        ) 
    return user

