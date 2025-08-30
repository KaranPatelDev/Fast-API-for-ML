from fastapi import FastAPI
from pydantic import BaseModel

# Pydantic model
class User(BaseModel):
    id: int
    name: str

app = FastAPI()
# Endpoint using Pydantic model
@app.get("/user", response_model=User)
def get_user():
    return User(id=1, name="Bruce Wyane")
# To see go to http://localhost:8000/user