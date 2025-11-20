from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import psycopg2
from backend.models import Base
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
    """
    db_url = os.getenv("DATABASE_URL")
        # If Render provides DATABASE_URL, use it
    if db_url:
        # Parse the URL
        url = urlparse(db_url)

        host = url.hostname

        # If running locally, override Docker hostname
        if host == "db":
            host = "localhost"

        return psycopg2.connect(
            database=url.path.lstrip("/"),
            user=url.username,
            password=url.password,
            host=host,
            port=url.port,
            sslmode=os.getenv("DB_SSLMODE", "disable")
        )
    
    # Otherwise, use local env variables
    return psycopg2.connect(
        host="localhost",
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE", "disable")  # Render will override this

    )
