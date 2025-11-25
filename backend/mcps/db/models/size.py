from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from mcps.db.models import Base


class Size(Base):
    __tablename__ = "sizes"

    size_id = Column(Integer, primary_key=True, autoincrement=True)
    size_label = Column(String, unique=True)

    variants = relationship("VariantSize", back_populates="size")
    sale_items = relationship("SaleLineItem", back_populates="size")
