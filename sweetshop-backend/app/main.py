"""Initialize FastAPI app and include authentication router"""
from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.product import router as product_router
from app.database import Base,engine
from app.api.cart import router as cart_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# ✅ CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Create  tables in Database
Base.metadata.create_all(bind= engine)

#Register authenticated routes
app.include_router(auth_router)
#Register for products
app.include_router(product_router)
#implimentation of cart
app.include_router(cart_router)