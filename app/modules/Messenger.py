from http import HTTPStatus

from fastapi import APIRouter
from app.modules.Router import db_dependency
from app.database.boxchat import *
from typing import List

messenger_router = APIRouter()

# Helper function to add members to a conversation
def add_member(db: db_dependency(), conversation_id: int, user_ids: List[int]):
    for member_id in user_ids:
        participant = Participant()
        participant.user_id = member_id
        participant.conversation_id = conversation_id
        db.add(participant)
    db.commit()

# Route to create a new conversation
@messenger_router.post("/Conversation/create_conversation")
async def create_conversation(db: db_dependency,user_id: int,name: str,members_id: List[int]):
    # Create a conversation
    conversation = Conversation()
    conversation.name = name
    conversation.admin_id = user_id
    db.add(conversation)
    db.commit()

    # Get the ID of the newly created conversation
    conversation_id = db.query(Conversation).filter(Conversation.admin_id == user_id, Conversation.name == name).first().id

    # Add members to the conversation
    add_member(db, conversation_id, members_id)

    return {
        "name": name,
        "user_id": user_id,
        "members_id": members_id
    }

# Route to add members to an existing conversation
@messenger_router.put("/conversation/{conversation_id}/add_member")
def add_conversation_member(db: db_dependency, conversation_id: int, members_id: List[int]):
    add_member(db, conversation_id, members_id)
    return {
        "members_id": members_id
    }

# Route to delete a conversation
@messenger_router.delete("/conversation/{conversation_id}/delete_conversation")
def delete_conversation(db: db_dependency, conversation_id: int):
    db.query(Conversation).filter(Conversation.id == conversation_id).delete()
    db.commit()
    return {"status": "success"}

# Route to retrieve messages from a conversation
@messenger_router.get("/conversation/{conversation_id}/read_messages")
def get_messages(db: db_dependency, conversation_id: int, user_id: int):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()

    # Placeholder logic for fetching blocked users
    blocked_ids = [
        block.blocked_id for block in db.query(BlockList).filter(BlockList.blocked_id == user_id).all()
    ]
    filtered_messages = [message for message in messages if message.user_id not in blocked_ids]

    return {
        "messages": filtered_messages
    }

@messenger_router.post("/conversation/{conversation_id}/send_message")
def send_message(db: db_dependency, content: str, conversation_id: int, user_id: int):
    message = Message()
    message.content = content
    message.conversation_id = conversation_id
    message.user_id = user_id
    db.add(message)
    db.commit()
    return {
        "Time": message.content
    }



@messenger_router.put("/relationship/block_user")
def add_block_user(db: db_dependency, blocker_id: int, blocked_id: int):
    block = BlockList()
    block.blocker_id = blocker_id
    block.blocked_id = blocked_id
    db.add(block)
    db.commit()
    return {
        HTTPStatus.OK: "success"
    }
@messenger_router.delete("/relationship/unblock_user")
def remove_block_user(db: db_dependency, blocker_id: int, blocked_id: int):
    db.query(BlockList).filter(BlockList.blocker_id == blocker_id, BlockList.blocked_id == blocked_id).delete()
    db.commit()

