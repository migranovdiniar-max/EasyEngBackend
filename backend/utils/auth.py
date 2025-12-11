from argon2 import PasswordHasher
from datetime import datetime, timedelta
from jose import jwt
from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(
    plain_password: str, 
    hashed_password: str) -> bool:
    
    try:
        return ph.verify(hashed_password, plain_password)
    except:
        return False


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def needs_rehash(hashed_password: str) -> bool:
    try:
        return ph.check_needs_rehash(hashed_password)
    except:
        return False