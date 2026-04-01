#!/bin/bash

# Quick verification script for the refactored backend
# Run this to verify all changes are in place

echo "=================================================="
echo "NeuroPath AI - Backend Verification Script"
echo "=================================================="
echo ""

# Check Python version
echo "[1/8] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION"
else
    echo "❌ Python3 not found"
    exit 1
fi

# Check model files
echo ""
echo "[2/8] Checking model files..."
if [ -f "yolo_best.pt" ]; then
    echo "✅ yolo_best.pt found"
else
    echo "⚠️  yolo_best.pt not found (optional for mock mode)"
fi

if [ -f "resunet_best_optimized.pth" ]; then
    echo "✅ resunet_best_optimized.pth found"
else
    echo "⚠️  resunet_best_optimized.pth not found (optional for mock mode)"
fi

# Check core files exist
echo ""
echo "[3/8] Checking refactored files..."
if [ -f "models/model_manager.py" ]; then
    echo "✅ models/model_manager.py (NEW)"
else
    echo "❌ models/model_manager.py missing"
fi

if [ -f "models/detection_model.py" ]; then
    echo "✅ models/detection_model.py (REFACTORED)"
else
    echo "❌ models/detection_model.py missing"
fi

if [ -f "models/segmentation_model.py" ]; then
    echo "✅ models/segmentation_model.py (REFACTORED)"
else
    echo "❌ models/segmentation_model.py missing"
fi

# Check main.py
echo ""
echo "[4/8] Checking main.py..."
if grep -q "TumorDetector" main.py; then
    echo "✅ main.py uses TumorDetector"
else
    echo "❌ main.py doesn't import TumorDetector"
fi

if grep -q "SegmentationProcessor" main.py; then
    echo "✅ main.py uses SegmentationProcessor"
else
    echo "❌ main.py doesn't import SegmentationProcessor"
fi

# Check requirements.txt
echo ""
echo "[5/8] Checking requirements.txt..."
if grep -q "ultralytics" requirements.txt; then
    echo "✅ ultralytics in requirements.txt"
else
    echo "❌ ultralytics not in requirements.txt"
fi

# Check documentation
echo ""
echo "[6/8] Checking documentation..."
DOCS=("CHANGES_SUMMARY.md" "REFACTORING_GUIDE.md" "BEFORE_AFTER_COMPARISON.md" "IMPLEMENTATION_COMPLETE.md")
for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo "✅ $doc"
    else
        echo "⚠️  $doc missing"
    fi
done

# Test imports
echo ""
echo "[7/8] Testing Python imports..."
python3 -c "from models.model_manager import ModelManager; print('✅ ModelManager imports successfully')" 2>/dev/null || echo "❌ ModelManager import failed"
python3 -c "from models.detection_model import TumorDetector; print('✅ TumorDetector imports successfully')" 2>/dev/null || echo "❌ TumorDetector import failed"
python3 -c "from models.segmentation_model import SegmentationProcessor; print('✅ SegmentationProcessor imports successfully')" 2>/dev/null || echo "❌ SegmentationProcessor import failed"

# Summary
echo ""
echo "[8/8] Verification complete!"
echo ""
echo "=================================================="
echo "To get started:"
echo "1. pip install -r requirements.txt"
echo "2. python main.py"
echo "3. Open http://localhost:8000/docs"
echo "=================================================="
