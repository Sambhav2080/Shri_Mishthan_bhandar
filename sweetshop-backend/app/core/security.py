from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User


SECRET_KEY = "mysecretkey123"
REFRESH_SECRET_KEY = "refreshsecretkey456"
ALGORITHM = "HS256"
RESET_SECRET_KEY = "resetsecretkey789"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = ".api/auth/login")

def create_access_token(data: dict, expires_minutes: int = 30):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes = expires_minutes)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm =ALGORITHM)

def create_refresh_token(data:dict,expires_days:int = 7):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days = expires_days)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,REFRESH_SECRET_KEY,algorithm = ALGORITHM)

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

#Hash Password
def hash_password(plain_password:str)->str:
    return pwd_context.hash(plain_password)

#verify Password
def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)


def get_current_user(token:str = Depends(oauth2_scheme),db:Session= Depends(get_db)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        user_id :int = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code= 401, detail = "invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")

    return user

def create_reset_token(data:dict, expires_minutes: int = 10):
    """Generate password reset token (valid for 10 minutes)."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, RESET_SECRET_KEY, algorithm=ALGORITHM)

def verify_reset_token(token: str):
    """Decode reset token and return payload (user_id)."""
    try:
        payload = jwt.decode(token, RESET_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_id")
    except JWTError:
        return None


