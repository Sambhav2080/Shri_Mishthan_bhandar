from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2)
    category: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    price: float | None = None
    stock: int | None = None

class ProductResponse(ProductBase):
    id: int
    stock:int

    model_config = ConfigDict(from_attributes=True)
    
