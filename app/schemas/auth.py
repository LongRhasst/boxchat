from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class create_user(BaseModel):
    email: EmailStr
    hash_password: str