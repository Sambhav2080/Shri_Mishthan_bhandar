from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, require_admin
from app.core.exceptions import SweetNotFound, OutOfStock
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import (
    create_product, get_all_products, update_product, delete_product, get_product_by_id
)

router = APIRouter(prefix="/api/products", tags=["Products"])


# ------------------ Create Product (Admin Only) ------------------
@router.post("", status_code=201, response_model=ProductResponse)
def add_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return create_product(db, data)


# ------------------ Public: Get All Products ------------------
@router.get("", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return get_all_products(db)


# ------------------ Update Product ------------------
@router.put("/{product_id}", response_model=ProductResponse)
def modify_product(
    product_id: int,
    updates: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    updated = update_product(db, product_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")

    return updated


# ------------------ Delete Product ------------------
@router.delete("/{product_id}")
def remove_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}

#---------------- Purchase Product ----------------
@router.post("/{product_id}/purchase")
def purchase_product(product_id: int, db: Session = Depends(get_db)):
    try:
        return purchase_product(db, product_id)
    except SweetNotFound:
        raise HTTPException(404, "Sweet not found")
    except OutOfStock:
        raise HTTPException(400, "Out of stock")


#---------------- Restock Product (ADMIN only) ----------------
@router.post("/{sweet_id}/restock")
def restock_product(
    product_id: int,
    amount: int = 1,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    try:
        return restock_product(db, product_id, amount)
    except SweetNotFound:
        raise HTTPException(404, "Sweet not found")