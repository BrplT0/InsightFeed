import feedparser
from datetime import datetime
from time import mktime
from sqlalchemy.orm import Session
from src.database.crud import create_news
from src.processors.embedder import global_embedder


def fetch_and_store_rss(db: Session, rss_url: str, source_name: str):
    """
    Verilen RSS adresinden haberleri çeker ve veritabanına yazar.
    """
    print(f"Bağlanılıyor: {source_name} ({rss_url})")

    feed = feedparser.parse(rss_url)

    saved_count = 0

    for entry in feed.entries:
        try:
            pub_date = None
            if hasattr(entry, 'published_parsed'):
                pub_date = datetime.fromtimestamp(mktime(entry.published_parsed))

            text_to_embed = f"{entry.title}. {entry.summary if hasattr(entry, 'summary') else ''}"

            embedding_vector = global_embedder.embed_text(text_to_embed)

            create_news(
                db=db,
                title=entry.title,
                content=entry.summary if hasattr(entry, 'summary') else entry.title,
                url=entry.link,
                source=source_name,
                pub_date=pub_date,
                embedding=embedding_vector
            )
            saved_count += 1
            print(f"   ✅ Kaydedildi: {entry.title[:30]}...")

        except Exception as e:
            # Eğer hata "UniqueViolation" ise (yani haber zaten varsa) pas geç
            if "unique constraint" in str(e).lower():
                print(f"   zzz Zaten var: {entry.title[:15]}...")
                db.rollback()  # İşlemi geri al ki diğerlerine devam edebilelim
            else:
                print(f"   ❌ Hata oluştu: {e}")
                db.rollback()

    print(f"🏁 Tamamlandı! Toplam {saved_count} yeni haber eklendi.\n")