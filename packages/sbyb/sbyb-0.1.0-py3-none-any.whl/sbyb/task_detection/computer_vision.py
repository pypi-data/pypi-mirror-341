"""
Computer vision task detection for SBYB.

This module provides specialized components for detecting computer vision tasks.
"""

from typing import Any, Dict, List, Optional, Union
import os
import glob
import numpy as np
import pandas as pd
from pathlib import Path

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import TaskDetectionError


class ComputerVisionDetector(SBYBComponent):
    """
    Computer vision task detection component.
    
    This component specializes in detecting computer vision tasks.
    """
    
    CV_TASKS = [
        'image_classification',
        'object_detection',
        'image_segmentation',
        'image_generation',
        'image_regression'
    ]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the computer vision detector.
        
        Args:
            config: Configuration dictionary for the detector.
        """
        super().__init__(config)
    
    def detect(self, data: Union[str, np.ndarray], target: Optional[Union[str, pd.Series]] = None) -> Dict[str, Any]:
        """
        Detect if the data represents a computer vision task and identify the specific task type.
        
        Args:
            data: Input data path or numpy array of images.
            target: Target variable (if applicable).
            
        Returns:
            Dictionary with detection results:
                - is_cv: Whether the task is a computer vision task
                - task_type: Specific computer vision task type
                - confidence: Confidence score for the detection
                - details: Additional details about the detection
        """
        # Handle different input types
        if isinstance(data, str):
            # Path to a file or directory
            return self._detect_from_path(data, target)
        elif isinstance(data, np.ndarray):
            # Numpy array of images
            return self._detect_from_array(data, target)
        else:
            raise TaskDetectionError(f"Unsupported data type for computer vision detection: {type(data)}")
    
    def _detect_from_path(self, path: str, target: Optional[Union[str, pd.Series]] = None) -> Dict[str, Any]:
        """
        Detect computer vision task from a file or directory path.
        
        Args:
            path: Path to file or directory.
            target: Target variable (if applicable).
            
        Returns:
            Dictionary with detection results.
        """
        if os.path.isdir(path):
            # Directory with image files
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
            image_files = []
            
            for ext in image_extensions:
                image_files.extend(glob.glob(os.path.join(path, f"*{ext}")))
                image_files.extend(glob.glob(os.path.join(path, f"*{ext.upper()}")))
            
            if not image_files:
                return {
                    'is_cv': False,
                    'confidence': 0.9,
                    'details': {
                        'reason': 'No image files found in the directory'
                    }
                }
            
            # Check for common CV dataset structures
            subdirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
            
            if len(subdirs) > 0:
                # Check if subdirectories contain images (common for classification datasets)
                subdir_image_counts = {}
                for subdir in subdirs:
                    subdir_path = os.path.join(path, subdir)
                    subdir_images = []
                    for ext in image_extensions:
                        subdir_images.extend(glob.glob(os.path.join(subdir_path, f"*{ext}")))
                        subdir_images.extend(glob.glob(os.path.join(subdir_path, f"*{ext.upper()}")))
                    subdir_image_counts[subdir] = len(subdir_images)
                
                if sum(subdir_image_counts.values()) > 0:
                    # Likely an image classification dataset with subdirectories for classes
                    return {
                        'is_cv': True,
                        'task_type': 'image_classification',
                        'confidence': 0.9,
                        'details': {
                            'n_classes': len(subdirs),
                            'classes': subdirs,
                            'images_per_class': subdir_image_counts,
                            'data_source': 'directory'
                        }
                    }
            
            # Check for annotation files (common for object detection/segmentation)
            annotation_files = glob.glob(os.path.join(path, "*.xml"))  # Pascal VOC format
            annotation_files.extend(glob.glob(os.path.join(path, "*.json")))  # COCO format
            
            if annotation_files:
                # Try to determine if it's object detection or segmentation
                task_type = 'object_detection'  # Default assumption
                confidence = 0.7
                
                # Sample an annotation file to check format
                try:
                    import json
                    with open(annotation_files[0], 'r') as f:
                        if annotation_files[0].endswith('.json'):
                            annotation = json.load(f)
                            # Check for segmentation data in COCO format
                            if 'annotations' in annotation and 'segmentation' in str(annotation):
                                task_type = 'image_segmentation'
                                confidence = 0.8
                except:
                    pass  # If reading fails, stick with default assumption
                
                return {
                    'is_cv': True,
                    'task_type': task_type,
                    'confidence': confidence,
                    'details': {
                        'n_images': len(image_files),
                        'n_annotations': len(annotation_files),
                        'data_source': 'directory'
                    }
                }
            
            # If no clear structure, default to image classification
            return {
                'is_cv': True,
                'task_type': 'image_classification',  # Default assumption
                'confidence': 0.7,
                'details': {
                    'n_images': len(image_files),
                    'data_source': 'directory',
                    'note': 'No clear task structure, defaulting to image classification'
                }
            }
        else:
            # Single file
            file_extension = os.path.splitext(path)[1].lower()
            
            if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
                # Single image file, likely for inference
                return {
                    'is_cv': True,
                    'task_type': 'image_classification',  # Default assumption
                    'confidence': 0.6,
                    'details': {
                        'data_source': 'file',
                        'file_type': file_extension,
                        'note': 'Single image file, assuming classification for inference'
                    }
                }
            elif file_extension in ['.csv', '.json']:
                # Could be metadata for images
                return {
                    'is_cv': True,
                    'task_type': 'image_classification',  # Default assumption
                    'confidence': 0.5,
                    'details': {
                        'data_source': 'file',
                        'file_type': file_extension,
                        'note': 'Metadata file, assuming related to image classification'
                    }
                }
            else:
                return {
                    'is_cv': False,
                    'confidence': 0.8,
                    'details': {
                        'reason': f'Unsupported file type for computer vision: {file_extension}',
                        'data_source': 'file'
                    }
                }
    
    def _detect_from_array(self, data: np.ndarray, target: Optional[Union[str, pd.Series]] = None) -> Dict[str, Any]:
        """
        Detect computer vision task from a numpy array.
        
        Args:
            data: Numpy array of images.
            target: Target variable (if applicable).
            
        Returns:
            Dictionary with detection results.
        """
        # Check if the array has the right shape for images
        if len(data.shape) not in [3, 4]:
            return {
                'is_cv': False,
                'confidence': 0.9,
                'details': {
                    'reason': f'Array shape {data.shape} is not compatible with image data',
                    'expected_shapes': ['(n_samples, height, width, channels)', '(height, width, channels)']
                }
            }
        
        # Determine if it's a single image or a batch
        is_batch = len(data.shape) == 4
        
        if is_batch:
            n_samples, height, width, channels = data.shape
        else:
            height, width, channels = data.shape
            n_samples = 1
        
        # If target is provided, determine the task type
        if target is not None:
            if isinstance(target, pd.Series):
                y = target
            elif isinstance(target, str) and os.path.exists(target):
                # Try to load target from file
                try:
                    if target.endswith('.csv'):
                        y = pd.read_csv(target).iloc[:, 0]
                    elif target.endswith('.json'):
                        import json
                        with open(target, 'r') as f:
                            y_data = json.load(f)
                            # Assume it's a list or dictionary with values
                            if isinstance(y_data, list):
                                y = pd.Series(y_data)
                            elif isinstance(y_data, dict):
                                y = pd.Series(list(y_data.values()))
                            else:
                                y = None
                    else:
                        y = None
                except:
                    y = None
            else:
                y = None
            
            if y is not None:
                # Check if it's classification or regression
                is_categorical = pd.api.types.is_categorical_dtype(y.dtype) or pd.api.types.is_string_dtype(y.dtype)
                n_unique = y.nunique()
                is_classification = is_categorical or (pd.api.types.is_numeric_dtype(y.dtype) and n_unique <= min(10, len(y) * 0.05))
                
                if is_classification:
                    return {
                        'is_cv': True,
                        'task_type': 'image_classification',
                        'confidence': 0.9,
                        'details': {
                            'n_samples': n_samples,
                            'image_shape': (height, width, channels),
                            'n_classes': n_unique,
                            'data_source': 'array'
                        }
                    }
                else:
                    return {
                        'is_cv': True,
                        'task_type': 'image_regression',
                        'confidence': 0.9,
                        'details': {
                            'n_samples': n_samples,
                            'image_shape': (height, width, channels),
                            'data_source': 'array'
                        }
                    }
        
        # If no target or target loading failed, make a best guess based on the data
        # Check for common image shapes
        is_standard_shape = (height == width) and height in [32, 64, 96, 128, 224, 256, 299, 384, 512]
        
        return {
            'is_cv': True,
            'task_type': 'image_classification',  # Default assumption
            'confidence': 0.7,
            'details': {
                'n_samples': n_samples,
                'image_shape': (height, width, channels),
                'is_standard_shape': is_standard_shape,
                'data_source': 'array',
                'note': 'No target information, defaulting to image classification'
            }
        }
    
    def suggest_preprocessing(self, data: Union[str, np.ndarray]) -> Dict[str, Any]:
        """
        Suggest preprocessing steps for the image data.
        
        Args:
            data: Input data path or numpy array of images.
            
        Returns:
            Dictionary with suggested preprocessing steps.
        """
        # Get basic information about the data
        if isinstance(data, str):
            # For directory paths, get image dimensions from a sample
            if os.path.isdir(data):
                image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
                image_files = []
                
                for ext in image_extensions:
                    image_files.extend(glob.glob(os.path.join(data, f"*{ext}")))
                    image_files.extend(glob.glob(os.path.join(data, f"*{ext.upper()}")))
                
                if not image_files:
                    return {
                        'error': 'No image files found in the directory'
                    }
                
                # Sample an image to get dimensions
                try:
                    from PIL import Image
                    sample_image = Image.open(image_files[0])
                    width, height = sample_image.size
                    channels = len(sample_image.getbands())
                except:
                    # If reading fails, use default values
                    width, height, channels = None, None, None
            else:
                # For single files, try to get dimensions
                try:
                    from PIL import Image
                    sample_image = Image.open(data)
                    width, height = sample_image.size
                    channels = len(sample_image.getbands())
                except:
                    # If reading fails, use default values
                    width, height, channels = None, None, None
        elif isinstance(data, np.ndarray):
            # For numpy arrays, get dimensions directly
            if len(data.shape) == 4:
                _, height, width, channels = data.shape
            elif len(data.shape) == 3:
                height, width, channels = data.shape
            else:
                return {
                    'error': f'Array shape {data.shape} is not compatible with image data'
                }
        else:
            return {
                'error': f'Unsupported data type for preprocessing suggestions: {type(data)}'
            }
        
        # Suggest preprocessing steps
        steps = ['normalization']  # Always normalize
        
        # Suggest resizing if dimensions are available
        if width is not None and height is not None:
            # Common target sizes for different models
            target_sizes = [224, 256, 299, 384]
            
            # Find the closest target size
            if max(width, height) > 64:  # Only suggest resizing for larger images
                closest_size = min(target_sizes, key=lambda x: abs(x - max(width, height)))
                steps.append(f'resize_to_{closest_size}x{closest_size}')
        
        # Always suggest data augmentation for training
        steps.append('data_augmentation')
        
        # Suggest channel adjustments if needed
        if channels == 1:
            steps.append('grayscale_to_rgb')
        elif channels == 4:  # RGBA
            steps.append('remove_alpha_channel')
        
        return {
            'suggested_steps': steps,
            'model_recommendations': [
                {'model': 'resnet50', 'suitability': 'high', 'input_size': '224x224'},
                {'model': 'efficientnet', 'suitability': 'high', 'input_size': '224x224 to 600x600'},
                {'model': 'mobilenet', 'suitability': 'high', 'input_size': '224x224'}
            ],
            'augmentation_recommendations': [
                'random_flip',
                'random_rotation',
                'random_zoom',
                'random_brightness',
                'random_contrast'
            ],
            'details': {
                'original_dimensions': f'{width}x{height}' if width is not None else 'unknown',
                'channels': channels if channels is not None else 'unknown'
            }
        }
