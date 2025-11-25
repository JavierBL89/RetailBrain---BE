from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import psycopg2
from models import Base
from urllib.parse import urlparse
from dotenv import load_dotenv


load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)

def init_db():
    print("Creating database schema...")
    Base.metadata.create_all(bind=engine)
    print("Schema created.")

def get_db_connection():
    """
    Establish a connection to the PostgreSQL database using environment variables.
    Handles both Docker (service name 'db') and production (Render) environments.
    """
    db_url = os.getenv("DATABASE_URL")
    
    if db_url:
        # Parse the URL
        url = urlparse(db_url)
        host = url.hostname
        
        # Keep 'db' hostname when running in Docker
        # Only override if explicitly running locally (not in container)
        
        return psycopg2.connect(
            database=url.path.lstrip("/"),
            user=url.username,
            password=url.password,
            host=host,  # Use 'db' when in Docker, actual host for Render
            port=url.port,
            sslmode=os.getenv("DB_SSLMODE", "disable")
        )
    
    # Fallback: use Docker service name by default
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),  # Changed from "localhost" to "db"
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "mydatabase"),
        user=os.getenv("POSTGRES_USER", "hackathon_user"),
        password=os.getenv("POSTGRES_PASSWORD", "hackathon_pass"),
        sslmode=os.getenv("DB_SSLMODE", "disable")
    )