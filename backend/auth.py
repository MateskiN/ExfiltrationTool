import bcrypt
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt

from settings import SECRET_KEY, ALGORITHM

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer flow for token retrieval
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock database of users (replace with your user database logic)
mock_users_db = {
    "user1": {
        "username": "user1",
        "password": "$2b$12$xVRqjzJKNI1RWB1oYtCaw.guxLdmPIZaa84/tBtQCI9bPIJW0Az7u",  # hashed password: 'password1'
        "disabled": False,
    }
}

# Authentication function
def authenticate_user(username: str, password: str):
    user = mock_users_db.get(username)
    if not user or not bcrypt.checkpw(bytes(password, encoding="utf-8"),
                                      bytes(user["password"], encoding="utf-8"),):
        return False
    return user

# Token generation function
def create_access_token(data: dict):
    encoded_jwt = jwt.encode(payload=data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency for extracting and verifying JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        token_data = {"username": username}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return token_data