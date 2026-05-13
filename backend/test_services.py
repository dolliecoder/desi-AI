"""Test script to verify all services are working"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_config():
    """Test configuration loading"""
    print("\n1. Testing Configuration...")
    try:
        from utils.config import settings
        print(f"   ✓ API Host: {settings.api_host}")
        print(f"   ✓ API Port: {settings.api_port}")
        print(f"   ✓ Embedding Model: {settings.embedding_model}")
        print(f"   ✓ ChromaDB Dir: {settings.chroma_persist_dir}")
        
        if settings.gemini_api_key:
            print(f"   ✓ Gemini API Key: {'*' * 20}{settings.gemini_api_key[-4:]}")
        else:
            print("   ❌ Gemini API Key: Not configured")
            return False
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

async def test_gemini():
    """Test Gemini service"""
    print("\n2. Testing Gemini Service...")
    try:
        from services.gemini_service import get_gemini_service
        service = get_gemini_service()
        
        # Test simple generation
        response = await service.generate_response(
            system_prompt="You are a helpful assistant.",
            user_prompt="Say 'Hello' in one word.",
            temperature=0.1
        )
        print(f"   ✓ Response: {response.strip()}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

async def test_embedding():
    """Test embedding service"""
    print("\n3. Testing Embedding Service (Lightweight Model)...")
    try:
        from services.embedding_service import get_embedding_service
        service = get_embedding_service()
        
        # Test embedding generation
        text = "Hello world"
        embedding = service.generate_embedding(text)
        print(f"   ✓ Embedding dimension: {len(embedding)}")
        print(f"   ✓ Sample values: {[round(v, 3) for v in embedding[:3]]}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

async def test_vectorstore():
    """Test vector store service"""
    print("\n4. Testing Vector Store Service...")
    try:
        from services.vectorstore_service import get_vectorstore_service
        service = get_vectorstore_service()
        
        count = service.get_count()
        print(f"   ✓ Documents in store: {count}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

async def test_normalization():
    """Test normalization service"""
    print("\n5. Testing Normalization Service...")
    try:
        from services.normalization_service import get_normalization_service
        service = get_normalization_service()
        
        # Test query normalization
        result = await service.normalize_query("Bhai async await kab use karte hai?")
        print(f"   ✓ Original: {result.original_query}")
        print(f"   ✓ Normalized: {result.normalized_query}")
        print(f"   ✓ Language: {result.detected_language}")
        print(f"   ✓ Style: {result.explanation_style}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

async def main():
    """Run all tests"""
    print("="*60)
    print("CodeSwitch AI - Service Tests")
    print("="*60)
    
    tests = [
        ("Configuration", test_config()),
        ("Gemini Service", test_gemini()),
        ("Embedding Service", test_embedding()),
        ("Vector Store", test_vectorstore()),
        ("Normalization", test_normalization()),
    ]
    
    results = []
    for name, test_coro in tests:
        try:
            result = await test_coro
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for name, passed in results:
        symbol = "✓" if passed else "❌"
        print(f"{symbol} {name}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n✓ All tests passed! Backend is ready.")
    else:
        print("\n❌ Some tests failed. Check errors above.")
        print("   See TROUBLESHOOTING.md for help.")
    
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
