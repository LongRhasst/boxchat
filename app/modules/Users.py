from typing import Annotated
import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from datetime import timedelta, timezone
from app.Cores.config import SECRET_KEY, REFRESH_KEY
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

oath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/auth/create", tags = ["Authentication"])
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

@router.post("/auth/login", tags = ["Authentication"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()] , db: db_dependency):
   user = authentication_user(form_data.username, form_data.password, db)
   access_token = create_access_token(user.id, user.email)
   response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, status_code=200)
   refresh_token = create_refresh_token(user.id)
   response.set_cookie(key="refresh_token", value=refresh_token)
   return response

def create_refresh_token(user_id: int):
    REFRESH_TOKEN_EXPIRE_DAYS = 300
    refresh_token_expires = datetime.now(timezone.utc) + timedelta(days = REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token_payload = {
        "id": user_id,
        "exp": refresh_token_expires
    }
    refresh_token = jwt.encode(refresh_token_payload, REFRESH_KEY, algorithm="HS256")
    return refresh_token

def create_access_token(user_id: int, user_email: str):
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   access_token_expires = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
   access_token_payload = {
       "id": user_id,
       "sub":user_email,
       "exp": access_token_expires
   }
   access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm="HS256")
   return access_token

def authentication_user(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@router.get("/user", tags = ["Authorize"])
async def get_user(request: Request):
    user_id = request.state.user_id
    return {
        "user_id": user_id,
        "message": f"Welcome user {user_id}"
    }


@router.delete("/auth/logout", tags = ["Authentication"])
def logout():
    response = JSONResponse(content={"message": "Logged out successfully"}, status_code=200)
    response.delete_cookie(key="access_token")
    return response