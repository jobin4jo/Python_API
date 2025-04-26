import datetime
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import jwt, JWTError
load_dotenv()


SECRET_KEY = os.getenv("E_SECRET_KEY")
ALGORITHM = os.getenv("E_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("E_ACCESS_TOKEN_EXPIRE_MINUTES")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))  # Use timedelta directly
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None