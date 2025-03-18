from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import authenticate_user, create_access_token, get_current_user
from database import get_db, UserORM, ChatMemberORM, ChatORM, MessageORM, MessageStatusORM
import jwt

from settings import SECRET_KEY

models_mapping = {
    "users": UserORM,
    "chats": ChatORM,
    "chatmembers": ChatMemberORM,
    "messages": MessageORM,
    "messagestatus": MessageStatusORM
}

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello World"}

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token_data = {"sub": user["username"]}
    access_token = create_access_token(token_data)
    return access_token

@app.post("/collect-data/{table_name}")
async def collect_data(table_name: str, request: Request, db: Session = Depends(get_db), _ = Depends(get_current_user)):
    data = await request.json()

    model = models_mapping.get(table_name.lower())
    if model is None:
        raise HTTPException(status_code=404, detail=f"Table {table_name} not found.")

    created_objects = []
    for item in data:
        new_obj = model(**item)
        db.add(new_obj)
    db.commit()

    for obj in db.new:  # or iterate over the added instances manually if stored
        db.refresh(obj)
        created_objects.append(obj)

    return created_objects

@app.get("/messages")
def get_messages(db: Session = Depends(get_db), _ = Depends(get_current_user)):
    messages = db.query(MessageORM).all()
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this chat.")

    return messages

@app.get("/messages/{chat_id}")
async def get_messages_by_chat(chat_id: int, db: Session = Depends(get_db), _ = Depends(get_current_user)):
    messages = db.query(MessageORM).filter(MessageORM.chat_id == chat_id).order_by(MessageORM.timestamp).all()

    if not messages:
        raise HTTPException(status_code=404, detail="No messages found or chat does not exist.")

    conversation = []

    for message in messages:
        user = db.query(UserORM).get(message.sender_id)
        if not user:
            continue

        if message.message_type == 'text':
            content = message.content
        else:
            content = message.media_url

        conversation.append({
            "user": user.name,
            "message": content
        })

    return conversation

# Helper Methods
def validate_token(token: str):
    jwt.decode(token, key=SECRET_KEY)