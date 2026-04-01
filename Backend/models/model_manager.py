"""
Model Manager for loading and caching AI models
"""
import torch
import torch.nn as nn
from pathlib import Path
from ultralytics import YOLO


class ModelManager:
    """Manages loading and caching of detection and segmentation models"""
    
    _yolo_model = None
    _resunet_model = None
    _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    @classmethod
    def load_yolo_model(cls, model_path='yolo_best.pt'):
        """Load YOLO model for tumor detection"""
        if cls._yolo_model is not None:
            return cls._yolo_model
        
        try:
            model_path_obj = Path(__file__).parent.parent / model_path
            if not model_path_obj.exists():
                print(f"⚠ Warning: Model file not found at {model_path_obj}")
                return None
            
            model = YOLO(str(model_path_obj))
            model.to(cls._device)
            cls._yolo_model = model
            print(f"✓ YOLO model loaded successfully from {model_path_obj}")
            return model
        except Exception as e:
            print(f"❌ Error loading YOLO model: {e}")
            return None
    
    @classmethod
    def load_resunet_model(cls, model_path='resunet_best_optimized.pth'):
        """Load ResUNet model for segmentation"""
        if cls._resunet_model is not None:
            return cls._resunet_model
        
        try:
            model_path_obj = Path(__file__).parent.parent / model_path
            if not model_path_obj.exists():
                print(f"⚠ Warning: Model file not found at {model_path_obj}")
                return None
            
            checkpoint = torch.load(model_path_obj, map_location=cls._device)
            cls._resunet_model = checkpoint
            print(f"✓ ResUNet model loaded successfully from {model_path_obj}")
            return checkpoint
        except Exception as e:
            print(f"❌ Error loading ResUNet model: {e}")
            return None
    
    @classmethod
    def get_device(cls):
        """Get device (GPU or CPU)"""
        return cls._device
