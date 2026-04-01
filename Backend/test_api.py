"""
Test script for NeuroPath AI API endpoints
Run this after starting the FastAPI server: python main.py
"""

import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("🏥 Testing Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_classification(image_path=None):
    """Test classification endpoint"""
    print("\n" + "="*60)
    print("🧠 Testing Classification")
    print("="*60)
    
    if image_path is None:
        print("⚠️  No image provided. Using test mode.")
        return
    
    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/classify", files=files)
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Classification Result: {result.get('result')}")
        print(f"Confidence: {result.get('confidence'):.2%}")
        print(f"Full Response: {json.dumps(result, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_segmentation(image_path=None):
    """Test segmentation endpoint"""
    print("\n" + "="*60)
    print("🎯 Testing Segmentation")
    print("="*60)
    
    if image_path is None:
        print("⚠️  No image provided. Using test mode.")
        return
    
    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/segment", files=files)
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Tumor Area: {result.get('tumor_area_percentage'):.2f}%")
        print(f"Mask Generated: {bool(result.get('mask_base64'))}")
        print(f"Response Keys: {list(result.keys())}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_detection(image_path=None):
    """Test detection endpoint"""
    print("\n" + "="*60)
    print("🔍 Testing Detection")
    print("="*60)
    
    if image_path is None:
        print("⚠️  No image provided. Using test mode.")
        return
    
    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/detect", files=files)
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Tumor Count: {result.get('tumor_count')}")
        print(f"Detections: {len(result.get('detections', []))} boxes")
        for i, det in enumerate(result.get('detections', []), 1):
            print(f"  Detection {i}: Confidence={det.get('confidence'):.2%}, BBox={det.get('bbox')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_analyze(image_path=None):
    """Test full analysis endpoint"""
    print("\n" + "="*60)
    print("📊 Testing Full Analysis (All 3 Models)")
    print("="*60)
    
    if image_path is None:
        print("⚠️  No image provided. Using test mode.")
        return
    
    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/analyze", files=files)
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        print("\n📋 Classification Results:")
        print(f"  Result: {result['classification'].get('result')}")
        print(f"  Confidence: {result['classification'].get('confidence'):.2%}")
        
        print("\n🎯 Segmentation Results:")
        print(f"  Tumor Area: {result['segmentation'].get('tumor_area_percentage'):.2f}%")
        
        print("\n🔍 Detection Results:")
        print(f"  Tumor Count: {result['detection'].get('tumor_count')}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🧠 NeuroPath AI - API Test Suite 🧠".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    print(f"\n🔗 API URL: {BASE_URL}")
    print("⏳ Starting tests...\n")
    
    # Test health check
    health_ok = test_health()
    
    if not health_ok:
        print("\n❌ Health check failed! Make sure the server is running:")
        print("   python main.py")
        print("\n   or use: ./run.sh (macOS/Linux) or run.bat (Windows)")
        return
    
    # Find a test image (optional)
    image_path = None
    possible_paths = [
        Path("test_image.jpg"),
        Path("sample.png"),
        Path("brain_scan.jpg"),
    ]
    
    for path in possible_paths:
        if path.exists():
            image_path = str(path)
            print(f"\n📂 Found test image: {image_path}")
            break
    
    # Run tests
    results = {
        "Health Check": health_ok,
        "Classification": test_classification(image_path),
        "Segmentation": test_segmentation(image_path),
        "Detection": test_detection(image_path),
        "Full Analysis": test_analyze(image_path),
    }
    
    # Print summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASSED" if passed_test else "⏭️  SKIPPED" if passed_test is None else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests {'✅ PASSED' if passed == total else '⚠️  SOME SKIPPED'}")
    
    if image_path is None:
        print("\n💡 Tip: Add a test image (jpg/png) to run full endpoint tests")
        print("   Place it in the Backend folder and name it: test_image.jpg")
    
    print("\n📚 For API documentation, open: http://localhost:8000/docs\n")


if __name__ == "__main__":
    main()
