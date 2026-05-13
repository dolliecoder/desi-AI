"""Verification script to test backend stability"""

import requests
import json
import sys
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)

def test_health():
    """Test health endpoint"""
    print_section("Testing /health")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_docs():
    """Test docs endpoint"""
    print_section("Testing /docs")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Content length: {len(response.text)} bytes")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_normalize():
    """Test normalization endpoint"""
    print_section("Testing /normalize")
    try:
        payload = {"query": "Bhai async await kab use karte hai?"}
        response = requests.post(
            f"{BASE_URL}/normalize",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Original: {data['original_query']}")
            print(f"Normalized: {data['normalized_query']}")
            print(f"Language: {data['detected_language']}")
            print(f"Style: {data['explanation_style']}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ingest():
    """Test ingestion endpoint"""
    print_section("Testing /rag/ingest")
    try:
        payload = {"force_reload": False}
        response = requests.post(
            f"{BASE_URL}/rag/ingest",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data['status']}")
            print(f"Documents processed: {data['documents_processed']}")
            print(f"Chunks created: {data['chunks_created']}")
            print(f"Message: {data['message']}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_search():
    """Test search endpoint"""
    print_section("Testing /rag/search")
    try:
        payload = {
            "query": "async await",
            "top_k": 3,
            "use_reranking": True
        }
        response = requests.post(
            f"{BASE_URL}/rag/search",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Query: {data['query']}")
            print(f"Total results: {data['total_results']}")
            for i, result in enumerate(data['results'], 1):
                print(f"\nResult {i}:")
                print(f"  Source: {result['source']}")
                print(f"  Score: {result['score']}")
                print(f"  Content: {result['content'][:100]}...")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Backend Stability Verification")
    print("="*60)
    print(f"Testing server at: {BASE_URL}")
    print("Make sure the server is running: python main.py")
    print()
    
    # Wait for user confirmation removed for automation
    
    # Run tests
    tests = [
        ("Health Check", test_health),
        ("Swagger Docs", test_docs),
        ("Normalization", test_normalize),
        ("Ingestion", test_ingest),
        ("Search", test_search),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
            time.sleep(1)  # Brief pause between tests
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print_section("Test Summary")
    passed_count = 0
    for name, passed in results:
        symbol = "✓" if passed else "❌"
        print(f"{symbol} {name}")
        if passed:
            passed_count += 1
    
    print(f"\nPassed: {passed_count}/{len(results)}")
    
    if passed_count == len(results):
        print("\n✓ All tests passed! Backend is stable and ready.")
        return 0
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
