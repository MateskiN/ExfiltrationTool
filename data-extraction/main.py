import sqlite3
import json
from datetime import datetime

import requests

from settings import LOCAL_DB_PATH
from models import User, Chat, ChatMember, Message, MessageStatus

USERS_TABLE = 'Users'
CHATS_TABLE = 'Chats'
CHAT_MEMBERS_TABLE = 'ChatMembers'
MESSAGES_TABLE = 'Messages'
MESSAGE_STATUS_TABLE = 'MessageStatus'
URL = 'http://localhost:8000/collect-data/'
TOKEN_URL = 'http://localhost:8000/token'

credentials = {
    "username": "user1",
    "password": "password1"
}

def extract_data_from_table(db_path, table_name, obj, url, token, batch_size):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    entries = []

    cursor.execute(f"SELECT count(*) FROM {table_name}")
    num_of_entries = cursor.fetchone()

    for offset in range(0, num_of_entries[0], batch_size):

        cursor.execute(f"SELECT * FROM {table_name} LIMIT ? OFFSET {offset}", (batch_size,))
        rows = cursor.fetchall()

        for row in rows:
            entry = obj(row)
            entries.append(entry)

        json_output = [entry.model_dump() for entry in entries]
        entries.clear()

        # send this batch to the VPS
        send_data_to_vps(json_output, url, token)

    conn.close()


def create_user(row):
    return User(user_id=row[0], phone_number=row[1], name=row[2], profile_picture=row[3], status=row[4], last_seen=row[5])

def create_chat(row):
    return Chat(chat_id=row[0], chat_name=row[1], is_group=row[2], created_at=row[3])

def create_chat_member(row):
    return ChatMember(chat_id=row[0], user_id=row[1], is_admin=row[2], joined_at=row[3])

def create_message(row):
    return Message(message_id=row[0], chat_id=row[1], sender_id=row[2], message_type=row[3], content=row[4], media_url=row[5], timestamp=row[6], is_deleted=row[7])

def create_message_status(row):
    return MessageStatus(message_id=row[0], user_id=row[1], status=row[2], updated_at=row[3])

def get_jwt_token(url, form_data):
    response = requests.post(url, form_data)
    return response.json()

def send_data_to_vps(data, url, token):
    serialized_data = json.loads(json.dumps(data, default=lambda o: o.isoformat() if isinstance(o, datetime) else o))
    requests.post(url, json=serialized_data, headers={"Authorization": "Bearer " + token})

jwt_token = get_jwt_token(TOKEN_URL, credentials)

extract_data_from_table(LOCAL_DB_PATH, USERS_TABLE, create_user, URL + USERS_TABLE.lower(), jwt_token, 3)
extract_data_from_table(LOCAL_DB_PATH, CHATS_TABLE, create_chat, URL + CHATS_TABLE.lower(), jwt_token, 3)
extract_data_from_table(LOCAL_DB_PATH, CHAT_MEMBERS_TABLE, create_chat_member, URL + CHAT_MEMBERS_TABLE.lower(), jwt_token, 3)
extract_data_from_table(LOCAL_DB_PATH, MESSAGES_TABLE, create_message, URL + MESSAGES_TABLE.lower(), jwt_token, 3)
extract_data_from_table(LOCAL_DB_PATH, MESSAGE_STATUS_TABLE, create_message_status, URL + MESSAGE_STATUS_TABLE.lower(), jwt_token, 3)

