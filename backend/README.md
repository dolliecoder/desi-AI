# CodeSwitch AI - Backend

Multilingual coding assistant backend for Indian developers.

## Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

2. Run setup script (recommended):
```bash
python setup.py
```

This will:
- Check Python version
- Verify virtual environment
- Install dependencies
- Create .env file
- Check data directory

3. Manual installation (alternative):
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env and add your Gemini API key
# Get key from: https://makersuite.google.com/app/apikey
```

4. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Troubleshooting

If you encounter issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common problems and solutions.

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
```bash
GET /health
```

### Query Normalization
```bash
POST /normalize
Content-Type: application/json

{
  "query": "Bhai async await kab use karte hai?"
}
```

Response:
```json
{
  "original_query": "Bhai async await kab use karte hai?",
  "normalized_query": "When to use async await in JavaScript",
  "detected_language": "Hinglish",
  "explanation_style": "Beginner"
}
```

### Ask a Question (RAG-Powered)
```bash
POST /ask
Content-Type: application/json

{
  "query": "Bhai async await kab use karte hai?"
}
```

Response:
```json
{
  "query": "Bhai async await kab use karte hai?",
  "normalized_query": "When to use async await in JavaScript",
  "answer": "Async/await JavaScript mein asynchronous operations ko handle karne ke liye use hota hai...",
  "context_used": [
    {
      "content": "Async/await is syntactic sugar over Promises...",
      "source": "python_basics.md",
      "score": 0.91
    }
  ],
  "detected_language": "Hinglish",
  "explanation_style": "Beginner"
}
```

### Document Ingestion
```bash
POST /rag/ingest
Content-Type: application/json

{
  "force_reload": false
}
```

### Semantic Search
```bash
POST /rag/search
Content-Type: application/json

{
  "query": "When to use async await in JavaScript",
  "top_k": 3,
  "use_reranking": true
}
```

Response:
```json
{
  "query": "When to use async await in JavaScript",
  "results": [
    {
      "content": "Async/await is syntactic sugar over Promises...",
      "source": "python_basics.md",
      "score": 0.91,
      "metadata": {"topic": "async", "framework": "JavaScript"}
    }
  ],
  "total_results": 3
}
```

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── routes/                # API endpoints
│   ├── health.py         # Health check
│   └── normalization.py  # Query normalization
├── services/              # Business logic
│   ├── gemini_service.py # Gemini API integration
│   └── normalization_service.py # Query normalization
├── models/                # Pydantic models
│   └── normalization.py  # Normalization request/response
├── prompts/               # LLM prompts
│   ├── system_prompts.py # General system prompts
│   └── normalization_prompts.py # Normalization prompts
├── vectorstore/           # ChromaDB storage
└── utils/                 # Helper functions
    └── config.py         # Configuration management
```

## Performance

This backend is optimized for fast local demo performance:

- **Startup:** <20 seconds (first time)
- **Ingestion:** ~10 seconds for 3 documents
- **Search:** ~100-150ms per query
- **Memory:** ~1.5GB RAM

**Optimizations:**
- Lightweight embedding model (~90MB vs 2.2GB)
- Reranking disabled for speed
- Efficient ChromaDB storage

See [PERFORMANCE_OPTIMIZATIONS.md](PERFORMANCE_OPTIMIZATIONS.md) for details.
