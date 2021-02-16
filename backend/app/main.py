from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from .db.database import engine, get_db
from .db.models import Base
from .db import crud
from . import security

Base.metadata.create_all(bind=engine)

# def track_requests(request: Request):
#     token = request.cookies.get('token', False)
#     if token:
#         user = security.get_current_user(token=token)
#         print(type(user))



# app = FastAPI(dependencies=[Depends(track_requests)])
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router, prefix='/api')
