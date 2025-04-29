from http import HTTPStatus

from starlette.responses import JSONResponse

from app.schemas.conversation import *
from fastapi import APIRouter, Request, HTTPException
from app.modules.Users import db_dependency
from app.database.boxchat import *
from typing import List

from app.utils.auth_handle import verify_password

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
@messenger_router.post("/Conversation/create_conversation", tags = ["Conversation"])
async def create_conversation(db: db_dependency, schemas: CreateConversation, request: Request):
    user_id = request.state.user_id
    # Create a conversation
    conversation = Conversation()
    conversation.name = schemas.name
    conversation.admin_id = user_id

    # Get the ID of the newly created conversation
    db.add(conversation)
    db.commit()
    # Add members to the conversation
    add_member(db, conversation.id, schemas.members_id)
    if len(schemas.members_id) > 1:
        conversation.type = "private"
    else:
        conversation.type = "group"

    db.commit()

    return {
        "name": schemas.name,
        "user_id": user_id,
        "members_id": schemas.members_id
    }

# Route to add members to an existing conversation
@messenger_router.post("/conversation/add_member", tags = ["Conversation"])
def add_conversation_member(db: db_dependency, conversation_id: int, members: AddConversationMember):
    add_member(db, conversation_id, members.members_id)
    return {
        "members_id": members.members_id
    }

# Route to delete a conversation
@messenger_router.delete("/conversation/delete_conversation", tags = ["Conversation"])
def delete_conversation(db: db_dependency, conversation_id: int):
    db.query(Conversation).filter(Conversation.id == conversation_id).delete()
    db.commit()
    return {"status": "success"}

# @messenger_router.get("/conversation/{conversation_id}")
# def get_conversation_id(conversation_id: int):
#     response = JSONResponse(status_code=200, content={"detail": "success"})
#     response.set_cookie(
#         key = "conversation_id",
#         value = str(conversation_id)
#     )
#     return response


# Route to retrieve messages from a conversation

@messenger_router.get("/conversation/{conversation_id}/read_messages", tags=["Conversation"])
def get_messages(conversation_id: int, db: db_dependency, request: Request = None):
    user_id = request.state.user_id  # user đang xem tin nhắn

    # Lấy tất cả tin nhắn của cuộc hội thoại
    all_messages = db.query(Message).filter(Message.conversation_id == conversation_id)\
                                    .order_by(Message.created_at).all()

    # Lấy danh sách user mà current_user đã block
    blocked_ids = [
        block.blocked_id for block in db.query(BlockList)
        .filter(BlockList.blocker_id == user_id).all()
    ]

    # Lọc tin nhắn từ người không bị block
    filtered_messages = [msg for msg in all_messages if msg.user_id not in blocked_ids]

    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "id": msg.id,
                "user_id": msg.user_id,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            } for msg in filtered_messages
        ]
    }
@messenger_router.post("/conversation/send_message", tags = ["Conversation"])
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

@messenger_router.post("/conversation/relationship/block_user", tags = ["Conversation"])
def add_block_user(db: db_dependency, relation: RelationshipBlocked):
    block = BlockList()
    block.blocker_id = relation.blocker_id
    block.blocked_id = relation.blocked_id
    db.add(block)
    db.commit()
    return {
        HTTPStatus.OK: "success"
    }
@messenger_router.delete("/conversation/relationship/unblock_user", tags = ["Conversation"])
def remove_block_user(db: db_dependency, relation: RelationshipBlocked):
    db.query(BlockList).filter(BlockList.blocker_id == relation.blocker_id, BlockList.blocked_id == relation.blocked_id).delete()
    db.commit()

@messenger_router.put("/conversation/user_data/changeinfo", tags = ["Conversation"])
async def update_user_data(db: db_dependency, name: str, request: Request):
    user_id = request.state.user_id
    update = db.query(User).filter(User.id == user_id).first()
    update.name = name
    db.commit()
    return {
        "name": name
    }

@messenger_router.put("/conversation/user_data/changepassword", tags = ["Conversation"])
async def update_user_password(db: db_dependency, password: ChangePassword, request: Request):
    user_id = request.state.user_id
    update = db.query(User).filter(User.id == user_id).first()
    if not verify_password(password.old_password, update.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid current password")

    from app.utils.auth_handle import get_password_hash

    hashed_password = get_password_hash(password.new_password)
    update.hashed_password = hashed_password
    db.commit()
    return {
        "message": "success"
    }

