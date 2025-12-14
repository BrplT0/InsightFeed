from sqlalchemy.orm import Session
from src.database.models import News
from datetime import datetime
import numpy as np
from typing import List, Union


def create_news(
        db: Session,
        title: str,
        content: str,
        url: str,
        source: str,
        embedding: Union[List[float], np.ndarray],
        pub_date: datetime = None
) -> News:
    """
    Creates a new news record in the database.

    Args:
        db (Session): Active database session.
        title (str): Headline of the news.
        content (str): Summary or full content of the news.
        url (str): Unique URL of the news article.
        source (str): Source name (e.g., 'Wired').
        embedding (List[float] | np.ndarray): The vector representation of the text.
        pub_date (datetime, optional): Publication date. Defaults to None.

    Returns:
        News: The created News object.
    """

    # ⚠️ Compatibility Check:
    # SQLAlchemy/pgvector expects a standard Python list.
    # If Sentence-Transformers returns a NumPy array, we must convert it.
    if isinstance(embedding, np.ndarray):
        embedding_to_save = embedding.tolist()
    else:
        embedding_to_save = embedding

    new_entry = News(
        title=title,
        content=content,
        url=url,
        source=source,
        embedding=embedding_to_save,
        pub_date=pub_date
    )

    db.add(new_entry)  # Add to transaction
    db.commit()  # Commit changes to database
    db.refresh(new_entry)  # Refresh instance to get the generated ID

    return new_entry