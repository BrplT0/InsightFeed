# 🚀 InsightFeed

> An AI-powered news analysis engine that understands meaning, not just keywords

**InsightFeed** transforms how you discover and explore news content. By leveraging semantic vector embeddings and similarity search, it enables you to find relevant articles based on context and meaning—even when exact keywords don't match.

---

## ✨ What Makes InsightFeed Special?

Traditional search engines look for exact word matches. InsightFeed understands *meaning*. 

🔍 **Example:**  
Search for *"I need winter gear"* → Discover articles about heaters, wool clothing, and cold weather equipment—without those exact words appearing in your query.

---

## 🎯 Key Features

### 🤖 **Intelligent Data Pipeline**
- Automated ETL system that fetches and processes news from RSS feeds
- Supports major sources like Wired, Bloomberg, and more
- Clean, structured data ready for analysis

### 🧠 **AI-Powered Embeddings**
- Converts articles into 384-dimensional semantic vectors
- Uses `all-MiniLM-L6-v2` from Sentence-Transformers
- Captures contextual meaning beyond simple keywords

### ⚡ **Lightning-Fast Vector Search**
- PostgreSQL 16 with pgvector extension
- Optimized similarity search with HNSW indexing
- Sub-second query responses even with thousands of articles

### 🔎 **Natural Language Queries**
- Search using conversational language
- Context-aware results ranked by semantic similarity
- No need for boolean operators or complex syntax

---

## 🏗️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.12+ |
| **Database** | PostgreSQL 16 + pgvector |
| **ORM** | SQLAlchemy 2.0 (strongly typed) |
| **AI Model** | all-MiniLM-L6-v2 (Hugging Face) |
| **RSS Parser** | feedparser |
| **Container** | Docker & Docker Compose |
| **Package Manager** | Poetry |

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:

- ✅ [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- ✅ [Python 3.10+](https://www.python.org/downloads/)
- ✅ [Poetry](https://python-poetry.org/docs/)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/InsightFeed.git
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

> ⚠️ **Important:** Never commit `.env` to version control

**4. Start the database**
```bash
docker-compose up -d
```

This launches PostgreSQL with pgvector in a Docker container.

---

## 💡 Usage

### Ingest News Data

Fetch articles, generate embeddings, and populate the database:

```bash
poetry run python ingest.py
```

> 📝 **Note:** First run automatically initializes database tables and extensions

### Search with Natural Language

Query your knowledge base using semantic search:

```bash
poetry run python search.py
```

**Example Interaction:**

```
🔍 Query: "I am feeling cold"

📰 Results:
  1. "Best Merino Wool T-Shirts for Winter" (similarity: 0.87)
  2. "Top Space Heaters of 2024" (similarity: 0.84)
  3. "How to Stay Warm Without Heating Bills" (similarity: 0.81)
```

---

## 📁 Project Structure

```
insightfeed/
├── 📄 docker-compose.yml      # Infrastructure orchestration
├── 📄 pyproject.toml          # Python dependencies (Poetry)
├── 📄 ingest.py               # ETL pipeline entry point
├── 📄 search.py               # Semantic search interface
├── 📄 .env                    # Environment secrets (gitignored)
├── 📂 src/
│   ├── 📂 collectors/         # RSS feed ingestion logic
│   ├── 📂 processors/         # Embedding generation & AI
│   └── 📂 database/           # Models, connections & CRUD ops
├── 📄 LICENSE                 # MIT License
└── 📄 README.md               # You are here
```

---

## 🛠️ How It Works

### The Semantic Search Pipeline

```
1. 📡 RSS Ingestion
   └─> Fetch articles from configured feeds
   
2. 🧹 Data Cleaning
   └─> Extract title, content, metadata
   
3. 🤖 Embedding Generation
   └─> Convert text → 384D vectors
   
4. 💾 Vector Storage
   └─> Store in PostgreSQL with pgvector
   
5. 🔍 Similarity Search
   └─> Query embedding vs. stored vectors
   
6. 📊 Ranked Results
   └─> Return top matches by cosine similarity
```

---

## 🔧 Configuration

### Adding New RSS Feeds

Edit the feed configuration in `ingest.py`:

```python
# Target RSS Feed
        rss_url = "https://www.wired.com/feed/category/gear/latest/rss"
```

### Adjusting Search Parameters

Modify search behavior in `search.py`:

```python
results = search_semantic(
    query="your query",
    limit=5,          # Number of results
)
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. ✍️ Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎉 Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Sentence-Transformers](https://www.sbert.net/) for the embedding model
- [pgvector](https://github.com/pgvector/pgvector) for vector similarity search
- The open-source community for amazing tools and libraries

---

## 📧 Contact & Support

- 🐛 [Report a Bug](https://github.com/YOUR_USERNAME/InsightFeed/issues)
- 💡 [Request a Feature](https://github.com/YOUR_USERNAME/InsightFeed/issues)
- 📖 [Documentation](https://github.com/YOUR_USERNAME/InsightFeed/wiki)

---

<div align="center">

**Built with ❤️ using AI and Open Source**

⭐ Star this repo if you find it useful!

</div>