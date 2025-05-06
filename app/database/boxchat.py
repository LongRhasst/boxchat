from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text, Boolean, Index, Enum
from sqlalchemy.orm import relationship
from app.Cores.database import Base


class TimeStampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())


class User(Base, TimeStampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), index=True)
    hashed_password = Column(String(255))
    modified_by = Column(String(255))
    created_by = Column(String(255))

    messages = relationship("Message", back_populates="author")

    participants = relationship("Participant", back_populates="user")


class Conversation(Base, TimeStampMixin):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum("private", "group", name="conversation_type"))
    modified_by = Column(String(255))
    created_by = Column(String(255))

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

    __table_args__ = (
        Index("ix_messages_content", "content", mysql_length=255),  # Define a key length for MySQL
    )


class BlockList(Base, TimeStampMixin):
    __tablename__ = "block_list"
    blocker_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    blocked_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    is_active = Column(Boolean, default=True)

class HocSinh(Base):
    __tablename__  = "hocsinh"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)

    class HocSinh1(Base):
        __tablename__ = "hocsinh1"
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String(255), index=True)


class HocSinh2(Base):
    __tablename__ = "hocsinh2"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)


class HocSinh3(Base):
    __tablename__ = "hocsinh3"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)


class HocSinh4(Base):
    __tablename__ = "hocsinh4"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)

# class Authentications(Base, TimeStampMixin):
#     __tablename__ = "authentications"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     token = Column(String(255), index=True)