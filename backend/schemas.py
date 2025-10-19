from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    sizes: List[str] = Field(..., min_items=1)
    in_stock: bool = True
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    sizes: Optional[List[str]] = None
    in_stock: Optional[bool] = None
    image_url: Optional[str] = None

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ProductList(BaseModel):
    products: List[Product]
    total: int
    