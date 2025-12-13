import pydantic

class UserCreate(pydantic.BaseModel):
    name: str
    email: str
    password: str

class UserResponse(pydantic.BaseModel):
    id: int
    name: str
    email: str

    
    model_config = pydantic.ConfigDict(from_attributes = True)

class UserLogin(pydantic.BaseModel):
    email: str
    password: str