"""
NeuroPath AI - Model Wrappers Package

This package contains wrappers for the three medical imaging models:
- Classification: Brain tumor type identification
- Segmentation: Tumor region highlighting
- Detection: Tumor location and bounding boxes
"""

from .model_manager import ModelManager
from .classification_model import ClassificationModel
from .detection_model import TumorDetector, DetectionModel
from .segmentation_model import SegmentationProcessor, SegmentationModel

__all__ = [
    "ModelManager",
    "ClassificationModel",
    "TumorDetector",
    "DetectionModel",
    "SegmentationProcessor",
    "SegmentationModel"
]

