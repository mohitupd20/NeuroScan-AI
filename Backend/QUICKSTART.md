# NeuroPath AI - Backend Quick Reference

## 🎯 Quick Start

### 1. Installation (First Time Only)

```bash
cd Backend
pip install -r requirements.txt
```

### 2. Start Server

```bash
# Option 1: Direct Python
python main.py

# Option 2: Using Uvicorn with hot-reload
uvicorn main:app --reload --port 8000

# Option 3: Using startup scripts
./run.sh          # macOS/Linux
run.bat           # Windows
```

### 3. Test API

```bash
# Health check
python test_api.py

# Or with curl
curl http://localhost:8000/health
```

---

## 📡 API Endpoints Quick Reference

### Classification

```
POST /classify
- Identifies tumor type (Glioma, Meningioma, Pituitary, No Tumor)
- Returns confidence score and probabilities for each class
```

### Segmentation

```
POST /segment
- Highlights tumor region in the image
- Returns mask and tumor area percentage
```

### Detection

```
POST /detect
- Locates tumor with bounding boxes
- Returns detected image with highlights
```

### Complete Analysis

```
POST /analyze
- Runs all three models in one request
- Returns combined results
```

---

## 🏗️ Project Structure

| File/Folder                  | Purpose                         |
| ---------------------------- | ------------------------------- |
| `main.py`                    | FastAPI application entry point |
| `config.py`                  | Configuration and settings      |
| `models/`                    | Model wrappers and inference    |
| └─ `classification_model.py` | Brain tumor classifier          |
| └─ `segmentation_model.py`   | Tumor segmentation (ResUNet)    |
| └─ `detection_model.py`      | Tumor detection (YOLO)          |
| `utils/`                     | Utility functions               |
| └─ `image_processor.py`      | Image preprocessing             |
| `.env`                       | Environment variables           |
| `requirements.txt`           | Python dependencies             |
| `test_api.py`                | API testing script              |

---

## 🔧 Configuration

Edit `.env` to customize:

```env
HOST=0.0.0.0              # Server address
PORT=8000                 # Server port
DEBUG=True                # Debug mode
ALLOWED_ORIGINS=...       # CORS origins
USE_CUDA=True             # Enable GPU (if available)
```

---

## 📦 Model Files Required

Place these in the `Backend/` directory:

1. `best_brain_tumor_model.pth` (Classification)
2. `resunet_best_optimized.pth` (Segmentation)
3. `yolo_best.pt` (Detection)

---

## 🎨 Frontend Integration

### React Example

```javascript
const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://localhost:8000/classify", {
    method: "POST",
    body: formData,
  });

  return await response.json();
};
```

### cURL Example

```bash
curl -X POST "http://localhost:8000/classify" \
  -F "file=@image.jpg"
```

---

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🐛 Troubleshooting

| Issue            | Solution                                    |
| ---------------- | ------------------------------------------- |
| Port 8000 in use | `python main.py --port 8001`                |
| Models not found | Check `.env` and verify file paths          |
| CORS errors      | Update `ALLOWED_ORIGINS` in `.env`          |
| Import errors    | Run `pip install -r requirements.txt` again |
| GPU not detected | Install CUDA or set `USE_CUDA=False`        |

---

## 🚀 Performance Tips

- Use GPU if available (CUDA compatible NVIDIA GPU)
- For batch processing, use `/analyze` endpoint
- Images are automatically resized for efficiency
- Server caches models in memory for fast inference

---

## 📞 Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run with specific port
uvicorn main:app --port 8001

# Run with multiple workers
uvicorn main:app --workers 4

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Check Python version
python --version

# View installed packages
pip list

# Clear cache
rm -rf __pycache__ .pytest_cache
```

---

## 🌐 Endpoints Response Format

All endpoints return JSON:

```json
{
  "status": "success",
  "task": "classification",
  "result": "Glioma",
  "confidence": 0.95,
  "filename": "scan.jpg"
}
```

---

## ✅ Server Health Indicators

✅ Health endpoint working  
✅ Models loaded successfully  
✅ CORS enabled for frontend  
✅ GPU support available (if installed)

Check status: `curl http://localhost:8000/health`

---

**Last Updated**: March 27, 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✨
