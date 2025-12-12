from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.database import Base,engine

app = FastAPI()

#Create  tables in Database
Base.metadata.create_all(bind= engine)

#Register authenticated routes
app.include_router(auth_router)