from datetime import datetime,timedelta, UTC
from jose import JWTError,jwt
from pydantic import EmailStr

from app.schemas.auth import TokenData
from app.Cores.config import SECRET_KEY

def create_access_token(data:dict, expires_delta:timedelta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm="HS256")
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        email:EmailStr = payload.get("sub")
        if email is None:
            raise JWTError
        token_data = TokenData(email=email)
    except JWTError:
        raise JWTError
    return token_data