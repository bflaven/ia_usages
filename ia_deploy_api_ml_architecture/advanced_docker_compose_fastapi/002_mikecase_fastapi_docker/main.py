from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'msg' : 'welcome on FastAPI in Docker'}
