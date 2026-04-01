import torch
import torch.nn as nn
from pathlib import Path
import numpy as np
from PIL import Image
from torchvision import transforms
import base64
from io import BytesIO
import cv2


class ResUNetBlock(nn.Module):
    """ResUNet building block"""
    
    def __init__(self, in_channels, out_channels):
        super(ResUNetBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1)
        self.conv_skip = nn.Conv2d(in_channels, out_channels, kernel_size=1) if in_channels != out_channels else None
    
    def forward(self, x):
        skip = x
        x = self.conv1(x)
        x = self.relu(x)
        x = self.conv2(x)
        if self.conv_skip:
            skip = self.conv_skip(skip)
        x = x + skip
        x = self.relu(x)
        return x


class SegmentationModel:
    """Wrapper for brain tumor segmentation using ResUNet"""
    
    def __init__(self):
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model_state = None
            self.is_model_loaded = False
            self.load_model()
        except Exception as e:
            print(f"⚠ Warning: Segmentation model initialization error: {e}")
            self.device = torch.device("cpu")
            self.model_state = None
            self.is_model_loaded = False
    
    def is_loaded(self):
        """Check if model is properly loaded"""
        return self.is_model_loaded
    
    def load_model(self):
        """Load pre-trained segmentation model"""
        try:
            model_path = Path(__file__).parent.parent / "resunet_best_optimized.pth"
            if not model_path.exists():
                print(f"⚠ Model file not found: {model_path}")
                return
            
            checkpoint = torch.load(model_path, map_location=self.device)
            
            # Try different ways to extract the model
            if isinstance(checkpoint, dict):
                if 'model_state_dict' in checkpoint:
                    self.model_state = checkpoint['model_state_dict']
                elif 'state_dict' in checkpoint:
                    self.model_state = checkpoint['state_dict']
                else:
                    self.model_state = checkpoint
            else:
                self.model_state = checkpoint
            
            self.is_model_loaded = True
            print(f"✓ Segmentation model loaded from {model_path}")
        except Exception as e:
            print(f"⚠ Warning: Could not load segmentation weights: {e}")
            print("  Using mock mode for demonstration")
            self.model_state = None
            self.is_model_loaded = False
    
    def validate_image(self, image_array):
        """Validate if image is suitable for processing"""
        if image_array is None:
            return False, "Image is None"
        
        if len(image_array.shape) < 2:
            return False, "Invalid image shape"
        
        if image_array.shape[0] < 32 or image_array.shape[1] < 32:
            return False, "ROI too small (minimum 32×32)"
        
        return True, "Valid image"
    
    def segment(self, roi):
        """Segment tumor in ROI using thresholding and morphological operations
        
        Args:
            roi: Region of interest (numpy array)
        
        Returns:
            Segmentation mask as binary numpy array
        """
        try:
            if roi is None or roi.shape[0] == 0 or roi.shape[1] == 0:
                return np.zeros((roi.shape[0], roi.shape[1]), dtype=np.uint8) if roi is not None else None
            
            # Convert to grayscale if needed
            if len(roi.shape) == 3:
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            else:
                gray = roi.copy()
            
            # Normalize to 0-255 if needed
            if gray.dtype != np.uint8:
                gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            
            # Enhance contrast with CLAHE
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            
            # Apply bilateral filter to smooth while preserving edges
            filtered = cv2.bilateralFilter(enhanced, 5, 50, 50)
            
            # Use Otsu's thresholding for better segmentation
            _, thresh = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Apply morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Find connected components and keep larger ones (likely tumor)
            num_labels, labels = cv2.connectedComponents(mask)
            if num_labels > 1:
                # Get size of each component
                component_sizes = np.bincount(labels.ravel())
                # Keep components larger than 1% of ROI size
                min_size = int(roi.shape[0] * roi.shape[1] * 0.01)
                mask = np.zeros_like(mask)
                for label_idx in range(1, num_labels):
                    if component_sizes[label_idx] > min_size:
                        mask[labels == label_idx] = 255
            
            return mask.astype(np.uint8)
        except Exception as e:
            print(f"❌ Segmentation error: {e}")
            return np.zeros(roi.shape[:2], dtype=np.uint8) if roi is not None else None
    
    def create_overlay(self, roi, mask, alpha=0.5):
        """Create overlay of segmentation on original ROI with red color
        
        Args:
            roi: Original ROI image
            mask: Segmentation mask
            alpha: Blend factor (0-1)
        
        Returns:
            Overlaid image
        """
        try:
            if mask is None or np.all(mask == 0):
                return roi.copy()
            
            # Ensure ROI is 3-channel
            if len(roi.shape) == 2:
                roi_3ch = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
            else:
                roi_3ch = roi.copy() if roi.shape[2] == 3 else cv2.cvtColor(roi, cv2.COLOR_RGBA2BGR)
            
            # Normalize roi to 0-255 if needed
            if roi_3ch.dtype != np.uint8:
                roi_3ch = cv2.normalize(roi_3ch, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            
            # Create red mask (RED in RGB = BGR: [0, 0, 255])
            colored_mask = np.zeros_like(roi_3ch, dtype=np.uint8)
            colored_mask[mask > 127] = [0, 0, 255]  # Red in BGR
            
            # Blend: weighted average
            overlay = cv2.addWeighted(roi_3ch, 1 - alpha, colored_mask, alpha, 0)
            
            # Add green contours for better visibility
            try:
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(overlay, contours, -1, (0, 255, 0), 2)
            except:
                pass  # If contour drawing fails, just return the overlay
            
            return overlay
        except Exception as e:
            print(f"Error creating overlay: {e}")
            return roi.copy()
    
    def create_full_image_overlay(self, original_image, roi, mask, bbox, alpha=0.5):
        """Create overlay showing segmentation on full original MRI image
        
        Args:
            original_image: Full MRI image
            roi: Region of interest
            mask: Segmentation mask
            bbox: Bounding box coordinates (x1, y1, x2, y2)
            alpha: Blend factor
        
        Returns:
            Full image with segmentation overlay
        """
        try:
            if mask is None or np.all(mask == 0):
                return original_image.copy()
            
            result = original_image.copy().astype(np.uint8)
            
            # Extract bbox coordinates
            x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            
            # Ensure we have valid coordinates within image bounds
            x1 = max(0, min(x1, result.shape[1] - 1))
            y1 = max(0, min(y1, result.shape[0] - 1))
            x2 = max(x1 + 1, min(x2, result.shape[1]))
            y2 = max(y1 + 1, min(y2, result.shape[0]))
            
            roi_height = y2 - y1
            roi_width = x2 - x1
            
            # Resize mask to match the bbox region if needed
            if mask.shape[0] != roi_height or mask.shape[1] != roi_width:
                mask_resized = cv2.resize(mask, (roi_width, roi_height), interpolation=cv2.INTER_NEAREST)
            else:
                mask_resized = mask
            
            # Ensure result is 3-channel
            if len(result.shape) == 2:
                result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
            
            # Extract the ROI region for processing
            roi_region = result[y1:y2, x1:x2].copy()
            
            # Create red overlay only where mask is present
            overlay_region = roi_region.copy()
            overlay_region[mask_resized > 127] = [0, 0, 255]  # Red in BGR
            
            # Blend the overlay with the original ROI
            blended = cv2.addWeighted(roi_region, 1 - alpha, overlay_region, alpha, 0)
            
            # Place the blended ROI back into the full image
            result[y1:y2, x1:x2] = blended.astype(np.uint8)
            
            # Draw green contour around the segmented region
            try:
                contours, _ = cv2.findContours(mask_resized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    for contour in contours:
                        # Offset contour to match full image coordinates
                        contour_offset = contour + np.array([[[x1, y1]]])
                        cv2.drawContours(result, [contour_offset], 0, (0, 255, 0), 2)
            except Exception as e:
                print(f"⚠ Could not draw contours: {e}")
            
            return result.astype(np.uint8)
        except Exception as e:
            print(f"Error creating full image overlay: {e}")
            import traceback
            traceback.print_exc()
            return original_image.copy()
    
    def calculate_statistics(self, mask, roi):
        """Calculate segmentation statistics
        
        Args:
            mask: Segmentation mask
            roi: Region of interest
        
        Returns:
            Dictionary with statistics
        """
        if mask is None:
            return {
                'segmented_pixels': 0,
                'total_pixels': roi.shape[0] * roi.shape[1] if roi is not None else 0,
                'coverage_percentage': 0.0
            }
        
        mask_area = np.count_nonzero(mask)
        roi_area = mask.shape[0] * mask.shape[1]
        coverage_percentage = (mask_area / roi_area) * 100 if roi_area > 0 else 0
        
        return {
            'segmented_pixels': int(mask_area),
            'total_pixels': int(roi_area),
            'coverage_percentage': float(coverage_percentage)
        }
    
    def predict(self, image_array, original_image=None, bbox=None):
        """Perform segmentation prediction with mask and statistics
        
        Args:
            image_array: Input image (ROI or full image)
            original_image: (Optional) Full original image for overlay context
            bbox: (Optional) Bounding box [x1, y1, x2, y2] for placing ROI overlay on full image
        
        Returns:
            Dictionary with segmentation results and base64 images
        """
        try:
            # Validate input
            if image_array is None:
                raise ValueError("Image array is None")
            
            print(f"[Segmentation] Input shape: {image_array.shape}, dtype: {image_array.dtype}")
            
            # Get segmentation mask
            mask = self.segment(image_array)
            
            if mask is None:
                raise ValueError("Segmentation mask is None")
            
            print(f"[Segmentation] Mask shape: {mask.shape}, non-zero pixels: {np.count_nonzero(mask)}")
            
            # Resize mask if needed (to match image size)
            if mask.shape[:2] != image_array.shape[:2]:
                print(f"[Segmentation] Resizing mask from {mask.shape} to {image_array.shape[:2]}")
                mask = cv2.resize(mask, (image_array.shape[1], image_array.shape[0]), interpolation=cv2.INTER_NEAREST)
            
            print(f"[Segmentation] Final mask non-zero pixels: {np.count_nonzero(mask)}")
            
            # Calculate statistics
            stats = self.calculate_statistics(mask, image_array)
            print(f"[Segmentation] Coverage: {stats['coverage_percentage']:.2f}%")
            
            # Prepare image for display
            if len(image_array.shape) == 2:
                original = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)
            elif len(image_array.shape) == 3 and image_array.shape[2] == 4:
                original = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)
            else:
                original = image_array.copy().astype(np.uint8)
            
            # Create ROI overlay (for mask display)
            roi_overlay = self.create_overlay(original, mask, alpha=0.5)
            
            # Create full-image overlay if original image and bbox provided
            if original_image is not None and bbox is not None:
                try:
                    print(f"[Segmentation] Creating full image overlay with bbox: {bbox}")
                    full_overlay = self.create_full_image_overlay(original_image, image_array, mask, bbox, alpha=0.5)
                    print(f"[Segmentation] Full overlay created successfully")
                except Exception as e:
                    print(f"⚠ Warning: Full image overlay failed: {e}, using ROI overlay instead")
                    import traceback
                    traceback.print_exc()
                    full_overlay = roi_overlay
            else:
                print(f"[Segmentation] No original_image or bbox provided, using ROI overlay only")
                full_overlay = roi_overlay
            
            # Convert mask to uint8 for base64
            mask_uint8 = (mask.astype(np.float32) / 255.0 * 255).astype(np.uint8)
            
            # Convert to base64
            mask_pil = Image.fromarray(mask_uint8)
            mask_base64 = self._image_to_base64(mask_pil)
            
            # Full image overlay for display
            full_overlay_pil = Image.fromarray(cv2.cvtColor(full_overlay, cv2.COLOR_BGR2RGB))
            full_overlay_base64 = self._image_to_base64(full_overlay_pil)
            
            # ROI overlay for reference
            roi_overlay_pil = Image.fromarray(cv2.cvtColor(roi_overlay, cv2.COLOR_BGR2RGB))
            roi_overlay_base64 = self._image_to_base64(roi_overlay_pil)
            
            return {
                "mask_base64": mask_base64,
                "segmented_image_base64": full_overlay_base64,  # Full image overlay
                "roi_overlay_base64": roi_overlay_base64,  # ROI-only overlay for reference
                "tumor_area_percentage": float(stats['coverage_percentage']),
                "statistics": stats
            }
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "mask_base64": "",
                "segmented_image_base64": "",
                "roi_overlay_base64": "",
                "tumor_area_percentage": 0,
                "statistics": {"segmented_pixels": 0, "total_pixels": 0, "coverage_percentage": 0}
            }
            print(f"❌ Segmentation prediction error: {e}")
            raise Exception(f"Segmentation error: {str(e)}")
    
    @staticmethod
    def _image_to_base64(image):
        """Convert PIL Image to base64 string"""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str


# Alias for backward compatibility with new architecture naming
SegmentationProcessor = SegmentationModel
