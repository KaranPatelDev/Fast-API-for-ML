from fastapi import FastAPI, Depends

app = FastAPI()

# Dependency Functions/Injection
def get_db():
    db = {"connection to db": "mock_db_connection"}
    try:
        yield db
    finally:
        db.close()



# Endpoints
@app.get("/home")
def home(db = Depends(get_db)): # Dependency Injection Code Here
    return {"db_status": db['connection']}