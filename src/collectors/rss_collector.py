import feedparser
from datetime import datetime
from time import mktime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database.crud import create_news
from src.processors.embedder import global_embedder

# 🚫 BANNED TITLES (Generic, useless headers)
BANNED_TITLES = [
    "business", "politics", "sport", "technology", "world",
    "opinion", "letters", "editor's picks", "morning briefing",
    "evening briefing", "today's paper", "correction", "news"
]


def fetch_and_store_rss(db: Session, rss_url: str, source_name: str) -> None:
    """
    Fetches news, VALIDATES them (filters out garbage), embeds, and stores.
    """
    print(f"🔌 Connecting to RSS Feed: {source_name}...")

    feed = feedparser.parse(rss_url)
    saved_count = 0

    if not feed.entries:
        print("⚠️ No entries found.")
        return

    for entry in feed.entries:
        try:
            title = entry.title.strip()

            # --- 🛡️ JUNK FILTER (Çöp Filtresi) ---

            # 1. Filter out very short titles (e.g., "Ads", "More")
            if len(title) < 10:
                print(f"   🗑️ Skipped (Too short): {title}")
                continue

            # 2. Filter out generic section headers
            if title.lower() in BANNED_TITLES:
                print(f"   🗑️ Skipped (Generic title): {title}")
                continue
            # -------------------------------------

            pub_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_date = datetime.fromtimestamp(mktime(entry.published_parsed))

            summary_text = entry.summary if hasattr(entry, 'summary') else ''
            text_to_embed = f"{title}. {summary_text}"

            embedding_vector = global_embedder.embed_text(text_to_embed)

            create_news(
                db=db,
                title=title,
                content=summary_text or title,
                url=entry.link,
                source=source_name,
                pub_date=pub_date,
                embedding=embedding_vector
            )

            saved_count += 1
            print(f"   ✅ Saved: {title[:30]}...")

        except IntegrityError:
            db.rollback()
            # Commenting this out to reduce noise in massive ingestion
            # print(f"   ⏭️ Duplicate skipped.")

        except Exception as e:
            db.rollback()
            print(f"   ❌ Error: {e}")

    print(f"🏁 Source Done. Added {saved_count} valid articles.\n")