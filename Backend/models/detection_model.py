"""
YOLO-based Tumor Detection Module
Provides accurate tumor detection with bounding box extraction and visualization
"""

import cv2
import numpy as np
from pathlib import Path
import base64
import sys

from .model_manager import ModelManager


class TumorDetector:
    """Handles tumor detection using YOLO model"""
    
    def __init__(self, model_path='yolo_best.pt'):
        """Initialize detector with YOLO model"""
        self.model = ModelManager.load_yolo_model(model_path)
        self.device = ModelManager.get_device()
    
    def is_loaded(self):
        """Check if model is properly loaded"""
        return self.model is not None
    
    def detect(self, image, conf_threshold=0.5, iou_threshold=0.5):
        """Perform YOLO detection on image"""
        if not self.is_loaded():
            print("⚠ Model not loaded")
            return None
        
        try:
            results = self.model(image, conf=conf_threshold, iou=iou_threshold, verbose=False)
            return results
        except Exception as e:
            print(f"❌ Detection error: {e}")
            return None
    
    def extract_detections(self, image, results, padding_percent=10):
        """Extract detection boxes, confidence, and ROIs from YOLO results"""
        detections = []
        
        if results is None or len(results) == 0:
            return None, "No detections found"
        
        try:
            if isinstance(results, list):
                result = results[0]
            else:
                result = results
            
            if not hasattr(result, 'boxes') or result.boxes is None:
                return None, "No boxes in detection result"
            
            boxes = result.boxes
            h, w = image.shape[:2]
            
            for idx, box in enumerate(boxes):
                try:
                    xyxy = box.xyxy[0]
                    x1, y1, x2, y2 = float(xyxy[0]), float(xyxy[1]), float(xyxy[2]), float(xyxy[3])
                    
                    conf = float(box.conf[0]) if hasattr(box, 'conf') and len(box.conf) > 0 else 0.0
                    cls = int(box.cls[0]) if hasattr(box, 'cls') and len(box.cls) > 0 else 0
                    
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    box_width = x2 - x1
                    box_height = y2 - y1
                    pad_x = int(box_width * padding_percent / 100)
                    pad_y = int(box_height * padding_percent / 100)
                    
                    x1_pad = max(0, x1 - pad_x)
                    y1_pad = max(0, y1 - pad_y)
                    x2_pad = min(w, x2 + pad_x)
                    y2_pad = min(h, y2 + pad_y)
                    
                    roi = image[y1_pad:y2_pad, x1_pad:x2_pad].copy()
                    area = (x2 - x1) * (y2 - y1)
                    
                    detection = {
                        'id': idx,
                        'original_bbox': [x1, y1, x2, y2],
                        'padded_bbox': [x1_pad, y1_pad, x2_pad, y2_pad],
                        'bbox': [x1, y1, x2, y2],
                        'roi': roi,
                        'confidence': float(conf),
                        'class': int(cls),
                        'area': int(area),
                        'width': x2 - x1,
                        'height': y2 - y1
                    }
                    
                    detections.append(detection)
                    print(f"✓ Detection {idx+1}: Conf={conf:.2%}, Bbox=[{x1},{y1},{x2},{y2}]")
                
                except Exception as e:
                    print(f"⚠ Error processing box {idx}: {e}")
                    continue
            
            if detections:
                return detections, f"Found {len(detections)} tumor(s)"
            else:
                return None, "No valid detections extracted"
        
        except Exception as e:
            print(f"❌ Error extracting detections: {e}")
            return None, f"Error: {str(e)}"
    
    def visualize_detections(self, image, detections, draw_center=True, draw_area=True):
        """Draw detection boxes on image with all information"""
        viz_image = image.copy()
        
        if not detections:
            return viz_image
        
        for idx, det in enumerate(detections):
            x1, y1, x2, y2 = det['bbox']
            conf = det['confidence']
            
            cv2.rectangle(viz_image, (x1, y1), (x2, y2), (0, 255, 255), 3)
            
            label = f"Tumor {idx+1}: {conf:.1%}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            thickness = 2
            
            text_size = cv2.getTextSize(label, font, font_scale, thickness)[0]
            text_x = x1
            text_y = y1 - 10
            
            cv2.rectangle(viz_image, 
                         (text_x, text_y - text_size[1] - 5),
                         (text_x + text_size[0], text_y + 5),
                         (0, 255, 255), -1)
            
            cv2.putText(viz_image, label, (text_x, text_y),
                       font, font_scale, (0, 0, 0), thickness)
            
            coord_text = f"({x1},{y1}) ({x2},{y2})"
            cv2.putText(viz_image, coord_text, (x1, y2 + 25),
                       font, 0.5, (0, 255, 255), 1)
            
            if draw_center:
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                cv2.circle(viz_image, (center_x, center_y), 5, (0, 255, 255), -1)
                cv2.putText(viz_image, f"C:({center_x},{center_y})", 
                           (center_x + 10, center_y - 10),
                           font, 0.4, (0, 255, 255), 1)
            
            if draw_area:
                area_text = f"Area: {det['area']}px²"
                cv2.putText(viz_image, area_text, (x1, y2 + 45),
                           font, 0.5, (255, 0, 255), 1)
        
        return viz_image
    
    @staticmethod
    def image_to_base64(image):
        """Convert numpy array image to base64 string"""
        try:
            _, buffer = cv2.imencode('.png', image)
            return base64.b64encode(buffer).decode()
        except Exception as e:
            print(f"Error converting to base64: {e}")
            return None
    
    def predict(self, image_array, conf=0.5, iou=0.5, padding=10):
        """Complete detection pipeline"""
        if len(image_array.shape) == 2:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)
        elif image_array.shape[2] == 4:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)
        
        results = self.detect(image_array, conf, iou)
        detections, message = self.extract_detections(image_array, results, padding)
        
        viz_image = self.visualize_detections(image_array, detections) if detections else image_array
        viz_base64 = self.image_to_base64(viz_image)
        
        return {
            'detected_image_base64': viz_base64,
            'detected_image': viz_image,
            'detections': detections or [],
            'tumor_count': len(detections) if detections else 0,
            'message': message
        }


# Backward compatibility
DetectionModel = TumorDetector
