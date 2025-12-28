# 🚀 InsightFeed API

> An AI-powered semantic search engine and news aggregator API.
> **Understand meaning, don't just match keywords.**

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker)

**InsightFeed** is a modern backend system that aggregates news from 50+ global sources, filters out noise, generates AI embeddings, and serves results via a high-performance REST API. It leverages **PostgreSQL pgvector** to perform semantic similarity searches, allowing users to find relevant content based on context rather than exact keywords.

---

## ✨ What's New in v1.0?

- **🌍 Massive Scale:** Pre-configured to ingest data from **50+ top-tier sources** (Wired, NASA, Bloomberg, IGN, BBC, etc.).
- **🛡️ Smart Junk Filter:** Automatically detects and rejects low-quality content (clickbait, short titles, generic headers like "Business" or "Politics").
- **⚡ RESTful API:** Built with **FastAPI**, providing a full Swagger UI for interaction.
- **🧠 Advanced AI:** Uses `all-MiniLM-L6-v2` to understand the nuance of headlines and summaries.

---

## 🎯 Key Features

### 🤖 **Intelligent ETL Pipeline**
- **Automated Ingestion:** Fetches thousands of articles in seconds.
- **Noise Reduction:** Custom algorithms filter out generic and "garbage" titles to ensure high-quality search results.
- **Robustness:** Handles connection errors and duplicates gracefully.

### 🧠 **AI-Powered Embeddings**
- Converts text into **384-dimensional dense vectors**.
- Captures semantic meaning (e.g., understands that *"Cupertino Giant"* refers to *Apple*).

### ⚡ **Lightning-Fast Vector Search**
- **pgvector Extension:** Native vector similarity search inside PostgreSQL.
- **HNSW Indexing:** Optimized for sub-second query responses even with large datasets.

### 🌐 **Modern API Architecture**
- **FastAPI:** High-performance, async-ready web framework.
- **Swagger UI:** Automatic interactive documentation at `/docs`.
- **Pydantic:** Strong data validation and serialization.

---

## 🏗️ Technology Stack

| Component | Technology | Description |
|-----------|-----------|-------------|
| **Core** | Python 3.12 | The brain of the operation. |
| **API** | FastAPI + Uvicorn | High-performance ASGI web server. |
| **Database** | PostgreSQL 16 | Relational storage. |
| **Vector Search** | pgvector | Extension for AI similarity search. |
| **ORM** | SQLAlchemy 2.0 | Modern, strongly-typed database interaction. |
| **AI Model** | Sentence-Transformers | `all-MiniLM-L6-v2` model via Hugging Face. |
| **Container** | Docker & Compose | Infrastructure orchestration. |
| **Package Mgr** | Poetry | Dependency management. |

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:
- ✅ [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- ✅ [Python 3.10+](https://www.python.org/downloads/)
- ✅ [Poetry](https://python-poetry.org/docs/)

### Installation

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_USERNAME/InsightFeed.git](https://github.com/YOUR_USERNAME/InsightFeed.git)
cd InsightFeed

```

**2. Install dependencies**

```bash
poetry install

```

**3. Configure environment**
Create a `.env` file in the project root:

```env
# Database Configuration
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=insightfeed_db
DB_HOST=localhost
DB_PORT=5432

```

**4. Start the Infrastructure**

```bash
docker-compose up -d

```

*This spins up the PostgreSQL container with the pgvector extension enabled.*

---

## 💡 Usage Guide

### 1️⃣ Ingest Data (ETL)

Populate your database with thousands of articles from the 50+ configured sources.

```bash
poetry run python ingest.py

```

*> Watch as the system fetches, filters, embeds, and indexes news from around the world.*

### 2️⃣ Start the API Server

Launch the FastAPI backend.

```bash
poetry run uvicorn api:app --reload

```

*> The server will start at http://127.0.0.1:8000*

### 3️⃣ Search via Swagger UI

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)**

1. Click on the **`/search`** endpoint.
2. Click **Try it out**.
3. Enter a natural language query (e.g., *"Latest AI breakthroughs"* or *"Crypto market trends"*).
4. Hit **Execute** and see the magic! 🎩✨

---

## 📁 Project Structure

```
insightfeed/
├── 📄 docker-compose.yml      # Infrastructure (Postgres + pgvector)
├── 📄 pyproject.toml          # Dependencies
├── 📄 api.py                  # FastAPI Application (Entry Point)
├── 📄 ingest.py               # ETL Pipeline Entry Point
├── 📄 .env                    # Secrets (Not committed)
├── 📂 src/
│   ├── 📂 collectors/         # RSS logic & Junk Filters
│   ├── 📂 processors/         # Embedding generation
│   └── 📂 database/           # Models & CRUD operations
└── 📄 README.md               # Documentation

```

---

## 🔧 Configuration

### Adding Custom Sources

To add more RSS feeds, edit the `RSS_SOURCES` list in `ingest.py`:

```python
RSS_SOURCES = [
    ("My Custom Feed", "[https://example.com/rss](https://example.com/rss)"),
    # ... existing 50+ sources
]

```

### Adjusting the Junk Filter

To change validation logic, edit `src/collectors/rss_collector.py`:

```python
BANNED_TITLES = ["business", "politics", "sport", ...] # Add words here
if len(title) < 10: # Adjust minimum length
    continue

```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/cool-stuff`).
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the **MIT License**.

---

<div align="center">

**Built with ❤️ by Berat Polat**

</div>
