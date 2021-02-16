import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import crud, schemas

router = APIRouter()


@router.post('/likes')
def analyse_likes_by_date(
    date_from: datetime.date, date_to: datetime.date, 
    db: Session = Depends(get_db)
) -> str:
    sorted_likes = crud.get_likes_by_date(
        db, date_from=date_from, date_to=date_to
    )
    return f'Likes between {date_from} and {date_to}: {len(sorted_likes)}'


@router.post('/user-activity')
def analyse_user_activity(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, 
            detail='User doesn`t exists'
        )
    return f'Last login: {db_user.last_login}, Last active: {db_user.last_active}'

