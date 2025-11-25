from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import Base


class ProductTag(Base):
    __tablename__ = "product_tags"

    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True)

    product = relationship("Product", back_populates="tags")
    tag = relationship("Tag", back_populates="products")
