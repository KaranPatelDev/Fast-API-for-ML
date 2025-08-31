from datetime import datetime, timedelta, timezone
from authlib.jose import jwt, JWTError
from fastapi import HTTPException


# Constants
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Function to create a JWT token
def create_access_token(data: dict):
    header = {"alg": ALGORITHM}
    expire = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = data.copy()
    payload.update({"exp": expire})
    return jwt.encode(header, payload, SECRET_KEY).decode("utf-8")


# Function to verify a JWT token
def verify_token(token: str):
    try:
        claims = jwt.decode(token, SECRET_KEY)
        claims.validate()  # This will check the 'exp' claim
        username = claims.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

