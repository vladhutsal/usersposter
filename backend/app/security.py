from typing import Optional, Union
from datetime import datetime, timedelta

from pydantic import ValidationError
from fastapi import Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from jose import jwt
from passlib.context import CryptContext

from app.db import models, crud
from app.db.database import get_db

SECRET_KEY = '2ad389004a0a141e0f67dd6bbcf150e042ddd2272a7b1363fdcdfbc81a3efd3b'
ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTES = 10080

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/users/login/get-token')


def create_access_token(subject: Union[str, int]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode = {'exp': expire, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail='Could not validate credentials',
        )
    user = crud.get_user(db, user_id=payload.get('sub'))

    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


def authenticate(db: Session, username: str, password: str) -> Optional[models.User]:
    user = crud.get_user_by_name(db, username=username)
    password_pass = verify_password(password, user.hashed_password)
    if not user or not password_pass:
        return None
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
