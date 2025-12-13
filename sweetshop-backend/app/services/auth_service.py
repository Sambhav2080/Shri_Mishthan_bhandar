from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password,verify_password
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException
import bcrypt

#Registration of NEW USER
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
        password = hashed_pw
    )

    #add to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#Login USER
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


