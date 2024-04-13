from fastapi import FastAPI

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