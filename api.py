from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Import core logic and models
from search import search_semantic
from src.database.models import News

# 1. Initialize FastAPI Application
# This is the main entry point for the web server.
app = FastAPI(
    title="InsightFeed API",
    description="AI-Powered Semantic Search Engine for News. Built with FastAPI, PostgreSQL, and Sentence-Transformers.",
    version="1.0.0"
)


# 2. Define Data Models (Schemas)
# Pydantic models define the structure of the data exchanged between the API and the client.
# This ensures that the JSON response is always consistent and documented.

class NewsResponse(BaseModel):
    """
    Schema for the news article response.
    Hides internal database IDs and exposes only relevant fields.
    """
    title: str
    url: str
    source: Optional[str] = None
    pub_date: Optional[datetime] = None

    class Config:
        # Essential for compatibility with SQLAlchemy ORM objects.
        # It tells Pydantic to read data from attributes (e.g., news.title) instead of a dict.
        from_attributes = True


# 3. Define Endpoints (Routes)

@app.get("/")
def health_check():
    """
    Root endpoint to verify if the API is up and running.
    """
    return {
        "status": "online",
        "system": "InsightFeed AI Engine",
        "version": "1.0.0"
    }


@app.get("/search", response_model=List[NewsResponse])
def search_news(q: str, limit: int = 5):
    """
    Performs a semantic search on the news database.

    Args:
        q (str): The user's search query (natural language).
        limit (int): Maximum number of results to return. Defaults to 5.

    Returns:
        List[NewsResponse]: A list of relevant news articles sorted by semantic similarity.
    """
    # Input validation
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Query parameter 'q' cannot be empty.")

    print(f"🌍 API Request received: Searching for '{q}' with limit {limit}...")

    try:
        # Call the core semantic search logic
        results = search_semantic(user_query=q, limit=limit)
        return results
    except Exception as e:
        # Log the error and return a 500 Internal Server Error
        print(f"❌ API Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during search.")