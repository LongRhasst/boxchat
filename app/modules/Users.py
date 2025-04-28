from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from starlette.responses import JSONResponse

from app.Cores.config import SECRET_KEY
from app.Cores.database import SessionLocal
from app.database.boxchat import *
from app.schemas.auth import *
from app.utils.auth_handle import get_password_hash, verify_password

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
        raise HTTPException(status_code=409, detail = "Email already registered")

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
    response = JSONResponse(status_code=200, content={"detail": "success"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age = 1800,
        samesite="lax",
        secure=False
    )
    return response


@router.get("/user")
async def get_user(request: Request):
    user_id = request.state.user_id
    return {
        "user_id": user_id,
        "message": f"Welcome user {user_id}"
    }


@router.delete("/auth/logout")
def logout():
    response = JSONResponse(content={"message": "Logged out successfully"}, status_code=200)
    response.delete_cookie(key="access_token")
    return response