from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.db import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.Post)
def create_user_post(
    user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    return crud.create_post(db=db, post=post, user_id=user_id)


@router.get("/", response_model=List[schemas.Post])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
