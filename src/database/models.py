from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from pgvector.sqlalchemy import Vector

# Base class for SQLAlchemy models
Base = declarative_base()

class News(Base):
    """
    SQLAlchemy model representing a news article.
    Stores metadata (title, url) and the semantic vector embedding for AI search.
    """
    __tablename__ = 'news'

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Core Content
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    # Metadata
    # unique=True ensures we don't store the same article twice
    url = Column(String, nullable=False, unique=True)
    source = Column(String, nullable=True)

    # Timestamps
    pub_date = Column(DateTime, nullable=True)            # Original publication date form RSS
    created_at = Column(DateTime, default=datetime.utcnow) # Record insertion time

    # Vector Embedding
    # We use 384 dimensions because 'all-MiniLM-L6-v2' model outputs 384 floats.
    # This column enables semantic search via pgvector.
    embedding = Column(Vector(384))

    def __repr__(self):
        """String representation for debugging"""
        return f"<News(id={self.id}, title='{self.title}', source='{self.source}')>"