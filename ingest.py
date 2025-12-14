from sqlalchemy import text
from src.database.db import SessionLocal, engine
from src.database.models import Base
from src.collectors.rss_collector import fetch_and_store_rss


def init_db():
    """
    Initializes the database:
    1. Activates the 'pgvector' extension.
    2. Creates tables if they don't exist.
    """
    try:
        # 1. Activate 'vector' extension for AI embeddings
        with engine.connect() as connection:
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            connection.commit()

        # 2. Create Schema (Tables)
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully (Extension + Tables).")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")


def run_collector():
    """
    Manually triggers the RSS collector for testing purposes.
    """
    db = SessionLocal()
    try:
        # Target RSS Feed
        rss_url = "https://www.wired.com/feed/category/gear/latest/rss"
        source_name = "Wired Gear"

        print("🚀 Starting InsightFeed Data Collector...")
        print(f"🎯 Target: {source_name}")

        # Start the ETL process
        fetch_and_store_rss(
            db=db,
            rss_url=rss_url,
            source_name=source_name
        )

    except Exception as e:
        print(f"❌ Critical Error in Collector: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # First, ensure DB is ready
    init_db()

    # Then run the collector
    run_collector()