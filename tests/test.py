import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base


SQLALCHEMY_DATABASE_URL = "postgresql://test:test@localhost/test_vne_techwear"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_product():
    """
    Проверка создания товара
    """
    product_data = {
        "name": "Test Tech Jacket",
        "description": "Waterproof tech jacket with multiple pockets",
        "price": 299.99,
        "category": "Jackets",
        "sizes": ["S", "M", "L"],
        "in_stock": True,
        "image_url": "https://example.com/jacket.jpg"
    }
    
    response = client.post("/products", json=product_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]
    assert data["category"] == product_data["category"]
    assert "id" in data

def test_create_product_invalid_data():
    ''' 
    Тест на невалидные данные (отрицательная цена)
    '''
    product_data = {
        "name": "Test Product",
        "price": -10.0,
        "category": "Test",
        "sizes": ["M"]
    }
    
    response = client.post("/products", json=product_data)
    assert response.status_code == 422

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert "total" in data

def test_get_product():
    ''' 
    Создание товара и получение созданного товара
    ''' 
    product_data = {
        "name": "Test Product for Get",
        "price": 199.99,
        "category": "Pants",
        "sizes": ["M", "L"]
    }
    
    create_response = client.post("/products", json=product_data)
    product_id = create_response.json()["id"]
    
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == product_data["name"]

def test_get_nonexistent_product():
    """
    Проверка несуществующего товара
    """
    response = client.get("/products/9999")
    assert response.status_code == 404

def test_delete_product():
    """
    Проверка удаления товара
    """
    product_data = {
        "name": "Product to Delete",
        "price": 99.99,
        "category": "Accessories",
        "sizes": ["One Size"]
    }
    
    create_response = client.post("/products", json=product_data)
    product_id = create_response.json()["id"]
    
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404

def test_search_products():
    """
    Тестовый поиск товаров
    """
    products = [
        {
            "name": "Urban Tech Pants",
            "price": 159.99,
            "category": "Pants",
            "sizes": ["S", "M", "L"]
        },
        {
            "name": "Tech Hoodie Black",
            "price": 129.99,
            "category": "Hoodies",
            "sizes": ["M", "L", "XL"]
        }
    ]
    
    for product in products:
        client.post("/products", json=product)
    
    response = client.get("/products?category=Hoodies")
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) > 0
    assert all(p["category"] == "Hoodies" for p in data["products"])
    
    response = client.get("/products?search=Urban")
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) > 0
    assert any("Urban" in p["name"] for p in data["products"])
