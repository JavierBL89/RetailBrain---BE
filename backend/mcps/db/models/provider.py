from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from mcps.db.models import Base


class Provider(Base):
    __tablename__ = "providers"

    provider_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,unique=True, nullable=False)
    description = Column(String)
    email = Column(String, unique=True, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    products = relationship("Product", back_populates="provider")
