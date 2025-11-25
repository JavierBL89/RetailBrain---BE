from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from mcps.db.models import Base


class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String, unique=True)

    products = relationship("ProductTag", back_populates="tag")
