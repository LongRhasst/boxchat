from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.schemas.auth import *
from app.database.boxchat import *
from app.Cores.database import SessionLocal
from app.utils.jwt_handle import create_access_token, decode_access_token
from app.utils.auth_handle import get_password_hash, verify_password

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[SessionLocal, Depends(get_db)]

@router.post("/create")
def create_user(auth: CreateUser,db: db_dependency):
    existing_user = db.query(User).filter(User.email == auth.email).first()
    if existing_user:
        raise HTTPException(status_code=404, detail = "Email already registered")

    new_user = User(
        email=str(auth.email),
        hashed_password=get_password_hash(auth.password),  # Use hashed password here
        name=auth.name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return auth.email

@router.post("/login")
async def login( account: LoginUser, db: db_dependency):
    user = db.query(User).filter(User.email == account.email).first()
    if not user or not verify_password(account.password,user.hashed_password):
        raise HTTPException(status_code=404, detail="Invalid credentials")
    return {"user_id": user.id}

