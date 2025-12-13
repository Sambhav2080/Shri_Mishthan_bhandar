from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os

#here every request will get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#SQLite Databse
DATABASE_URL ="sqlite:///.sweetshop.db"

#create connection between python and SQLite
engine = create_engine(DATABASE_URL,connect_args = {"check_same_thread":False}
    )

#creatind session objects to interact with Database
SessionLocal = sessionmaker(autocommit = False , autoflush = False, bind = engine)

#base class for all models
Base = declarative_base()
