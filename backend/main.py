from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import health, normalization, rag, ask, pdf
from utils.config import settings
import sys
import traceback

# Initialize FastAPI app
app = FastAPI(
    title="CodeSwitch AI",
    description="Multilingual coding assistant for Indian developers",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
try:
    app.include_router(health.router)
    app.include_router(normalization.router)
    app.include_router(rag.router)
    app.include_router(ask.router)
    app.include_router(pdf.router)
    print("✓ All routes registered successfully")
except Exception as e:
    print(f"❌ Error registering routes: {e}")
    traceback.print_exc()
    sys.exit(1)

@app.on_event("startup")
async def startup_event():
    """Validate environment and services on startup"""
    print("\n" + "="*60)
    print("CodeSwitch AI - Backend Startup (Lightweight Demo)")
    print("="*60)
    
    try:
        # Check OpenAI API key
        if not settings.openai_api_key:
            print("❌ ERROR: OPENAI_API_KEY not configured")
            print("   Please set OPENAI_API_KEY in .env file")
            sys.exit(1)
        if not settings.openai_base_url:
            print("❌ ERROR: OPENAI_BASE_URL not configured")
            print("   Please set OPENAI_BASE_URL in .env file")
            sys.exit(1)
        if not settings.openai_model:
            print("❌ ERROR: OPENAI_MODEL not configured")
            print("   Please set OPENAI_MODEL in .env file")
            sys.exit(1)
        print("✓ OpenAI API configured")
        print(f"   Model: {settings.openai_model}")
        print(f"   Base URL: {settings.openai_base_url}")
        
        print("\n" + "="*60)
        print("Performance Optimizations:")
        print("  - Keyword-based retrieval (no ML models)")
        print("  - In-memory document storage")
        print("  - Expected startup: <5 seconds")
        print("="*60)
        print("\nServices will initialize on first use:")
        print("  - Gemini API (on first /normalize request)")
        print("  - Keyword retrieval (on first /rag/ingest or /rag/search)")
        print("="*60)
        print(f"\nServer starting on http://{settings.api_host}:{settings.api_port}")
        print(f"Swagger docs: http://localhost:{settings.api_port}/docs")
        print(f"ReDoc: http://localhost:{settings.api_port}/redoc")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        traceback.print_exc()
        sys.exit(1)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("\n" + "="*60)
    print("CodeSwitch AI - Shutting down")
    print("="*60 + "\n")

if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(
            "main:app",
            host=settings.api_host,
            port=settings.api_port,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        traceback.print_exc()
        sys.exit(1)
