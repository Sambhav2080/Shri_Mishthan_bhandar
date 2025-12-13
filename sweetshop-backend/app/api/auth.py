from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse,UserLogin
from app.services.auth_service import create_user,authenticate_user

router = APIRouter(prefix = "/api/auth",tags = ["Auth"])

# ---------------- REGISTER ----------------
@router.post("/register",response_model = UserResponse,status_code = 201)
def register_user(user:UserCreate,db:Session = Depends(get_db)):
    new_user =  create_user(db,user)
    return new_user

@router.post("/login",status_code = 200)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    authenticated = authenticate_user(db,user.email,user.password)

    if not authenticated:
        return{"error":"Invalid credentials"}
    
    #simple sample tokens
    token = "dummy_token_123"

    return{
        "email": authenticated.email,
        "token": token
    }