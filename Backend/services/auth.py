from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_for_dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def verify_password(plain_pass:str, hashed_pass: str)->bool:
    return pwd_context.verify(plain_pass, hashed_pass)

def get_password_hash(password:str)->str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_in: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_in:
        expire = datetime.now(timezone.utc) + timedelta(expires_in)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
