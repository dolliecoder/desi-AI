# Quick Start - CodeSwitch AI Frontend

## 🚀 5-Minute Setup

```bash
# 1. Install dependencies
npm install

# 2. Start development server
npm run dev
```

Open http://localhost:3000 in your browser!

## ✅ Prerequisites

Before starting the frontend, make sure:

1. **Backend is running**
   ```bash
   cd ../backend
   python main.py
   ```
   Backend should be on http://localhost:8000

2. **Documents are ingested**
   ```bash
   curl -X POST http://localhost:8000/rag/ingest \
     -H "Content-Type: application/json" \
     -d '{"force_reload": false}'
   ```

## 🎯 Test the App

1. Open http://localhost:3000
2. Try example queries:
   - "Bhai async await kab use karte hai?"
   - "React hydration error kaise fix kare?"
   - "Explain binary search for beginners"

3. You should see:
   - ✅ Original query
   - ✅ Normalized query
   - ✅ AI-generated answer
   - ✅ Retrieved sources
   - ✅ Language and style detection

## 🛠️ Common Commands

```bash
# Development
npm run dev          # Start dev server (http://localhost:3000)

# Production
npm run build        # Build for production
npm start            # Start production server

# Linting
npm run lint         # Run ESLint
```

## 🎨 Features

- **Dark Modern UI** - Professional developer tool aesthetic
- **Responsive** - Works on desktop, tablet, mobile
- **Real-time Loading** - Shows progress while processing
- **Example Queries** - Quick start with pre-filled questions
- **Source Display** - See which documents were used
- **Metadata** - Language and style detection visible

## 🔧 Troubleshooting

### Backend Connection Error

**Error:** "Failed to get response"

**Fix:**
```bash
# Check backend is running
curl http://localhost:8000/health

# If not, start it
cd ../backend
python main.py
```

### Port Already in Use

**Error:** "Port 3000 is already in use"

**Fix:**
```bash
# Use different port
PORT=3001 npm run dev
```

### Dependencies Not Installing

**Fix:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📱 Demo Flow

1. **Welcome Screen**
   - Shows app title and description
   - Displays example queries
   - Clean, minimal interface

2. **Ask Question**
   - Type or click example
   - Click "Ask" button
   - Shows loading state

3. **View Response**
   - See original and normalized query
   - Read AI-generated answer
   - Check retrieved sources
   - View language/style metadata

4. **Ask Another**
   - Click "Ask Another Question"
   - Returns to input screen

## 🎯 Perfect For

- ✅ Hackathon demos
- ✅ Local development
- ✅ Quick prototyping
- ✅ User testing

## 📚 Next Steps

1. ✅ Frontend running
2. ✅ Backend connected
3. ✅ Test with queries
4. 🎉 Demo ready!

---

**Need help?** Check the main README.md or backend documentation.
