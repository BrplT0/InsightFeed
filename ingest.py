from sqlalchemy import text
from src.database.db import SessionLocal, engine
from src.database.models import Base
from src.collectors.rss_collector import fetch_and_store_rss

# --- GLOBAL RSS SOURCE LIST (50+ FEEDS) ---
RSS_SOURCES = [
    # 💻 TECHNOLOGY & SOFTWARE
    ("Wired Top Stories", "https://www.wired.com/feed/rss"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("Hacker News", "https://news.ycombinator.com/rss"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
    ("Engadget", "https://www.engadget.com/rss.xml"),
    ("Gizmodo", "https://gizmodo.com/rss"),
    ("Mashable", "https://mashable.com/feed/"),
    ("ZDNet", "https://www.zdnet.com/news/rss.xml"),
    ("VentureBeat", "https://venturebeat.com/feed/"),
    ("MacRumors", "https://www.macrumors.com/macrumors.xml"),
    ("Android Authority", "https://www.androidauthority.com/feed"),
    ("9to5Mac", "https://9to5mac.com/feed/"),

    # 👨‍💻 DEVELOPER & CODING
    ("Stack Overflow Blog", "https://stackoverflow.blog/feed/"),
    ("Python Real News", "https://realpython.com/atom.xml"),
    ("InfoQ", "https://feed.infoq.com/"),
    ("Martin Fowler", "https://martinfowler.com/feed.atom"),
    ("FreeCodeCamp", "https://www.freecodecamp.org/news/rss/"),

    # 🚀 SCIENCE & SPACE
    ("NASA Breaking", "https://www.nasa.gov/rss/dyn/breaking_news.rss"),
    ("Space.com", "https://www.space.com/feeds/all"),
    ("Science Daily", "https://www.sciencedaily.com/rss/all.xml"),
    ("New Scientist", "https://www.newscientist.com/feed/home/"),
    ("Phys.org", "https://phys.org/rss-feed/"),
    ("Scientific American", "http://rss.sciam.com/ScientificAmerican-Global"),

    # 🌍 WORLD & NEWS
    ("BBC Top Stories", "http://feeds.bbci.co.uk/news/rss.xml"),
    ("CNN Top Stories", "http://rss.cnn.com/rss/edition.rss"),
    ("New York Times World", "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"),
    ("Guardian World", "https://www.theguardian.com/world/rss"),
    ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml"),
    ("Reuters Top News", "https://www.reutersagency.com/feed/?best-topics=top-news&post_type=best"),

    # 💰 FINANCE & ECONOMY
    ("Bloomberg", "https://www.bloomberg.com/feed/rss"),
    ("CNBC", "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
    ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
    ("Investing.com", "https://www.investing.com/rss/news.rss"),
    ("Fortune", "https://fortune.com/feed"),

    # 🎮 GAMING
    ("IGN", "https://feeds.ign.com/ign/news"),
    ("GameSpot", "https://www.gamespot.com/feeds/news/"),
    ("Kotaku", "https://kotaku.com/rss"),
    ("Polygon", "https://www.polygon.com/rss/index.xml"),
    ("Eurogamer", "https://www.eurogamer.net/?format=rss"),
    ("PC Gamer", "https://www.pcgamer.com/rss"),

    # ⚽ SPORTS & HEALTH
    ("ESPN Top News", "https://www.espn.com/espn/rss/news"),
    ("BBC Sport", "http://feeds.bbci.co.uk/sport/rss.xml"),
    ("WebMD Health", "https://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=rss_public_health"),
    ("Psychology Today", "https://www.psychologytoday.com/us/feed"),
    ("Lifehacker", "https://lifehacker.com/rss"),
]


def init_db():
    """
    Initializes the database:
    1. Activates the 'pgvector' extension (Crucial for AI).
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


def process_feeds():
    """
    Iterates through the massive RSS_SOURCES list.
    """
    db = SessionLocal()
    try:
        total = len(RSS_SOURCES)
        print(f"🚀 Starting InsightFeed MASSIVE ETL Pipeline. Targets: {total}\n")

        for index, (source_name, url) in enumerate(RSS_SOURCES, 1):
            print(f"📡 Processing [{index}/{total}]: {source_name}")

            # Start the ETL process for this specific URL
            # Note: Some feeds might fail due to timeout, we continue to next.
            try:
                fetch_and_store_rss(
                    db=db,
                    rss_url=url,
                    source_name=source_name
                )
            except Exception as feed_error:
                print(f"   ⚠️ Could not fetch {source_name}: {feed_error}")

            print("-" * 30)

    except Exception as e:
        print(f"❌ Critical Error in Collector: {e}")
    finally:
        db.close()
        print("\n✨ Ingestion Complete. Database session closed.")


if __name__ == "__main__":
    # 1. Ensure DB is ready
    init_db()

    # 2. Run the massive collector
    process_feeds()