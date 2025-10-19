from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Product
from schemas import ProductCreate, ProductUpdate
from typing import List, Optional

def get_products(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None
) -> List[Product]:
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    
    if search:
        search_filter = or_(
            Product.name.ilike(f"%{search}%"),
            Product.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    return query.offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int) -> Product:
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
        sizes=product.sizes,
        in_stock=product.in_stock,
        image_url=product.image_url
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> bool:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False

def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product

def get_products_count(db: Session) -> int:
    return db.query(Product).count()
