from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Annotated
import jwt
from jose import JWTError
from app.schemas.auth import *
from app.database.boxchat import *
from app.Cores.database import SessionLocal
from app.utils.jwt_handle import create_access_token, decode_access_token
from app.utils.auth_handle import get_password_hash, verify_password
from fastapi.security import HTTPBearer
from app.Cores.config import SECRET_KEY

oauth2_scheme = HTTPBearer()
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[SessionLocal, Depends(get_db)]

@router.post("/auth/create")
def create_user(auth: CreateUser,db: db_dependency):
    existing_user = db.query(User).filter(User.email == auth.email).first()
    if existing_user:
        raise HTTPException(status_code=404, detail = "Email already registered")

    new_user = User(
        email=str(auth.email),
        hashed_password=get_password_hash(auth.password),
        name=auth.name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return auth.email

@router.post("/auth/login")
async def login( account: LoginUser, db: db_dependency):
    user = db.query(User).filter(User.email == account.email).first()
    if not user or not verify_password(account.password,user.hashed_password):
        raise HTTPException(status_code=404, detail="Invalid credentials")
    access_token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm="HS256")
    return {
        "access_token": access_token
    }


@router.get("/user")
async def get_user(request: Request, db: db_dependency):
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name
    }