"use client";

import { useState, useRef } from "react";

interface RetrievedContext {
  content: string;
  source: string;
  score: number;
}

interface AskResponse {
  query: string;
  normalized_query: string;
  answer: string;
  context_used: RetrievedContext[];
  detected_language: string;
  explanation_style: string;
}

interface PDFUploadResponse {
  filename: string;
  num_chunks: number;
  total_chars: number;
  message: string;
}

interface PDFAskResponse {
  query: string;
  answer: string;
  source: string;
}

export default function Home() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<AskResponse | null>(null);
  const [pdfResponse, setPdfResponse] = useState<PDFAskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadedPDF, setUploadedPDF] = useState<PDFUploadResponse | null>(null);
  const [uploadingPDF, setUploadingPDF] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handlePDFUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.pdf')) {
      setError("Please upload a PDF file");
      return;
    }

    setUploadingPDF(true);
    setError(null);
    setUploadedPDF(null);
    setPdfResponse(null);
    setResponse(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch("http://localhost:8000/pdf/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Error: ${res.status} ${res.statusText}`);
      }

      const data: PDFUploadResponse = await res.json();
      setUploadedPDF(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to upload PDF");
    } finally {
      setUploadingPDF(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResponse(null);
    setPdfResponse(null);

    try {
      // If PDF is uploaded, use PDF ask endpoint
      if (uploadedPDF) {
        const res = await fetch("http://localhost:8000/pdf/ask", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: query.trim() }),
        });

        if (!res.ok) {
          throw new Error(`Error: ${res.status} ${res.statusText}`);
        }

        const data: PDFAskResponse = await res.json();
        setPdfResponse(data);
      } else {
        // Otherwise use regular ask endpoint
        const res = await fetch("http://localhost:8000/ask", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: query.trim() }),
        });

        if (!res.ok) {
          throw new Error(`Error: ${res.status} ${res.statusText}`);
        }

        const data: AskResponse = await res.json();
        setResponse(data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to get response");
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (exampleQuery: string) => {
    setQuery(exampleQuery);
  };

  const handleNewPDF = () => {
    setUploadedPDF(null);
    setPdfResponse(null);
    setResponse(null);
    setQuery("");
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900">
      {/* Header */}
      <header className="border-b border-gray-800 bg-black/50 backdrop-blur-sm">
        <div className="max-w-5xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">CS</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">CodeSwitch AI</h1>
                <p className="text-sm text-gray-400">
                  {uploadedPDF ? "PDF Chat Mode" : "Multilingual Coding Assistant"}
                </p>
              </div>
            </div>
            
            {/* PDF Upload Button */}
            <div>
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handlePDFUpload}
                className="hidden"
                id="pdf-upload"
              />
              <label
                htmlFor="pdf-upload"
                className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg cursor-pointer transition-colors inline-block"
              >
                📄 Upload PDF
              </label>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-4 py-8">
        {/* PDF Upload Status */}
        {uploadingPDF && (
          <div className="bg-purple-900/20 border border-purple-800 rounded-xl p-6 mb-6">
            <div className="flex items-center gap-3">
              <div className="animate-spin rounded-full h-6 w-6 border-2 border-purple-500 border-t-transparent"></div>
              <p className="text-purple-300">Uploading and processing PDF...</p>
            </div>
          </div>
        )}

        {uploadedPDF && (
          <div className="bg-purple-900/20 border border-purple-800 rounded-xl p-6 mb-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-purple-300 mb-2">
                  ✓ PDF Uploaded
                </h3>
                <p className="text-gray-400">
                  <strong>{uploadedPDF.filename}</strong>
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  {uploadedPDF.num_chunks} chunks • {uploadedPDF.total_chars.toLocaleString()} characters
                </p>
              </div>
              <button
                onClick={handleNewPDF}
                className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-colors"
              >
                Upload New PDF
              </button>
            </div>
          </div>
        )}

        {/* Welcome Section */}
        {!response && !pdfResponse && !loading && !uploadedPDF && (
          <div className="text-center mb-12 mt-8">
            <h2 className="text-4xl font-bold text-white mb-4">
              Ask me anything about coding
            </h2>
            <p className="text-xl text-gray-400 mb-8">
              English, Hindi, or Hinglish - I understand them all
            </p>

            {/* Example Queries */}
            <div className="flex flex-wrap gap-3 justify-center mb-8">
              {[
                "Bhai async await kab use karte hai?",
                "React hydration error kaise fix kare?",
                "Explain binary search for beginners",
              ].map((example, idx) => (
                <button
                  key={idx}
                  onClick={() => handleExampleClick(example)}
                  className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg text-sm transition-colors border border-gray-700"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        )}

        {uploadedPDF && !response && !pdfResponse && !loading && (
          <div className="text-center mb-12 mt-8">
            <h2 className="text-3xl font-bold text-white mb-4">
              Ask questions about your PDF
            </h2>
            <p className="text-lg text-gray-400 mb-8">
              I'll answer based on the uploaded document
            </p>
          </div>
        )}

        {/* Query Input */}
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="relative">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={
                uploadedPDF
                  ? "Ask anything about your PDF..."
                  : "Ask your coding question in any language..."
              }
              className="w-full px-6 py-4 bg-gray-900 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows={3}
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="absolute bottom-4 right-4 px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
            >
              {loading ? "Thinking..." : "Ask"}
            </button>
          </div>
        </form>

        {/* Loading State */}
        {loading && (
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-8 text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-700 border-t-blue-500 mb-4"></div>
            <p className="text-gray-400">Processing your question...</p>
            <p className="text-sm text-gray-600 mt-2">
              {uploadedPDF ? "Analyzing PDF content..." : "Normalizing → Retrieving → Generating"}
            </p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-900/20 border border-red-800 rounded-xl p-6">
            <h3 className="text-red-400 font-semibold mb-2">Error</h3>
            <p className="text-red-300">{error}</p>
            <p className="text-sm text-gray-500 mt-2">
              Make sure the backend is running on http://localhost:8000
            </p>
          </div>
        )}

        {/* PDF Response */}
        {pdfResponse && (
          <div className="space-y-6">
            {/* Answer */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                Answer from PDF
              </h3>
              <div className="text-gray-300 leading-relaxed whitespace-pre-wrap markdown-content">
                {pdfResponse.answer}
              </div>
              <div className="mt-4 pt-4 border-t border-gray-800">
                <p className="text-sm text-gray-500">
                  Source: <span className="text-purple-400">{pdfResponse.source}</span>
                </p>
              </div>
            </div>

            {/* Ask Another Question */}
            <div className="text-center">
              <button
                onClick={() => {
                  setPdfResponse(null);
                  setQuery("");
                }}
                className="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-colors"
              >
                Ask Another Question
              </button>
            </div>
          </div>
        )}

        {/* Regular Response */}
        {response && (
          <div className="space-y-6">
            {/* Metadata */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <p className="text-xs text-gray-500 uppercase mb-1">
                    Original Query
                  </p>
                  <p className="text-gray-300">{response.query}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase mb-1">
                    Normalized
                  </p>
                  <p className="text-gray-300">{response.normalized_query}</p>
                </div>
                <div className="flex gap-4">
                  <div>
                    <p className="text-xs text-gray-500 uppercase mb-1">
                      Language
                    </p>
                    <span className="inline-block px-3 py-1 bg-blue-900/30 text-blue-400 rounded-full text-sm">
                      {response.detected_language}
                    </span>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 uppercase mb-1">
                      Style
                    </p>
                    <span className="inline-block px-3 py-1 bg-purple-900/30 text-purple-400 rounded-full text-sm">
                      {response.explanation_style}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Answer */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                Answer
              </h3>
              <div className="text-gray-300 leading-relaxed whitespace-pre-wrap markdown-content">
                {response.answer}
              </div>
            </div>

            {/* Retrieved Context */}
            {response.context_used && response.context_used.length > 0 && (
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4">
                  Retrieved Sources
                </h3>
                <div className="space-y-3">
                  {response.context_used.map((context, idx) => (
                    <div
                      key={idx}
                      className="bg-gray-800/50 border border-gray-700 rounded-lg p-4"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-blue-400">
                          {context.source}
                        </span>
                        <span className="text-xs text-gray-500">
                          Score: {(context.score * 100).toFixed(0)}%
                        </span>
                      </div>
                      <p className="text-sm text-gray-400 line-clamp-3">
                        {context.content}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Ask Another Question */}
            <div className="text-center">
              <button
                onClick={() => {
                  setResponse(null);
                  setQuery("");
                }}
                className="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-colors"
              >
                Ask Another Question
              </button>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 mt-16">
        <div className="max-w-5xl mx-auto px-4 py-6 text-center text-gray-500 text-sm">
          <p>
            Powered by Gemini AI • Built for Indian Developers • Open Source
          </p>
        </div>
      </footer>
    </div>
  );
}
