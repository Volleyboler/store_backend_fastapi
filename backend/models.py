from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    sizes = Column(ARRAY(String(20)), nullable=False)
    in_stock = Column(Boolean, default=True)
    image_url = Column(String(500))
