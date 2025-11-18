from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.models import Base

class SaleLineItem(Base):
    __tablename__ = "sale_line_item"

    sale_id = Column(Integer, ForeignKey("sales.sale_id"), primary_key=True)
    variant_id = Column(Integer, ForeignKey("product_variants.variant_id"), primary_key=True)
    size_id = Column(Integer, ForeignKey("sizes.size_id"), primary_key=True)

    sale_date = Column(DateTime)
    quantity_sold = Column(Integer)
    sale_price = Column(Float)

    sale = relationship("Sale", back_populates="line_items")
    variant = relationship("ProductVariant", back_populates="sale_items")
    size = relationship("Size", back_populates="sale_items")
