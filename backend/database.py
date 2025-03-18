from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserORM(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'whatsapp'}

    user_id = Column(Integer, primary_key=True)
    phone_number = Column(String)
    name = Column(String)
    profile_picture = Column(String)
    status = Column(String)
    last_seen = Column(DateTime)

class ChatORM(Base):
    __tablename__ = "chats"
    __table_args__ = {'schema': 'whatsapp'}

    chat_id = Column(Integer, primary_key=True)
    chat_name = Column(String)
    is_group = Column(Boolean)
    created_at = Column(DateTime)

class ChatMemberORM(Base):
    __tablename__ = "chatmembers"
    __table_args__ = {'schema': 'whatsapp'}

    chat_id = Column(Integer, ForeignKey("whatsapp.chats.chat_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("whatsapp.users.user_id"), primary_key=True)
    is_admin = Column(Boolean)
    joined_at = Column(DateTime)

class MessageORM(Base):
    __tablename__ = "messages"
    __table_args__ = {'schema': 'whatsapp'}

    message_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("whatsapp.chats.chat_id"))
    sender_id = Column(Integer, ForeignKey("whatsapp.users.user_id"))
    message_type = Column(String)
    content = Column(String)
    media_url = Column(String)
    timestamp = Column(DateTime)
    is_deleted = Column(Boolean)

class MessageStatusORM(Base):
    __tablename__ = "messagetatus"
    __table_args__ = {'schema': 'whatsapp'}

    message_id = Column(Integer, ForeignKey("whatsapp.messages.message_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("whatsapp.users.user_id"), primary_key=True)
    status = Column(String)
    updated_at = Column(DateTime)
