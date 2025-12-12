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

