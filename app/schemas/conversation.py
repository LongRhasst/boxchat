from pydantic import BaseModel
from typing import List

class CreateConversation(BaseModel):
    user_id: int
    name: str
    members_id: List[int]

class AddConversationMember(BaseModel):
    Conversation_id: int
    members_id: List[int]

class GetMessages(BaseModel):
    Conversation_id: int
    user_id: int

class SendMessage(BaseModel):
    conversation_id: int
    user_id: int
    content: str

class AddBlockUser(BaseModel):
    blocker_id: int
    blocked_id: int

class RemoveBlockUser(BaseModel):
    blocker_id: int
    blocked_id: int