from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import engine, get_db

# Создание таблиц
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VNE Techwear API",
    description="REST API для интернет-магазина techwear бренда VNE",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в VNE Techwear API"}

@app.get("/products", response_model=schemas.ProductList)
def read_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    products = crud.get_products(
        db, 
        skip=skip, 
        limit=limit, 
        category=category, 
        search=search
    )
    total = crud.get_products_count(db)
    
    return {
        "products": products,
        "total": total
    }

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return db_product

@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return {"message": "Товар успешно удален"}

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int, 
    product_update: schemas.ProductUpdate, 
    db: Session = Depends(get_db)
):
    updated_product = crud.update_product(db, product_id, product_update)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return updated_product

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}
