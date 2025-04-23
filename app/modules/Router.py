from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.schemas.auth import *
from app.database.boxchat import *
from app.Cores.database import SessionLocal  # thêm cái này vào cho anh

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[SessionLocal, Depends(get_db)]

@router.post("/create")
def create_user(auth: create_user,db: db_dependency):
    user = db.query(User).filter(User.email == auth.email).first()
    if user:
        raise HTTPException(status_code=404, detail = "Invalid Email")
    return user
