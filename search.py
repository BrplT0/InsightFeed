from sqlalchemy import select
from typing import List
from src.database.db import SessionLocal
from src.database.models import News
from src.processors.embedder import global_embedder


def search_semantic(user_query: str, limit: int = 5) -> List[News]:
    """
    Performs a semantic search on the news database using vector embeddings.
    Calculates L2 distance between the query vector and stored news vectors.

    Args:
        user_query (str): The search phrase or question from the user.
        limit (int): Maximum number of results to return. Defaults to 5.

    Returns:
        List[News]: A list of the most relevant News objects found in the database.
    """
    db = SessionLocal()
    results = []

    try:
        # 1. Convert user query to vector (embedding)
        query_vector = global_embedder.embed_text(user_query)

        if not query_vector:
            print("⚠️ Empty query vector generated.")
            return []

        # 2. Execute Vector Search (L2 Distance)
        # Finds the nearest neighbors in the 384-dimensional space
        statement = select(News).order_by(
            News.embedding.l2_distance(query_vector)
        ).limit(limit)

        results = db.execute(statement).scalars().all()

    except Exception as e:
        print(f"❌ Search failed: {e}")
    finally:
        db.close()

    return results


if __name__ == "__main__":
    # --- MANUAL TEST AREA ---
    test_query = "I need clothes for winter"

    print(f"🔎 Testing Search for: '{test_query}'")
    hits = search_semantic(test_query)

    print(f"✅ Found {len(hits)} results:\n")
    for news in hits:
        print(f"   📌 {news.title}")
        print(f"      🔗 {news.url}")
        print("-" * 30)