from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from mcps.db.models import Base


class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    sale_date = Column(DateTime, default=func.now())
    items_count = Column(Integer)
    sale_price = Column(Float)
    currency = Column(String, default="EUR")
    total_amount = Column(Float)

    line_items = relationship("SaleLineItem", back_populates="sale")
