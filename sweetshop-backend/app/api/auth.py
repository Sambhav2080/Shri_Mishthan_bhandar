from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import create_user

router = APIRouter(prefix = "/api/auth")

#here every request will get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register",response_model = UserResponse,status_code = 201)
def register_user(user:UserCreate,db:Session = Depends(get_db)):
    new_user =  create_user(db,user)
    return new_user