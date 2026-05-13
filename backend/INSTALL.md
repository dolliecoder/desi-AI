# Installation Guide - CodeSwitch AI Backend

## Quick Start (Recommended)

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 4. Run setup script
python setup.py

# 5. Edit .env and add your Gemini API key
# Get key from: https://makersuite.google.com/app/apikey

# 6. Test services (optional but recommended)
python test_services.py

# 7. Start server
python main.py
```

## Detailed Installation Steps

### Step 1: Prerequisites

**Required:**
- Python 3.9 or higher
- pip (comes with Python)
- Internet connection (for downloading models)

**Check your Python version:**
```bash
python --version
# Should show: Python 3.9.x or higher
```

### Step 2: Virtual Environment

**Why?** Isolates project dependencies from system Python.

**Create virtual environment:**
```bash
python -m venv venv
```

**Activate virtual environment:**
```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

**Verify activation:**
Your prompt should show `(venv)` prefix.

### Step 3: Install Dependencies

**Option A: Automated (Recommended)**
```bash
python setup.py
```

**Option B: Manual**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**This will install:**
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Google Generative AI (Gemini SDK)
- ChromaDB (vector database)
- Sentence Transformers (embeddings)
- PyTorch (ML framework)
- And other dependencies

**Installation time:** 5-10 minutes (depending on internet speed)

### Step 4: Configure Environment

**Create .env file:**
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

**Edit .env file:**
```bash
# Open in your favorite editor
notepad .env  # Windows
nano .env     # Linux/Mac
```

**Add your Gemini API key:**
```
GEMINI_API_KEY=your_actual_api_key_here
```

**Get a free Gemini API key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key and paste in .env

### Step 5: Prepare Data Directory

**Create data directory (if not exists):**
```bash
# Windows
mkdir ..\data

# Linux/Mac
mkdir ../data
```

**Add markdown files:**
Place your knowledge base markdown files in `../data/`

**Example files provided:**
- `python_basics.md`
- `react_debugging.md`
- `dsa_patterns.md`

**Markdown format:**
```markdown
---
topic: Your Topic
framework: Python/React/etc
difficulty: Beginner/Intermediate/Advanced
---

# Your Content Here
```

### Step 6: Verify Installation

**Run test script:**
```bash
python test_services.py
```

**Expected output:**
```
============================================================
CodeSwitch AI - Service Tests
============================================================

1. Testing Configuration...
   ✓ API Host: 0.0.0.0
   ✓ API Port: 8000
   ✓ Embedding Model: BAAI/bge-m3
   ✓ ChromaDB Dir: ./vectorstore/chroma_db
   ✓ Gemini API Key: ********************abcd

2. Testing Gemini Service...
   ✓ Gemini API initialized successfully
   ✓ Response: Hello

3. Testing Embedding Service...
   Loading embedding model: BAAI/bge-m3
   ✓ Embedding model loaded successfully (dimension: 1024)
   ✓ Embedding dimension: 1024
   ✓ Sample values: [0.123, -0.456, 0.789]

4. Testing Vector Store Service...
   ✓ ChromaDB initialized with 0 documents
   ✓ Documents in store: 0

5. Testing Normalization Service...
   ✓ Original: Bhai async await kab use karte hai?
   ✓ Normalized: When to use async await in JavaScript
   ✓ Language: Hinglish
   ✓ Style: Beginner

============================================================
Test Summary
============================================================
✓ Configuration
✓ Gemini Service
✓ Embedding Service
✓ Vector Store
✓ Normalization

✓ All tests passed! Backend is ready.
============================================================
```

### Step 7: Start Server

**Run the server:**
```bash
python main.py
```

**Expected output:**
```
============================================================
CodeSwitch AI - Backend Startup
============================================================
✓ Gemini API key configured
✓ Embedding model: BAAI/bge-m3
✓ ChromaDB directory: ./vectorstore/chroma_db

============================================================
Services will initialize on first use:
  - Gemini API (on first /normalize request)
  - Embedding model (on first /rag/ingest or /rag/search)
  - Reranker model (on first /rag/search with reranking)
============================================================

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Access the API:**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## First Time Usage

### 1. Check Health
```bash
curl http://localhost:8000/health
```

### 2. Ingest Documents
```bash
curl -X POST http://localhost:8000/rag/ingest \
  -H "Content-Type: application/json" \
  -d '{"force_reload": false}'
```

**Note:** First ingestion will download embedding models (~500MB). This is one-time only.

### 3. Test Normalization
```bash
curl -X POST http://localhost:8000/normalize \
  -H "Content-Type: application/json" \
  -d '{"query": "Bhai async await kab use karte hai?"}'
```

### 4. Test Search
```bash
curl -X POST http://localhost:8000/rag/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "When to use async await",
    "top_k": 3,
    "use_reranking": true
  }'
```

## Common Issues

### Issue: "ModuleNotFoundError"
**Solution:** Ensure virtual environment is activated and dependencies are installed.
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "GEMINI_API_KEY not configured"
**Solution:** Add your API key to .env file.
```bash
# Edit .env
GEMINI_API_KEY=your_actual_key_here
```

### Issue: "Port 8000 already in use"
**Solution:** Change port in .env or kill the process.
```bash
# Change port
API_PORT=8001

# Or kill process (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: Slow first request
**Expected:** Models load on first use (30-60 seconds). Subsequent requests are fast.

## Uninstallation

```bash
# 1. Deactivate virtual environment
deactivate

# 2. Remove virtual environment
rmdir /s /q venv  # Windows
rm -rf venv       # Linux/Mac

# 3. Remove vector store (optional)
rmdir /s /q vectorstore  # Windows
rm -rf vectorstore       # Linux/Mac
```

## Next Steps

After successful installation:

1. ✓ Server is running
2. ✓ Documents are ingested
3. ✓ Test all endpoints in Swagger UI: http://localhost:8000/docs
4. ✓ Build your frontend or integrate with existing app
5. ✓ Add more knowledge base files to ../data/

## Support

- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed error solutions
- See [README.md](README.md) for API documentation
- See [RAG_GUIDE.md](RAG_GUIDE.md) for RAG pipeline details
