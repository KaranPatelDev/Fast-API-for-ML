from fastapi import FastAPI

app = FastAPI()

# For each endpoint you create, you need to define a function that will be executed when that endpoint is called.
@app.get("/")
def read_root():
    return {"message": "Heyya!"}
'''
@app.get("/"): This is a decorator. In this context, it tells the application that the function directly below it should run when a user accesses the root URL (/) using an HTTP GET request.

home(): This is a function that gets executed when the route specified by the decorator (@app.get("/")) is accessed. It contains the logic that determines what the server should do or what information it should return.

return: This is the Python keyword used to send a value back from a function. The table notes that the returned value is automatically converted to JSON. This is a common feature in modern web frameworks, which helps simplify sending data to a client (like a web browser or a mobile app) in a standardized format.



FastAPI allows returning:
Dictionaries: These are the most common and straightforward. FastAPI automatically converts a Python dictionary into a JSON response, which is a standard format for data exchange on the web.
Pydantic models: Pydantic is a library used by FastAPI for data validation and settings management. When you return a Pydantic model, FastAPI automatically validates the data and serializes it into JSON. This is a powerful feature for ensuring that the data you send to the client is correctly structured and typed.
Custom response types: For situations where you don't want a JSON response, FastAPI allows you to return other data formats, such as HTML, plain text, or even streaming data (for things like large files or real-time updates).
'''




# To see in swagger UI: http://localhost:8000/docs
# To see in redocly: http://localhost:8000/redoc