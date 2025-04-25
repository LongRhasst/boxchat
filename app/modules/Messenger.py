from http import HTTPStatus

from starlette.responses import JSONResponse

from app.schemas.conversation import *
from fastapi import APIRouter, Request
from app.modules.Users import db_dependency
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
async def create_conversation(db: db_dependency, schemas: CreateConversation):
    # Create a conversation
    conversation = Conversation()
    conversation.name = schemas.name
    conversation.admin_id = schemas.user_id

    # Get the ID of the newly created conversation
    conversation_id = db.query(Conversation).filter(Conversation.admin_id == schemas.user_id and Conversation.name == schemas.name).first().id

    # Add members to the conversation
    add_member(db, conversation_id, schemas.members_id)
    if len(schemas.members_id) > 1:
        conversation.type = "private"
    else:
        conversation.type = "group"

    db.add(conversation)
    db.commit()

    return {
        "name": schemas.name,
        "user_id": schemas.user_id,
        "members_id": schemas.members_id
    }

# Route to add members to an existing conversation
@messenger_router.post("/conversation/{conversation_id}/add_member")
def add_conversation_member(db: db_dependency, conversation_id: int, members: AddConversationMember):
    add_member(db, conversation_id, members.members_id)
    return {
        "members_id": members.members_id
    }

# Route to delete a conversation
@messenger_router.delete("/conversation/{conversation_id}/delete_conversation")
def delete_conversation(db: db_dependency, conversation_id: int):
    db.query(Conversation).filter(Conversation.id == conversation_id).delete()
    db.commit()
    return {"status": "success"}

@messenger_router.get("/conversation/{conversation_id}")
def get_conversation_id(conversation_id: int):
    response = JSONResponse(status_code=200, content={"detail": "success"})
    response.set_cookie(
        key = "conversation_id",
        value = str(conversation_id)
    )
    return response


# Route to retrieve messages from a conversation
@messenger_router.get("/conversation/{conversation_id}/read_messages")
def get_messages(db: db_dependency, messages: GetMessages):
    messages = db.query(Message).filter(Message.conversation_id == messages.Conversation_id).order_by(Message.created_at).all()
    # Placeholder logic for fetching blocked users
    blocked_ids = [
        block.blocked_id for block in db.query(BlockList).filter(BlockList.blocked_id == messages.user_id).all()
    ]
    filtered_messages = [message for message in messages if message.user_id not in blocked_ids]

    return {
        "messages": filtered_messages
    }

@messenger_router.post("/conversation/{conversation_id}/send_message")
def send_message(db: db_dependency, messages: SendMessage):
    message = Message()
    message.content = messages.content
    message.conversation_id = messages.conversation_id
    message.user_id = messages.user_id
    db.add(message)
    db.commit()
    return {
        "Time": message.created_at
    }

@messenger_router.put("/relationship/block_user")
def add_block_user(db: db_dependency, relation: RelationshipBlocked):
    block = BlockList()
    block.blocker_id = relation.blocker_id
    block.blocked_id = relation.blocked_id
    db.add(block)
    db.commit()
    return {
        HTTPStatus.OK: "success"
    }
@messenger_router.delete("/relationship/unblock_user")
def remove_block_user(db: db_dependency, relation: RelationshipBlocked):
    db.query(BlockList).filter(BlockList.blocker_id == relation.blocker_id, BlockList.blocked_id == relation.blocked_id).delete()
    db.commit()

