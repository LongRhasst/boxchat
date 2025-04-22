from xmlrpc.client import Boolean

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.Cores.database import Base


class TimeStampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())


class User(Base, TimeStampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)
    modified_by = Column(String)
    created_by = Column(String)

    messages = relationship("Message", back_populates="author")

    participants = relationship("Participant", back_populates="user")


class Conversation(Base, TimeStampMixin):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    modified_by = Column(String)
    created_by = Column(String)

    participants = relationship("Participant", back_populates="conversation")

    messages = relationship("Message", back_populates="conversation")


class Participant(Base, TimeStampMixin):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)

    user = relationship("User", back_populates="participants")

    conversation = relationship("Conversation", back_populates="participants")


class Message(Base, TimeStampMixin):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    conversation = relationship("Conversation", back_populates="messages")

    author = relationship("User", back_populates="messages")

class BlockList(Base, TimeStampMixin):
    __tablename__ = "block_list"
    blocker_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    blocked_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    is_active = Column(Boolean, default=True)

class Authentications(Base, TimeStampMixin):
    __tablename__ = "authentications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, index=True)