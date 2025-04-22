from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import Token
from app.database.boxchat import *
from app.Cores.database import SessionLocal  # thêm cái này vào cho anh
from app import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/user", response_model=Token)
def index(db: Session = Depends(get_db)):
    user = db.query(User).first()
    return {"access_token": user.name}