from fastapi import FastAPI, Depends
from . import models
from . import schemas
from .database import engine, SessonLocal
from sqlalchemy.orm import Session

app = FastAPI()

# creates tables in database
schemas.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessonLocal()
    try: 
        yield db
    finally:
        db.close()


@app.post("/createBlog")
def createBlog(request: models.Blog, db: Session = Depends(get_db)):
    new_blog = schemas.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blogs")
def getAllBlogs(db = Depends(get_db)):
    blogs = db.query(schemas.Blog).all()
    return blogs


@app.get("/blog/{id}")
def getBlog(id: int, db = Depends(get_db)):
    blog = db.query(schemas.Blog).filter(schemas.Blog.id==id).first()
    return blog

