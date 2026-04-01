import torch
import torch.nn as nn
from pathlib import Path
import numpy as np
from PIL import Image
from torchvision import models, transforms


class ClassificationModel:
    """Wrapper for brain tumor classification"""

    def __init__(self):
        # 1. Device selection (MPS for Apple Silicon, otherwise CUDA/CPU)
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
            print("🚀 Using Apple Silicon GPU (MPS)")
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
            print("🚀 Using CUDA GPU")
        else:
            self.device = torch.device("cpu")
            print("Using CPU")

        # 2. Model definition (ResNet50, 4-class output)
        self.model = models.resnet50(weights=None)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 4)
        self.model = self.model.to(self.device)

        # 3. Class labels
        self.classes = ["Glioma", "Meningioma", "No Tumor", "Pituitary"]

        # 4. Preprocessing pipeline
        self.preprocess_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        self.load_model()
    
    def load_model(self):
        """Load pre-trained weights"""
        model_path = Path(__file__).parent.parent / "best_brain_tumor_model.pth"
        try:
            checkpoint = torch.load(model_path, map_location=self.device)
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                self.model.load_state_dict(checkpoint['model_state_dict'])
            else:
                self.model.load_state_dict(checkpoint)
            self.model.eval()
            print(f"✓ Classification model loaded from {model_path}")
        except Exception as e:
            print(f"⚠ Warning: Could not load classification model weights: {e}")
            print("  Using random initialization")

    def preprocess(self, image_array):
        """Preprocess image for classification"""
        if isinstance(image_array, np.ndarray):
            image = Image.fromarray(image_array.astype('uint8'))
        else:
            image = image_array

        image = image.convert('RGB')
        input_tensor = self.preprocess_transform(image)

        return input_tensor.unsqueeze(0).to(self.device)

    def predict(self, image_array):
        """Perform classification prediction"""
        try:
            with torch.no_grad():
                input_tensor = self.preprocess(image_array)
                output = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(output, dim=1)
                confidence, predicted = torch.max(probabilities, 1)

                predicted_class = self.classes[predicted.item()]
                confidence_score = confidence.item()

                return {
                    "classification": predicted_class,
                    "confidence": float(confidence_score),
                    "all_probabilities": {
                        self.classes[i]: float(probabilities[0, i].item())
                        for i in range(len(self.classes))
                    }
                }
        except Exception as e:
            raise Exception(f"Classification error: {str(e)}")

