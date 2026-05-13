# CodeSwitch AI - Frontend

Modern, minimal frontend for CodeSwitch AI multilingual coding assistant.

## Tech Stack

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **App Router** - Next.js routing

## Features

- 🌐 Single-page chat interface
- 🎨 Dark modern UI
- 📱 Responsive design
- ⚡ Real-time loading states
- 🔍 Shows normalized queries
- 📚 Displays retrieved sources
- 🎯 Example queries for quick start

## Setup

### Prerequisites

- Node.js 18+ installed
- Backend running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

The app will be available at http://localhost:3000

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

## Usage

1. **Start Backend First**
   ```bash
   cd ../backend
   python main.py
   ```

2. **Start Frontend**
   ```bash
   npm run dev
   ```

3. **Open Browser**
   - Navigate to http://localhost:3000
   - Ask coding questions in any language
   - View AI-powered answers with sources

## Example Queries

- "Bhai async await kab use karte hai?"
- "React hydration error kaise fix kare?"
- "Explain binary search for beginners"
- "DFS recursion mein stack overflow kyun hota hai?"

## API Integration

The frontend connects to the backend `/ask` endpoint:

```typescript
POST http://localhost:8000/ask
{
  "query": "Your coding question"
}
```

Response includes:
- Original query
- Normalized query
- AI-generated answer
- Retrieved context sources
- Detected language and style

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Main chat interface
│   └── globals.css      # Global styles
├── package.json         # Dependencies
├── tsconfig.json        # TypeScript config
├── tailwind.config.ts   # Tailwind config
└── next.config.js       # Next.js config
```

## Customization

### Change Backend URL

Edit `app/page.tsx`:
```typescript
const res = await fetch("http://your-backend-url/ask", {
  // ...
});
```

### Modify Styling

Edit `tailwind.config.ts` for theme changes or `app/globals.css` for custom styles.

## Troubleshooting

### "Failed to get response"

**Cause:** Backend not running or CORS issue

**Solution:**
1. Start backend: `cd ../backend && python main.py`
2. Check backend is on http://localhost:8000
3. Verify CORS is enabled in backend

### Port 3000 already in use

**Solution:**
```bash
# Use different port
PORT=3001 npm run dev
```

### Styling not working

**Solution:**
```bash
# Rebuild Tailwind
npm run dev
```

## Performance

- **Initial load:** <1s
- **Query response:** 2-4s (depends on backend)
- **Bundle size:** ~200KB (optimized)

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

MIT
