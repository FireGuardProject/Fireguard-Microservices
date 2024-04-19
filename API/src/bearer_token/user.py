from passlib.context import CryptContext
from pydantic import BaseModel

class UserInDB(BaseModel):
    username: str
    hashed_password: str

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy database for illustration
fake_users_db = {
    "test": {
        "username": "test",
        "hashed_password": pwd_context.hash("test"),
    }
}

def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

