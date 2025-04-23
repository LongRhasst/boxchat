from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CreateUser(BaseModel):
    email: str
    password: str
    name: str

class LoginUser(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None