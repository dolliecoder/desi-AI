Desi-AI 🇮🇳🤖

An AI-powered multilingual assistant that understands English, Hindi, and Hinglish, supports document upload, and answers questions using RAG (Retrieval-Augmented Generation).

Built to make AI interaction more natural for Indian users by allowing mixed-language conversations and document-based querying.

🚀 Features
🌐 Supports English, Hindi, and Hinglish
📄 Upload PDFs and documents
🧠 AI understands uploaded content using RAG
💬 Ask questions directly from your documents
🔍 Semantic search using embeddings + vector database
⚡ Fast and interactive AI responses
🤖 Context-aware conversational assistant
🛠️ Tech Stack
Frontend: React / Next.js
Backend: FastAPI
LLM: OpenRouter / Ollama
RAG Pipeline: Embeddings + Vector Search
Database: Vector Database (FAISS / ChromaDB / pgvector)
Document Processing: PDF & DOC parsing
📌 How It Works
User uploads a PDF or document
The system extracts and chunks the text
Embeddings are generated for the chunks
Data is stored in a vector database
When a user asks a question:
Relevant chunks are retrieved
Context is sent to the LLM
AI generates an accurate answer
🖼️ Example Queries
“Summarize this PDF”
“Is document me kya likha hai?”
“Explain chapter 2 in simple Hindi”
“What are the key points from this document?”
“Yeh agreement kis bare me hai?”
⚙️ Installation
# Clone the repository
git clone https://github.com/dolliecoder/desi-AI.git

# Move into the project
cd desi-AI

# Install dependencies
npm install

# Start frontend
npm run dev

Backend setup:

pip install -r requirements.txt

uvicorn app:app --reload
📂 Supported File Types
PDF
DOCX
TXT
🎯 Future Improvements
Voice input support
Indian language speech output
Better multilingual embeddings
Chat history & memory
Deployment support
🤝 Contributing

Contributions are welcome!
Feel free to open issues or submit pull requests.

📜 License

This project is licensed under the MIT License.

👩‍💻 Author

Made with ❤️ by dolliecoder
