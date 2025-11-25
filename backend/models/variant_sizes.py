from sqlalchemy import Column, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from models import Base


class VariantSize(Base):
    __tablename__ = "variant_sizes"

    variant_id = Column(Integer, ForeignKey("product_variants.variant_id", ondelete="CASCADE"), primary_key=True)
    size_id = Column(Integer, ForeignKey("sizes.size_id", ondelete="CASCADE"), primary_key=True)
    stock_quantity = Column(Integer, default=0)
    available = Column(Boolean, default=True)

    variant = relationship("ProductVariant", back_populates="sizes")
    size = relationship("Size", back_populates="variants")

    __table_args__ = (UniqueConstraint("variant_id", "size_id"),)
