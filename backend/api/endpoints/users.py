from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.db import crud, schemas
from backend.db.database import get_db
from backend.security import create_access_token, get_password_hash, authenticate

router = APIRouter()


@router.post('/signup', response_model=schemas.User)
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail='User with that name is already exisrts'
        )
    return crud.create_user(
        db=db, username=user.username, 
        password=get_password_hash(user.password)
    )


@router.post('/login/get-token', response_model=schemas.Token)
def login(
    *,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    response: Response,
):  
    user = authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, 
            detail='Incorrect username or password'
        )
    token = create_access_token(user.id)
    response.set_cookie(key='token', value=token)
    return {
        'access_token': token,
        'token_type': 'bearer',
    }
