from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Create the database connection
engine = create_engine(config("SQLALCHEMY_DATABASE_URL"), echo=True)
SQLModel.metadata.create_all(engine)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
