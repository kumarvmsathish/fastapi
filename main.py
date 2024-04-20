from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def index():
    return {"status": "Application running"}
    
@app.get("/home")
def home():
    return {"result": "Home"}


@app.get("/health")
def health():
    return {"status": "healthy", "version": 1}


if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=9000)