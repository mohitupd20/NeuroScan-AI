# NeuroPath AI - Medical Imaging Analysis Backend

FastAPI server for brain tumor analysis with three AI models:

- **Classification**: Identify tumor type (Glioma, Meningioma, Pituitary, No Tumor)
- **Segmentation**: Highlight tumor region (ResUNet model)
- **Detection**: Locate and mark tumor boundaries (YOLO model)

## 📋 Project Structure

```
Backend/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── .env                            # Environment configuration
├── best_brain_tumor_model.pth       # Classification model
├── resunet_best_optimized.pth       # Segmentation model
├── yolo_best.pt                     # Detection model
├── models/
│   ├── __init__.py
│   ├── classification_model.py      # Tumor classification wrapper
│   ├── segmentation_model.py        # Tumor segmentation wrapper
│   └── detection_model.py           # Tumor detection wrapper
└── utils/
    ├── __init__.py
    └── image_processor.py           # Image preprocessing utilities
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
cd Backend
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python main.py
```

Or using Uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

## 📚 API Endpoints

### 1. Health Check

```
GET /health
```

Check if all models are loaded and API is running.

**Response:**

```json
{
  "status": "healthy",
  "models": {
    "classification": "loaded",
    "segmentation": "loaded",
    "detection": "loaded"
  }
}
```

### 2. Classification

```
POST /classify
```

Classify brain tumor type from MRI/CT scan.

**Request:**

- File upload (multipart/form-data): Medical image (JPG, PNG, DICOM)

**Response:**

```json
{
  "status": "success",
  "task": "classification",
  "result": "Glioma",
  "confidence": 0.95,
  "all_probabilities": {
    "No Tumor": 0.02,
    "Glioma": 0.95,
    "Meningioma": 0.02,
    "Pituitary": 0.01
  },
  "filename": "scan.jpg"
}
```

### 3. Segmentation

```
POST /segment
```

Segment tumor region and highlight affected area.

**Request:**

- File upload (multipart/form-data): Medical image

**Response:**

```json
{
  "status": "success",
  "task": "segmentation",
  "mask": "iVBORw0KGgoAAAANSUhEUgAAAAEA...",
  "segmented_image": "iVBORw0KGgoAAAANSUhEUgAAAAEA...",
  "tumor_area_percentage": 15.5,
  "filename": "scan.jpg"
}
```

### 4. Detection

```
POST /detect
```

Detect and highlight tumor location with bounding boxes.

**Request:**

- File upload (multipart/form-data): Medical image

**Response:**

```json
{
  "status": "success",
  "task": "detection",
  "detected_image": "iVBORw0KGgoAAAANSUhEUgAAAAEA...",
  "detections": [
    {
      "bbox": [120, 150, 250, 280],
      "confidence": 0.92,
      "class": "tumor",
      "class_id": 0
    }
  ],
  "tumor_count": 1,
  "filename": "scan.jpg"
}
```

### 5. Complete Pipeline Analysis

```
POST /analyze
```

Perform all three analyses (classification, segmentation, detection) in one request.

**Request:**

- File upload (multipart/form-data): Medical image

**Response:**

```json
{
  "status": "success",
  "task": "full_analysis",
  "filename": "scan.jpg",
  "classification": {
    "result": "Glioma",
    "confidence": 0.95
  },
  "segmentation": {
    "mask": "base64_encoded_mask",
    "segmented_image": "base64_encoded_image",
    "tumor_area_percentage": 15.5
  },
  "detection": {
    "detected_image": "base64_encoded_image",
    "detections": [...],
    "tumor_count": 1
  }
}
```

## 🎯 Usage Example

### Using cURL

```bash
# Classification
curl -X POST "http://localhost:8000/classify" \
  -F "file=@brain_scan.jpg"

# Segmentation
curl -X POST "http://localhost:8000/segment" \
  -F "file=@brain_scan.jpg"

# Detection
curl -X POST "http://localhost:8000/detect" \
  -F "file=@brain_scan.jpg"

# Full Analysis
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@brain_scan.jpg"
```

### Using Python

```python
import requests

url = "http://localhost:8000/classify"
files = {"file": open("brain_scan.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

### Using Frontend (React)

```javascript
const formData = new FormData();
formData.append("file", imageFile);

const response = await fetch("http://localhost:8000/classify", {
  method: "POST",
  body: formData,
});

const result = await response.json();
```

## 📖 API Documentation

Interactive API documentation is available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

Edit `.env` file to customize:

```env
HOST=0.0.0.0         # Server host
PORT=8000            # Server port
DEBUG=True           # Debug mode
ALLOWED_ORIGINS=...  # CORS allowed origins
```

## 📦 Model Files

The following pre-trained models should be placed in the Backend folder:

1. **best_brain_tumor_model.pth** - Classification model (PyTorch)
2. **resunet_best_optimized.pth** - Segmentation model (PyTorch)
3. **yolo_best.pt** - Detection model (YOLO format)

## ✅ Features

- ✅ Multiple medical imaging format support (JPG, PNG, DCIM)
- ✅ Three specialized AI models for different analysis tasks
- ✅ Base64 encoded image responses for easier frontend integration
- ✅ Comprehensive error handling and validation
- ✅ CORS enabled for frontend communication
- ✅ Interactive API documentation (Swagger/ReDoc)
- ✅ GPU acceleration support (CUDA if available)
- ✅ Async/await support for non-blocking requests

## 🐛 Troubleshooting

### Models not loading

- Check model files exist in Backend folder
- Verify file names match configuration
- Check file permissions

### Port already in use

```bash
# Use different port
python main.py --port 8001
# Or
lsof -i :8000  # Find process using port
kill -9 <PID>   # Kill the process
```

### CORS errors

- Update `ALLOWED_ORIGINS` in `.env`
- Ensure frontend URL matches CORS settings

### Model inference errors

- Check image format and size
- Ensure model weights are compatible
- Check GPU/CUDA availability if using GPU

## 📞 Support

For issues or questions, please check:

1. API documentation: http://localhost:8000/docs
2. Error messages in server logs
3. Model compatibility and file integrity

---

**NeuroPath AI** - Advanced Medical Imaging Analysis Platform
