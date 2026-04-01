from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
import cv2
import numpy as np
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from models.classification_model import ClassificationModel
from models.detection_model import TumorDetector
from models.segmentation_model import SegmentationProcessor
from utils.image_processor import ImageProcessor

# Initialize FastAPI app
app = FastAPI(
    title="NeuroPath AI - Medical Imaging Analysis API",
    description="API for brain tumor classification, segmentation, and detection",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
print("=" * 60)
print("Loading NeuroPath AI Models...")
print("=" * 60)

try:
    print("[1/3] Loading Classification Model...")
    classification_model = ClassificationModel()
    print("✓ Classification model loaded")
except Exception as e:
    print(f"⚠ Warning: Classification model failed: {e}")
    classification_model = None

try:
    print("[2/3] Loading Detection Model (YOLO)...")
    detection_model = TumorDetector()
    print(f"✓ Detection model loaded: {'YOLO' if detection_model.is_loaded() else 'Mock'}")
except Exception as e:
    print(f"⚠ Warning: Detection model failed: {e}")
    detection_model = None

try:
    print("[3/3] Loading Segmentation Model (ResUNet)...")
    segmentation_model = SegmentationProcessor()
    print(f"✓ Segmentation model loaded: {'ResUNet' if segmentation_model.is_loaded() else 'Fallback'}")
except Exception as e:
    print(f"⚠ Warning: Segmentation model failed: {e}")
    segmentation_model = None

image_processor = ImageProcessor()
print("=" * 60)
print("✓ All models initialized successfully!")
print("=" * 60)


# ============ HEALTH CHECK ============
@app.get("/health")
async def health_check():
    """Check if all models are loaded and API is running"""
    return {
        "status": "healthy",
        "models": {
            "classification": "loaded",
            "segmentation": "loaded",
            "detection": "loaded"
        }
    }


# ============ CLASSIFICATION ROUTE ============
@app.post("/classify")
async def classify_tumor(file: UploadFile = File(...)):
    """
    Classify brain tumor from MRI/CT scan image
    - Returns: Classification result and confidence score
    """
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        if classification_model is None:
            raise HTTPException(status_code=503, detail="Classification model not loaded")
        
        # Read and process image
        image_array = await image_processor.read_uploaded_file(file)
        
        # Run classification
        result = classification_model.predict(image_array)
        
        return JSONResponse({
            "status": "success",
            "task": "classification",
            "result": result["classification"],
            "confidence": result["confidence"],
            "filename": file.filename
        })
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Classification error: {e}")
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")


# ============ SEGMENTATION ROUTE ============
@app.post("/segment")
async def segment_tumor(file: UploadFile = File(...)):
    """
    Segment brain tumor region from MRI/CT scan image
    - Returns: Segmentation mask and processed image with highlighted tumor area
    """
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        if segmentation_model is None:
            raise HTTPException(status_code=503, detail="Segmentation model not loaded")
        
        if detection_model is None:
            raise HTTPException(status_code=503, detail="Detection model not loaded - needed for ROI extraction")
        
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image_array = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image_array is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Step 1: Run detection to get ROI
        detection_result = detection_model.predict(image_array, conf=0.5, iou=0.5, padding=10)
        detections = detection_result.get('detections', [])
        
        if not detections:
            raise HTTPException(status_code=400, detail="No tumors detected for segmentation")
        
        # Step 2: Segment each detected ROI
        segmentation_results = []
        
        for idx, detection in enumerate(detections):
            try:
                roi = detection.get('roi')
                bbox = detection.get('bbox')
                
                if roi is None or bbox is None:
                    continue
                
                # Run segmentation on ROI with full image context for overlay
                seg_result = segmentation_model.predict(roi, original_image=image_array, bbox=bbox)
                
                # Store results with bbox info for overlay reconstruction
                segmentation_results.append({
                    'detection_id': idx,
                    'mask_base64': seg_result['mask_base64'],
                    'segmented_image_base64': seg_result['segmented_image_base64'],
                    'tumor_area_percentage': seg_result['tumor_area_percentage'],
                    'statistics': seg_result['statistics'],
                    'bbox': bbox
                })
            except Exception as e:
                print(f"⚠ Error segmenting ROI {idx}: {e}")
                continue
        
        if not segmentation_results:
            raise HTTPException(status_code=500, detail="Failed to segment detected regions")
        
        # Return first segmentation result (or all if multiple detections)
        primary_result = segmentation_results[0]
        
        return JSONResponse({
            "status": "success",
            "task": "segmentation",
            "mask": primary_result["mask_base64"],
            "segmented_image": primary_result["segmented_image_base64"],
            "tumor_area_percentage": primary_result["tumor_area_percentage"],
            "statistics": primary_result["statistics"],
            "total_detections": len(segmentation_results),
            "filename": file.filename
        })
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Segmentation error: {e}")
        raise HTTPException(status_code=500, detail=f"Segmentation error: {str(e)}")


# ============ DETECTION ROUTE ============
@app.post("/detect")
async def detect_tumor(file: UploadFile = File(...)):
    """
    Detect and highlight tumor location in brain scan image
    - Returns: Image with bounding boxes and tumor location data
    """
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        if detection_model is None:
            raise HTTPException(status_code=503, detail="Detection model not loaded")
        
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image_array = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image_array is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Run detection
        result = detection_model.predict(image_array, conf=0.5, iou=0.5, padding=10)
        
        # Format detections for JSON response (convert to serializable format)
        detections_json = []
        if result['detections']:
            for det in result['detections']:
                detections_json.append({
                    'id': det.get('id', 0),
                    'bbox': [int(x) for x in det['bbox']],
                    'confidence': float(det['confidence']),
                    'class': det.get('class', 0),
                    'area': int(det['area']),
                    'width': int(det['width']),
                    'height': int(det['height']),
                    'center': [
                        int((det['bbox'][0] + det['bbox'][2]) / 2),
                        int((det['bbox'][1] + det['bbox'][3]) / 2)
                    ]
                })
        
        return JSONResponse({
            "status": "success",
            "task": "detection",
            "detected_image": result["detected_image_base64"],
            "detections": detections_json,
            "tumor_count": result["tumor_count"],
            "message": result.get("message", ""),
            "filename": file.filename
        })
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Detection error: {e}")
        raise HTTPException(status_code=500, detail=f"Detection error: {str(e)}")


# ============ COMBINED ANALYSIS ROUTE ============
@app.post("/analyze")
async def analyze_full_pipeline(file: UploadFile = File(...)):
    """
    Perform complete analysis: Classification, Segmentation, and Detection
    - Returns: Results from all three models in a single response
    """
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Check if all models are loaded
        if classification_model is None:
            raise HTTPException(status_code=503, detail="Classification model not loaded")
        if segmentation_model is None:
            raise HTTPException(status_code=503, detail="Segmentation model not loaded")
        if detection_model is None:
            raise HTTPException(status_code=503, detail="Detection model not loaded")
        
        # Read and process image once
        image_array = await image_processor.read_uploaded_file(file)
        
        # Run classification
        classification_result = classification_model.predict(image_array)
        
        # Run detection
        detection_result = detection_model.predict(image_array, conf=0.5, iou=0.5, padding=10)
        detections = detection_result.get('detections', [])
        
        # Run segmentation on detected ROI (not full image)
        segmentation_result = None
        if detections:
            try:
                # Extract ROI from first detection
                roi = detections[0].get('roi')
                bbox = detections[0].get('bbox')
                if roi is not None and bbox is not None:
                    # Pass original image and bbox for full-image overlay
                    segmentation_result = segmentation_model.predict(roi, original_image=image_array, bbox=bbox)
            except Exception as e:
                print(f"⚠ Warning: Segmentation on detected ROI failed: {e}")
                segmentation_result = None
        
        # If no detections or segmentation failed, use full image as fallback
        if segmentation_result is None:
            try:
                segmentation_result = segmentation_model.predict(image_array)
            except Exception as e:
                print(f"⚠ Warning: Segmentation fallback failed: {e}")
                segmentation_result = {
                    "mask_base64": "",
                    "segmented_image_base64": "",
                    "tumor_area_percentage": 0
                }
        
        # Format detections for JSON serialization (remove numpy arrays)
        detections_json = []
        if detection_result['detections']:
            for det in detection_result['detections']:
                detections_json.append({
                    'id': det.get('id', 0),
                    'bbox': [int(x) for x in det['bbox']],
                    'confidence': float(det['confidence']),
                    'class': det.get('class', 0),
                    'area': int(det['area']),
                    'width': int(det['width']),
                    'height': int(det['height']),
                    'center': [
                        int((det['bbox'][0] + det['bbox'][2]) / 2),
                        int((det['bbox'][1] + det['bbox'][3]) / 2)
                    ]
                })
        
        return JSONResponse({
            "status": "success",
            "task": "full_analysis",
            "filename": file.filename,
            "classification": {
                "result": classification_result["classification"],
                "confidence": classification_result["confidence"]
            },
            "segmentation": {
                "mask": segmentation_result.get("mask_base64", ""),
                "segmented_image": segmentation_result.get("segmented_image_base64", ""),
                "tumor_area_percentage": segmentation_result.get("tumor_area_percentage", 0)
            },
            "detection": {
                "detected_image": detection_result["detected_image_base64"],
                "detections": detections_json,
                "tumor_count": detection_result["tumor_count"]
            }
        })
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


# ============ ROOT ROUTE ============
@app.get("/")
async def root():
    """Welcome message and API documentation"""
    return {
        "message": "Welcome to NeuroPath AI API",
        "version": "1.0.0",
        "documentation": "/docs",
        "available_endpoints": {
            "POST /classify": "Brain tumor classification",
            "POST /segment": "Tumor segmentation",
            "POST /detect": "Tumor detection and highlighting",
            "POST /analyze": "Complete pipeline (all three tasks)",
            "GET /health": "Health check"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
