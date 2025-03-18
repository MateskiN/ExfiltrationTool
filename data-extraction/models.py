from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    phone_number: str
    name: str
    profile_picture: str
    status: str
    last_seen: datetime


class Chat(BaseModel):
    chat_id: int
    chat_name: str
    is_group: bool
    created_at: datetime


class ChatMember(BaseModel):
    chat_id: int
    user_id: int
    is_admin: bool
    joined_at: datetime


class Message(BaseModel):
    message_id: int
    chat_id: int
    sender_id: int
    message_type: str
    content: str | None
    media_url: str | None
    timestamp: datetime
    is_deleted: bool


class MessageStatus(BaseModel):
    message_id: int
    user_id: int
    status: str
    updated_at: datetime
