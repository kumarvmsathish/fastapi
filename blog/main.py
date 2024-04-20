from fastapi import FastAPI
from . import models
from . import schemas
from .database import engine

app = FastAPI()

# creates tables in database
schemas.Base.metadata.create_all(bind=engine)


@app.post("/createBlog")
def createBlog(request: models.Blog):
    return request
