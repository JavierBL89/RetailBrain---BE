from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from mcps.db.models import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)
    material = Column(String)
    gender = Column(String)
    brand = Column(String)

    # Your custom field
    tags_string = Column(String)  # Comma-separated tags

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    variants = relationship("ProductVariant", back_populates="product")
    tags = relationship("ProductTag", back_populates="product")
