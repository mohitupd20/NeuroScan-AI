import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the backend directory
BACKEND_DIR = Path(__file__).parent

class Settings:
    """Application settings"""
    
    # Server Configuration
    APP_NAME = "NeuroPath AI"
    APP_VERSION = "1.0.0"
    DESCRIPTION = "Medical Imaging Analysis API for Brain Tumor Detection"
    
    # FastAPI Settings
    DEBUG = os.getenv("DEBUG", "True") == "True"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # CORS Settings
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5180",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5180",
    ]
    
    # Model Paths
    CLASSIFICATION_MODEL_PATH = BACKEND_DIR / os.getenv("CLASSIFICATION_MODEL", "best_brain_tumor_model.pth")
    SEGMENTATION_MODEL_PATH = BACKEND_DIR / os.getenv("SEGMENTATION_MODEL", "resunet_best_optimized.pth")
    DETECTION_MODEL_PATH = BACKEND_DIR / os.getenv("DETECTION_MODEL", "yolo_best.pt")
    
    # File Upload Settings
    MAX_UPLOAD_SIZE = 256 * 1024 * 1024  # 256 MB
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".dcm", ".nii", ".nii.gz"}
    
    # Model Loading
    USE_CUDA = os.getenv("USE_CUDA", "True") == "True"
    DEVICE = "cuda" if USE_CUDA else "cpu"
    
    @classmethod
    def check_models_exist(cls):
        """Check if all model files exist"""
        models = {
            "Classification": cls.CLASSIFICATION_MODEL_PATH,
            "Segmentation": cls.SEGMENTATION_MODEL_PATH,
            "Detection": cls.DETECTION_MODEL_PATH,
        }
        
        missing = []
        for name, path in models.items():
            if not path.exists():
                missing.append(f"{name}: {path}")
        
        if missing:
            print("⚠️  WARNING: Following model files are missing:")
            for m in missing:
                print(f"   - {m}")
            print()
            print("Models will be loaded in mock/demo mode.")
            return False
        
        return True


settings = Settings()
