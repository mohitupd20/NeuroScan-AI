import numpy as np
from PIL import Image
import io


class ImageProcessor:
    """Utility class for image processing and preprocessing"""
    
    @staticmethod
    async def read_uploaded_file(file):
        """
        Read uploaded file and convert to numpy array
        
        Args:
            file: UploadFile object from FastAPI
        
        Returns:
            numpy array of image in RGB format
        """
        try:
            # Read file contents
            contents = await file.read()
            
            # Convert to PIL Image
            image = Image.open(io.BytesIO(contents))
            
            # Convert to RGB if necessary (handles PNG with alpha, grayscale, etc.)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array
            image_array = np.array(image)
            
            return image_array
        
        except Exception as e:
            raise Exception(f"Error reading uploaded file: {str(e)}")
    
    @staticmethod
    def resize_image(image_array, target_size=(512, 512)):
        """
        Resize image to target size
        
        Args:
            image_array: numpy array of image
            target_size: tuple (height, width)
        
        Returns:
            resized numpy array
        """
        image = Image.fromarray(image_array.astype('uint8'))
        image = image.resize(target_size)
        return np.array(image)
    
    @staticmethod
    def normalize_image(image_array):
        """
        Normalize image to 0-1 range
        
        Args:
            image_array: numpy array of image
        
        Returns:
            normalized array
        """
        return image_array.astype(np.float32) / 255.0
