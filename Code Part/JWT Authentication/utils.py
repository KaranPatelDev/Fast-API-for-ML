# This file contains utility functions for JWT authentication.
# It is just collection of helper functions that can be used in various parts of the application.

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_user_db = {
    'johndoe': {
        'username': 'johndoe',
        'hashed_password': pwd_context.hash('secret123')
    }
}

def get_user(username: str):
    user = fake_user_db.get(username)
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
