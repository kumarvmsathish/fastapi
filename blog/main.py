from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
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


@app.post("/createBlog", status_code = status.HTTP_201_CREATED)
def createBlog(request: models.Blog, db: Session = Depends(get_db)):
    new_blog = schemas.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blogs", response_model= List[models.ShowBlog])
def getAllBlogs(db = Depends(get_db)):
    blogs = db.query(schemas.Blog).all()
    return blogs


@app.get("/blog/{id}", response_model= models.ShowBlog)
def getBlog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(schemas.Blog).filter(schemas.Blog.id==id).first()
    if not blog:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Blog with id {id} is not found"}

    return blog


@app.put("/blog/{id}", status_code = status.HTTP_202_ACCEPTED)
def updateBlog(id: int, request: models.Blog, db: Session = Depends(get_db)):
    
    blog = db.query(schemas.Blog).filter(schemas.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")
    
    result = blog.update(request.__dict__)
    # result = db.query(schemas.Blog).filter(schemas.Blog.id == id).update({'title': request.title, 'body': request.body})

    db.commit()

    return {"message": "Updated", "result": result}


@app.delete("/deleteBlog/{id}", status_code = status.HTTP_204_NO_CONTENT)
def deleteBlog(id: int, db:Session = Depends(get_db)):
    blog = db.query(schemas.Blog).filter(schemas.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")
    
    result = blog.delete(synchronize_session=False)
    # db.query(schemas.Blog).filter(schemas.Blog.id == id).delete(synchronize_session=False)
    
    db.commit()

    return {"message": "deleted", "result": result}

