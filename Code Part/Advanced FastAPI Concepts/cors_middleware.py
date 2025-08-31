from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
            "http://my-frontend.com",
            "http://localhost:3000",
        ],  # Allows all origins
    allow_credentials=True,
    allow_methods = ['GET', 'POST', 'PUT', 'DELETE'],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define endpoints
