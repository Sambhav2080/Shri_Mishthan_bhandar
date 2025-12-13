import pydantic
import re

class UserCreate(pydantic.BaseModel):
    name: str
    email: pydantic.EmailStr
    password: str = pydantic.Field(min_length = 8,max_length = 72)
    
    @pydantic.field_validator("email")
    def normalize_email(cls,v):
        return v.lower().strip()
    
    @pydantic.field_validator("password")
    def validate_password(cls,v):
        if not re.search(r"[A-Za-z]",v):
            raise ValueError("password must contain at least one letter.")
        if not re.search(r"\d",v):
            raise ValueError("Password must conatin at least one digit.")
        return v

class UserResponse(pydantic.BaseModel):
    id: int
    name: str
    email: str

    
    model_config = pydantic.ConfigDict(from_attributes = True)

class UserLogin(pydantic.BaseModel):
    email: str
    password: str

    @pydantic.field_validator("email")
    def normalize_email(cls,v):
        return v.lower().strip()
    
    @pydantic.field_validator("password")
    def validate_password(cls,v):
        if not re.search(r"[A-Za-z]",v):
            raise ValueError("password must contain at least one letter.")
        if not re.search(r"\d",v):
            raise ValueError("Password must conatin at least one digit.")
        return v
    
class RefreshTokenRequest(pydantic.BaseModel):
    refresh_token:str

class ForgotPasswordRequest(pydantic.BaseModel):
    email: str


class ResetPasswordRequest(pydantic.BaseModel):
    token: str
    new_password: str
