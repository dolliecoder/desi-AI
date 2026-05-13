# PDF Chat Feature - CodeSwitch AI

## Kya Hai Yeh Feature?

Ab aap koi bhi PDF upload kar sakte ho aur uske baare mein AI se sawal puch sakte ho! 

### Features:
1. **PDF Upload** - Koi bhi PDF document upload karo
2. **Text Extraction** - AI automatically PDF se text extract karega
3. **Smart Search** - Aapke question ke relevant sections dhundega
4. **AI Answers** - Gemini AI se answer milega based on PDF content
5. **Multilingual** - Hindi, English, Hinglish - kisi bhi language mein puch sakte ho!

## Kaise Use Karein?

### Step 1: Backend Start Karo

```bash
cd backend

# Virtual environment activate karo
venv\Scripts\activate

# Dependencies install karo (pehli baar)
pip install -r requirements.txt

# Server start karo
python main.py
```

Backend chalega: http://localhost:8000

### Step 2: Frontend Start Karo

```bash
cd frontend

# Dependencies install karo (pehli baar)
npm install

# Development server start karo
npm run dev
```

Frontend chalega: http://localhost:3000

### Step 3: PDF Upload Karo

1. Browser mein http://localhost:3000 kholo
2. Top right corner mein "📄 Upload PDF" button pe click karo
3. Apni PDF file select karo
4. Wait karo jab tak process ho jaye

### Step 4: Questions Pucho!

PDF upload hone ke baad:
- Input box mein apna question type karo
- Hindi, English, ya Hinglish - kuch bhi use kar sakte ho
- "Ask" button pe click karo
- AI answer dega based on your PDF!

## Example Questions

### English:
- "What is this document about?"
- "Summarize the main points"
- "Explain the key concepts"

### Hindi:
- "Is document mein kya hai?"
- "Main points batao"
- "Important cheezein kya hain?"

### Hinglish:
- "Yeh document kis baare mein hai?"
- "Main topics kya hain?"
- "Summary do iska"

## API Endpoints

### 1. Upload PDF
```bash
POST /pdf/upload
Content-Type: multipart/form-data

# Upload file
curl -X POST http://localhost:8000/pdf/upload \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "filename": "document.pdf",
  "num_chunks": 5,
  "total_chars": 4523,
  "message": "PDF uploaded and processed successfully"
}
```

### 2. Ask Question
```bash
POST /pdf/ask
Content-Type: application/json

{
  "query": "Is document ke baare mein batao"
}
```

**Response:**
```json
{
  "query": "Is document ke baare mein batao",
  "answer": "Yeh document...",
  "source": "document.pdf"
}
```

### 3. Check Status
```bash
GET /pdf/status
```

**Response:**
```json
{
  "uploaded": true,
  "filename": "document.pdf",
  "num_chunks": 5
}
```

## Technical Details

### Backend Architecture

```
PDF Upload
    ↓
Text Extraction (PyPDF2)
    ↓
Chunking (1000 chars per chunk)
    ↓
In-Memory Storage
    ↓
Keyword-Based Search
    ↓
Gemini AI Answer Generation
```

### Files Added

**Backend:**
- `services/pdf_service.py` - PDF processing
- `services/pdf_document_store.py` - Document storage
- `routes/pdf.py` - API endpoints
- `models/pdf.py` - Request/response models

**Frontend:**
- Updated `app/page.tsx` - PDF upload UI

### Dependencies Added

```
PyPDF2==3.0.1           # PDF text extraction
python-multipart==0.0.6  # File upload support
```

## Troubleshooting

### "Only PDF files are allowed"
**Solution:** Sirf .pdf files upload kar sakte ho

### "No PDF uploaded"
**Solution:** Pehle PDF upload karo, phir question pucho

### "Failed to extract text from PDF"
**Solution:** 
- Check if PDF is not password protected
- Check if PDF has actual text (not just images)
- Try a different PDF

### Backend not starting
**Solution:**
```bash
# Dependencies install karo
pip install -r requirements.txt

# Check if port 8000 is free
# Start server
python main.py
```

### Frontend not connecting
**Solution:**
- Check backend is running on http://localhost:8000
- Check frontend is running on http://localhost:3000
- Check CORS is enabled (already configured)

## Features

### ✅ What Works

- PDF upload and text extraction
- Multi-page PDF support
- Keyword-based search in PDF
- AI-powered answers using Gemini
- Multilingual support (Hindi/English/Hinglish)
- Clean, modern UI
- Real-time processing status

### 🚀 Future Enhancements (Optional)

- Multiple PDF support
- PDF history
- Download chat history
- Image extraction from PDF
- Table extraction
- OCR for scanned PDFs

## Performance

- **PDF Upload:** ~2-5 seconds (depends on size)
- **Text Extraction:** ~1-2 seconds per page
- **Question Answering:** ~2-4 seconds
- **Max PDF Size:** No hard limit (but keep under 10MB for best performance)

## Example Workflow

```
1. User uploads "research_paper.pdf"
   → Backend extracts text
   → Creates 10 chunks
   → Stores in memory

2. User asks: "Main findings kya hain?"
   → Backend searches relevant chunks
   → Finds 3 most relevant sections
   → Sends to Gemini AI
   → Returns answer in Hindi

3. User asks: "Explain methodology"
   → Backend searches again
   → Finds methodology sections
   → Gemini generates explanation
   → Returns answer
```

## Summary

Ab aap:
- ✅ Koi bhi PDF upload kar sakte ho
- ✅ AI se questions puch sakte ho
- ✅ Hindi/English/Hinglish mein answer mil jayega
- ✅ Fast aur reliable hai
- ✅ Easy to use UI hai

**Perfect for:**
- Research papers
- Documentation
- Study materials
- Reports
- Any PDF document!

---

**Happy Chatting with your PDFs! 🚀📄**
