import feedparser
from datetime import datetime
from time import mktime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError  # For handling duplicates properly

from src.database.crud import create_news
from src.processors.embedder import global_embedder


def fetch_and_store_rss(db: Session, rss_url: str, source_name: str) -> None:
    """
    Fetches news articles from a given RSS URL, generates AI embeddings,
    and stores them in the database.

    Args:
        db (Session): Active database session.
        rss_url (str): The URL of the RSS feed (e.g., Wired, CNN).
        source_name (str): A readable name for the source (e.g., 'Wired Tech').
    """
    print(f"🔌 Connecting to RSS Feed: {source_name} ({rss_url})...")

    # 1. Parse the RSS Feed
    feed = feedparser.parse(rss_url)
    saved_count = 0

    if not feed.entries:
        print("⚠️ No entries found in the RSS feed.")
        return

    # 2. Iterate through each news item
    for entry in feed.entries:
        try:
            # Parse publication date (handle format differences)
            pub_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_date = datetime.fromtimestamp(mktime(entry.published_parsed))

            # Prepare text for AI Embedding
            # We combine title and summary to give the AI more context.
            summary_text = entry.summary if hasattr(entry, 'summary') else ''
            text_to_embed = f"{entry.title}. {summary_text}"

            # Generate Vector (The heavy lifting)
            embedding_vector = global_embedder.embed_text(text_to_embed)

            # 3. Store in Database
            create_news(
                db=db,
                title=entry.title,
                content=summary_text or entry.title,  # Fallback to title if summary is empty
                url=entry.link,
                source=source_name,
                pub_date=pub_date,
                embedding=embedding_vector
            )

            saved_count += 1
            print(f"   ✅ Saved: {entry.title[:30]}...")

        except IntegrityError:
            # This catches "UniqueViolation" errors from PostgreSQL
            # (i.e., we already have this URL in the database)
            db.rollback()  # Important: Reset session state to continue
            print(f"   ⏭️  Skipping duplicate: {entry.title[:20]}...")

        except Exception as e:
            # Catch other unexpected errors
            db.rollback()
            print(f"   ❌ Error processing entry: {e}")

    print(f"🏁 Processing Complete! Added {saved_count} new articles.\n")