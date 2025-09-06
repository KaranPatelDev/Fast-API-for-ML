from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)


@app.get('/home')
def home():
    return {'message': 'Prometheus Demo'}

'''
Command to run the application:
uvicorn prometheus-setup:app --reload
Also visit : http://127.0.0.1:8000/metrics
'''
