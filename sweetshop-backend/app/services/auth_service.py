from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password, create_reset_token, get_current_user
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException
import bcrypt

#---------------- REGISTRATION OF NEW USER ----------------
def create_user(db:Session,user_data:UserCreate):
    
    #check Duplicate User
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise UserAlreadyExistsException(user_data.email)
    
    #hash password for safety purpose
    hashed_pw = hash_password(user_data.password)
    
    #creating user model object
    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password = hashed_pw,
        role = user_data.role or "user"
        )
    
    #add to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#---------------- AUTHENTICATION OF USER ----------------
def authenticate_user(db:Session, email: str, password: str):
    email = email.lower().strip()

    #fetch user from database
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    
    #verification of password
    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return None
    
    return user

#---------------- AUTHORIZATION OF ADMIN ----------------
def require_admin(current_user = Depends(get_current_user)):
    """Allow only admin users to access protected admin routes."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

#---------------- GENERATE RESET TOKEN ----------------
def generate_reset_token(db: Session, email: str):
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user:
        return None
    
    return create_reset_token({"user_id": user.id})

#---------------- RESET PASSWORD ----------------
def reset_password(db: Session, token: str, new_password: str):
    from app.core.security import verify_reset_token, hash_password
    
    user_id = verify_reset_token(token)
    if not user_id:
        return False
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    
    user.password = hash_password(new_password)
    db.commit()
    return True




