from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.services.product_service import get_product_by_id, purchase_sweet
from app.schemas.cart_schema import CartAdd

router = APIRouter(prefix="/api/cart", tags=["Cart"])

# Temporary in-memory cart
CART = {}

# ------------ Add Item to Cart ------------
@router.post("/add")
def add_to_cart(
    data:CartAdd,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.id

    # Validate sweet existence
    sweet = get_product_by_id(db, data.product_id)

    CART.setdefault(user_id, [])
    CART[user_id].append({"sweet_id": data.product_id, "quantity": data.quantity})

    return {"message": "Item added to cart", "cart": CART[user_id]}

# ------------ Checkout Cart ------------
@router.post("/checkout")
def checkout_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.id

    if user_id not in CART or not CART[user_id]:
        raise HTTPException(400, "Cart is empty")

    # Deduct stock for all cart items
    for item in CART[user_id]:
        purchase_sweet(db, item["sweet_id"], item["quantity"])

    # Clear cart after checkout
    CART[user_id] = []

    return {
        "message": "Order placed successfully",
        "payment": "Cash on Delivery"
    }
