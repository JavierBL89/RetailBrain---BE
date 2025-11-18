from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from backend.models import Base

engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)

def init_db():
    print("Creating database schema...")
    Base.metadata.create_all(bind=engine)
    print("Schema created.")
