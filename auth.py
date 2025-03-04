import os
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv


load_dotenv(os.path.join('TRIAL_JWT', '.env'))

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
REFRESH_TOKEN_EXPIRE_MINUTES=60*24*7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def create_refresh_token(data:dict):
    if not data:
        raise ValueError("Data for refresh token is missing")
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    token=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    if not isinstance(token, str):
        raise ValueError("Failed to generate refresh token...!")

    return token


def verify_token(token:str):
    try:
        payload=jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.PyJWTError:
        return None
