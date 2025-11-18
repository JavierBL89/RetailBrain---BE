from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.models import Base


class ProductVariant(Base):
    __tablename__ = "product_variants"

    variant_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"))
    variant_sku = Column(String, unique=True, nullable=False)
    color = Column(String)
    price = Column(Float)
    image_url = Column(String)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    product = relationship("Product", back_populates="variants")
    sizes = relationship("VariantSize", back_populates="variant")
    sale_items = relationship("SaleLineItem", back_populates="variant")
