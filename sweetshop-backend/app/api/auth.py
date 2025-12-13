from fastapi import APIRouter, Depends ,HTTPException
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse,UserLogin, RefreshTokenRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.services.auth_service import create_user,authenticate_user, generate_reset_token, reset_password
from app.core.security import create_access_token,create_refresh_token,get_current_user, REFRESH_SECRET_KEY,ALGORITHM

router = APIRouter(prefix = "/api/auth",tags = ["Auth"])

# ---------------- REGISTER ----------------
@router.post("/register",response_model = UserResponse,status_code = 201)
def register_user(user:UserCreate,db:Session = Depends(get_db)):
    new_user =  create_user(db,user)
    return new_user

# ---------------- LOGIN ----------------
@router.post("/login",status_code = 200)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    authenticated = authenticate_user(db,user.email,user.password)

    if not authenticated:
        return{"error":"Invalid credentials"}
    
    #simple sample tokens
    access_token = create_access_token({"user_id":authenticated.id})
    refresh_token = create_refresh_token({"user_id":authenticated.id})


    return{
        "email": authenticated.email,
        "access_token":access_token,
        "refresh_token":refresh_token
    }

# ---------------- REFRESH ----------------
@router.post("/refresh")
def refresh_token(data: RefreshTokenRequest):
    try:
        payload = jwt.decode(data.refresh_token,REFRESH_SECRET_KEY,algorithms = [ALGORITHM])
        user_id = payload.get("user_id")

    except JWTError:
        raise HTTPException(status_code= 401, detail = "Invalid Refresh Token")
    
    new_access_token  = create_access_token({"user_id": user_id})

    return {"access_token":new_access_token}


# ---------------- GET USER INFO ----------------
@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return {
        "id":current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }

# ---------------- FORGOT PASSWORD ----------------
@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    reset_token = generate_reset_token(db, request.email)
    
    if not reset_token:
        raise HTTPException(status_code=404, detail="Email not found")

    # Normally email would be sent — but for assignment we return the token
    return {"reset_token": reset_token}


# ---------------- RESET PASSWORD ----------------
@router.post("/reset-password")
def reset_password_route(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    success = reset_password(db, request.token, request.new_password)

    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    return {"message": "Password reset successful"}
