from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from jose import JWTError

from app.schemas.auth import *
from app.database.boxchat import *
from app.Cores.database import SessionLocal
from app.utils.jwt_handle import create_access_token, decode_access_token
from app.utils.auth_handle import get_password_hash, verify_password
from fastapi.security import HTTPBearer

oauth2_scheme = HTTPBearer()
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
        hashed_password=get_password_hash(auth.password),
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
    access_token = create_access_token({"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/user")
async def get_user(db: db_dependency, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "email": user.email,
            "name": user.name
        }
    except JWTError:
        raise HTTPException(status_code=403, detail="Token is invalid")