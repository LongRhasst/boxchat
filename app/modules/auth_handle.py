from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database.boxchat import User
from app.schemas.auth import LoginUser
from app.utils.jwt_handle import decode_access_token
