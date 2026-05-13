# CodeSwitch AI - Full Stack Guide

Complete guide for running the full CodeSwitch AI application.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    CodeSwitch AI                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Frontend (Next.js)          Backend (FastAPI)          │
│  ┌──────────────────┐       ┌──────────────────┐       │
│  │                  │       │                  │       │
│  │  Chat Interface  │──────▶│  /ask endpoint   │       │
│  │                  │       │                  │       │
│  │  - Input box     │       │  1. Normalize    │       │
│  │  - Response UI   │       │  2. Retrieve     │       │
│  │  - Sources       │       │  3. Generate     │       │
│  │                  │       │                  │       │
│  └──────────────────┘       └──────────────────┘       │
│                                      │                  │
│                                      ▼                  │
│                             ┌──────────────────┐       │
│                             │   Services       │       │
│                             │                  │       │
│                             │  - Gemini API    │       │
│                             │  - ChromaDB      │       │
│                             │  - Embeddings    │       │
│                             └──────────────────┘       │
└─────────────────────────────────────────────────────────┘
```

## Quick Start (Both Services)

### Terminal 1: Backend

```bash
# Navigate to backend
cd backend

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Start backend
python main.py
```

Backend runs on: http://localhost:8000

### Terminal 2: Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start frontend
npm run dev
```

Frontend runs on: http://localhost:3000

## Complete Setup (First Time)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env and add GEMINI_API_KEY
# Get key from: https://makersuite.google.com/app/apikey

# Test services
python test_services.py

# Start server
python main.py
```

### 2. Ingest Documents

```bash
# In a new terminal, with backend running
curl -X POST http://localhost:8000/rag/ingest \
  -H "Content-Type: application/json" \
  -d '{"force_reload": false}'
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Test the Application

1. Open http://localhost:3000
2. Try: "Bhai async await kab use karte hai?"
3. View the AI-powered response!

## Project Structure

```
sarvamai/
├── backend/                 # FastAPI backend
│   ├── main.py             # App entry point
│   ├── routes/             # API endpoints
│   │   ├── health.py       # Health check
│   │   ├── normalization.py # Query normalization
│   │   ├── rag.py          # RAG operations
│   │   └── ask.py          # Main Q&A endpoint
│   ├── services/           # Business logic
│   │   ├── gemini_service.py
│   │   ├── embedding_service.py
│   │   ├── vectorstore_service.py
│   │   ├── retrieval_service.py
│   │   ├── normalization_service.py
│   │   └── ask_service.py
│   ├── models/             # Pydantic models
│   ├── prompts/            # LLM prompts
│   └── utils/              # Configuration
│
├── frontend/               # Next.js frontend
│   ├── app/
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Main chat UI
│   │   └── globals.css     # Styles
│   ├── package.json
│   └── tailwind.config.ts
│
└── data/                   # Knowledge base
    ├── python_basics.md
    ├── react_debugging.md
    └── dsa_patterns.md
```

## API Endpoints

### Backend (http://localhost:8000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/normalize` | POST | Normalize multilingual query |
| `/rag/ingest` | POST | Ingest documents |
| `/rag/search` | POST | Semantic search |
| `/ask` | POST | **Main endpoint** - Full RAG pipeline |

### Frontend (http://localhost:3000)

| Route | Description |
|-------|-------------|
| `/` | Main chat interface |

## Features

### Backend Features

- ✅ Multilingual query normalization (Gemini)
- ✅ Semantic search (ChromaDB + Embeddings)
- ✅ RAG-powered answers (Gemini + Context)
- ✅ Language detection (English/Hindi/Hinglish)
- ✅ Style detection (Beginner/Interview/Advanced)
- ✅ Lightweight models (optimized for demos)

### Frontend Features

- ✅ Single-page chat interface
- ✅ Dark modern UI
- ✅ Responsive design
- ✅ Real-time loading states
- ✅ Example queries
- ✅ Source display
- ✅ Metadata visualization

## Example Usage

### 1. Ask in Hinglish

**Input:**
```
Bhai async await kab use karte hai?
```

**Output:**
- **Normalized:** "When to use async await in JavaScript"
- **Language:** Hinglish
- **Style:** Beginner
- **Answer:** Detailed explanation in Hinglish
- **Sources:** Relevant code snippets from knowledge base

### 2. Ask in English

**Input:**
```
Explain binary search algorithm for beginners
```

**Output:**
- **Normalized:** "Explain binary search algorithm"
- **Language:** English
- **Style:** Beginner
- **Answer:** Step-by-step explanation with examples
- **Sources:** Algorithm patterns from knowledge base

### 3. Advanced Query

**Input:**
```
DFS recursion mein stack overflow kyun hota hai internally?
```

**Output:**
- **Normalized:** "Why does DFS recursion cause stack overflow"
- **Language:** Hinglish
- **Style:** Advanced
- **Answer:** Technical explanation of call stack and recursion depth
- **Sources:** DSA patterns with implementation details

## Performance

### Backend
- **Startup:** <20 seconds
- **Ingestion:** ~10 seconds (3 documents)
- **Query processing:** 2-4 seconds
  - Normalization: ~1s
  - Retrieval: ~0.1s
  - Generation: ~1-3s

### Frontend
- **Initial load:** <1 second
- **Response display:** Instant (after backend responds)
- **Bundle size:** ~200KB

## Development Workflow

### 1. Backend Development

```bash
cd backend

# Make changes to code
# ...

# Restart server (auto-reload enabled)
# Server will restart automatically

# Test changes
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'
```

### 2. Frontend Development

```bash
cd frontend

# Make changes to code
# ...

# Next.js auto-reloads
# Just refresh browser

# Check for errors
npm run lint
```

## Troubleshooting

### Backend Issues

**Issue:** "GEMINI_API_KEY not configured"
```bash
# Edit .env and add your key
GEMINI_API_KEY=your_actual_key_here
```

**Issue:** "No module named 'google.generativeai'"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Issue:** Port 8000 in use
```bash
# Change port in .env
API_PORT=8001
```

### Frontend Issues

**Issue:** "Failed to get response"
```bash
# Check backend is running
curl http://localhost:8000/health

# If not, start it
cd backend
python main.py
```

**Issue:** Port 3000 in use
```bash
# Use different port
PORT=3001 npm run dev
```

**Issue:** Styling not working
```bash
# Rebuild
npm run dev
```

## Production Deployment

### Backend

```bash
cd backend

# Install production dependencies
pip install -r requirements.txt

# Set production environment
export GEMINI_API_KEY=your_key

# Run with gunicorn (recommended)
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend

```bash
cd frontend

# Build for production
npm run build

# Start production server
npm start
```

## Environment Variables

### Backend (.env)

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key

# Optional
API_HOST=0.0.0.0
API_PORT=8000
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=./vectorstore/chroma_db
```

### Frontend (.env.local)

```bash
# Optional (defaults to localhost:8000)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing

### Backend Tests

```bash
cd backend

# Run service tests
python test_services.py

# Test individual endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/normalize \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

### Frontend Tests

```bash
cd frontend

# Lint
npm run lint

# Manual testing
# Open http://localhost:3000 and test UI
```

## Documentation

### Backend Docs
- `backend/README.md` - Main documentation
- `backend/QUICKSTART.md` - Quick start guide
- `backend/INSTALL.md` - Installation guide
- `backend/TROUBLESHOOTING.md` - Common issues
- `backend/ASK_ENDPOINT_GUIDE.md` - /ask endpoint details
- `backend/PERFORMANCE_OPTIMIZATIONS.md` - Performance info

### Frontend Docs
- `frontend/README.md` - Main documentation
- `frontend/QUICKSTART.md` - Quick start guide

### Full Stack
- `FULL_STACK_GUIDE.md` - This file

## Tips for Demo

1. **Prepare Backend**
   - Start backend first
   - Ingest documents
   - Test with curl

2. **Prepare Frontend**
   - Start frontend
   - Test example queries
   - Check all features work

3. **Demo Flow**
   - Show welcome screen
   - Click example query
   - Highlight loading state
   - Show response with sources
   - Demonstrate language detection
   - Try different query styles

4. **Talking Points**
   - Multilingual support (English/Hindi/Hinglish)
   - RAG-powered answers
   - Context retrieval from knowledge base
   - Automatic language and style detection
   - Fast, optimized for demos

## Next Steps

1. ✅ Backend running
2. ✅ Frontend running
3. ✅ Documents ingested
4. ✅ Test queries working
5. 🎉 Ready to demo!

## Support

- Backend issues: See `backend/TROUBLESHOOTING.md`
- Frontend issues: See `frontend/README.md`
- API docs: http://localhost:8000/docs (Swagger UI)

---

**Built for hackathons. Optimized for demos. Ready to impress! 🚀**
