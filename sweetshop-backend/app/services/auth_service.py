from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
import bcrypt

def create_user(db:Session,user_data:UserCreate):

    #hash password for safety purpose
    hashed_pw = bcrypt.hashpw(user_data.password.encode('utf-8'),bcrypt.gensalt())
    
    #creating user model object
    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password = hashed_pw.decode('utf-8')
    )

    #add to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def authenticate_user(db:Session, email: str, password: str):
    #fetch user from database
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None
    
    #verification of password
    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return None
    
    return user


