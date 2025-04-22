from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Base schemas (for shared attributes)
class TimeStampSchema(BaseModel):
    created_at: datetime
    modified_at: Optional[datetime] = None

# User schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase, TimeStampSchema):
    id: int
    modified_by: Optional[str] = None
    created_by: Optional[str] = None

    class Config:
        from_attributes = True

# Message schemas
class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    conversation_id: int
    user_id: int

class Message(MessageBase, TimeStampSchema):
    id: int
    conversation_id: int
    user_id: int

    class Config:
        from_attributes = True

# Conversation schemas
class ConversationBase(BaseModel):
    name: str

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase, TimeStampSchema):
    id: int
    modified_by: Optional[str] = None
    created_by: Optional[str] = None

    class Config:
        from_attributes = True

# Participant schemas
class ParticipantBase(BaseModel):
    user_id: int
    conversation_id: int

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase, TimeStampSchema):
    id: int

    class Config:
        from_attributes = True

# BlockList schemas
class BlockListBase(BaseModel):
    blocker_id: int
    blocked_id: int
    is_active: bool = True

class BlockListCreate(BlockListBase):
    pass

class BlockList(BlockListBase, TimeStampSchema):
    class Config:
        from_attributes = True

# Authentication schemas
class AuthenticationBase(BaseModel):
    user_id: int
    token: str

class AuthenticationCreate(AuthenticationBase):
    pass

class Authentication(AuthenticationBase, TimeStampSchema):
    id: int

    class Config:
        from_attributes = True

# Response schemas with relationships
class UserWithRelations(User):
    messages: List[Message] = []
    participants: List[Participant] = []

class ConversationWithRelations(Conversation):
    participants: List[Participant] = []
    messages: List[Message] = []

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None