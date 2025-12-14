import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.database.models import Base

# 1. Load environment variables from .env file
load_dotenv()

# 2. Fetch database credentials
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
# Note: Use "localhost" if running Python locally.
# If running inside a Docker container, use the service name (e.g., "db").
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# 3. Construct Connection String
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 4. Initialize Database Engine
# The engine is the central point of entry to the database.
engine = create_engine(DATABASE_URL)

# 5. Configure Session
# SessionLocal is a factory for creating new database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency generator for FastAPI.
    Creates a new database session for a request and closes it when finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    """
    Simple utility function to verify database connectivity.
    Also initializes tables if they don't exist.
    """
    try:
        # Create tables defined in models (if not exists)
        Base.metadata.create_all(bind=engine)

        # Execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ SUCCESS: Database connection established!")
            print("✅ SUCCESS: Tables created (if not existed).")
    except Exception as e:
        print("❌ ERROR: Connection failed.")
        print(f"Details: {e}")


if __name__ == "__main__":
    test_connection()