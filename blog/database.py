from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# sample postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessonLocal  = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()
