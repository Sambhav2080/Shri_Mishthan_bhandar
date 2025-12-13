from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product_schema import ProductCreate,ProductUpdate
from app.core.exceptions import SweetNotFound,OutOfStock

# ------------ Create Product (Admin Only) ------------
def create_product(db: Session, data):
    product = Product(
        name=data.name,
        category=data.category,
        price=data.price,
        stock=data.stock
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# ------------ Get All Products ------------
def get_all_products(db: Session):
    return db.query(Product).all()


# ------------ Get by ID ------------
def get_product_by_id(db: Session, product_id: int):
    sweet =  db.query(Product).filter(Product.id == product_id).first()
    if not sweet :
        raise SweetNotFound("sweet not Found")
    return sweet

# ------------ Update Product ------------
def update_product(db: Session, product_id: int, updates):
    product = get_product_by_id(db, product_id)
    if not product:
        return None

    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

# ------------ Delete Product ------------
def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if not product:
        return False

    db.delete(product)
    db.commit()
    return True

#---------------- PURCHASE PRODUCT ----------------
def purchase_product(db: Session, product_id: int):
    sweet = get_product_by_id(db, product_id)

    if sweet.quantity <= 0:
        raise OutOfStock("This sweet is sold out!")

    sweet.stock -= 1
    db.commit()
    db.refresh(sweet)
    return sweet

#---------------- RESTOCK PRODUCT ----------------
def restock_sweet(db: Session, product_id: int, amount: int):
    sweet = get_product_by_id(db, product_id)
    sweet.stock += amount
    db.commit()
    db.refresh(sweet)
    return sweet