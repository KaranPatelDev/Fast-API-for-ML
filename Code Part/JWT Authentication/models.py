from pydantic import BaseModel


class User(BaseModel):
    username : str
    password : str

class UserInDB(User): # This class is used to represent a user stored in the database by calling User class and adding a new attribute
    hashed_password : str


