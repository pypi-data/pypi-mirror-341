"""
Main task detection component for SBYB.

This module provides the main task detection logic for automatically determining
the appropriate machine learning task based on data characteristics.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import os
from pathlib import Path

from sbyb.core.base import TaskDetector, SBYBComponent
from sbyb.core.exceptions import TaskDetectionError
from sbyb.core.utils import get_column_types, is_classification_target, is_regression_target


class TaskDetector(SBYBComponent):
    """
    Task detection component.
    
    This component automatically detects the appropriate machine learning task
    based on the data characteristics.
    """
    
    TASK_TYPES = [
        'binary_classification',
        'multiclass_classification',
        'multilabel_classification',
        'regression',
        'clustering',
        'nlp_classification',
        'nlp_regression',
        'computer_vision',
        'time_series_forecasting',
        'time_series_classification',
        'anomaly_detection'
    ]
    
    def __init__(self, threshold: float = 0.7, default_task: str = 'classification', config: Optional[Dict[str, Any]] = None):
        """
        Initialize the task detector.
        
        Args:
            threshold: Confidence threshold for task detection.
            default_task: Default task to use if detection is uncertain.
            config: Configuration dictionary for the task detector.
        """
        super().__init__(config)
        self.threshold = threshold
        self.default_task = default_task
    
    def detect(self, data: Union[pd.DataFrame, np.ndarray, str], target: Optional[Union[str, int]] = None) -> Dict[str, Any]:
        """
        Detect the machine learning task type from the data.
        
        Args:
            data: Input data or path to data.
            target: Target variable name or index.
            
        Returns:
            Dictionary with detected task information:
                - task_type: The detected task type
                - confidence: Confidence score for the detection
                - data_type: The detected data type (tabular, text, image, time_series)
                - details: Additional details about the detection
        """
        # Handle different input types
        data_type, processed_data = self._process_input(data)
        
        # Detect task based on data type
        if data_type == 'tabular':
            return self._detect_tabular_task(processed_data, target)
        elif data_type == 'text':
            return self._detect_text_task(processed_data, target)
        elif data_type == 'image':
            return self._detect_image_task(processed_data, target)
        elif data_type == 'time_series':
            return self._detect_time_series_task(processed_data, target)
        else:
            raise TaskDetectionError(f"Unsupported data type: {data_type}")
    
    def _process_input(self, data: Union[pd.DataFrame, np.ndarray, str]) -> Tuple[str, Any]:
        """
        Process the input data and determine its type.
        
        Args:
            data: Input data or path to data.
            
        Returns:
            Tuple of (data_type, processed_data)
        """
        # If data is a string, it's a path to a file or directory
        if isinstance(data, str):
            return self._detect_from_path(data)
        
        # If data is a DataFrame, it's tabular data
        if isinstance(data, pd.DataFrame):
            return 'tabular', data
        
        # If data is a numpy array, determine its type based on shape
        if isinstance(data, np.ndarray):
            if len(data.shape) == 2:
                # 2D array is likely tabular data
                return 'tabular', pd.DataFrame(data)
            elif len(data.shape) == 3:
                # 3D array could be time series or grayscale images
                if data.shape[2] == 1:
                    return 'image', data
                else:
                    return 'time_series', data
            elif len(data.shape) == 4:
                # 4D array is likely image data (batch, height, width, channels)
                return 'image', data
        
        raise TaskDetectionError(f"Unable to determine data type from input: {type(data)}")
    
    def _detect_from_path(self, path: str) -> Tuple[str, Any]:
        """
        Detect data type from a file or directory path.
        
        Args:
            path: Path to file or directory.
            
        Returns:
            Tuple of (data_type, processed_data)
        """
        if os.path.isdir(path):
            # Check if it's an image directory
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
            files = list(Path(path).glob('*'))
            image_files = [f for f in files if f.suffix.lower() in image_extensions]
            
            if len(image_files) > 0 and len(image_files) / len(files) > 0.5:
                return 'image', path
            
            # Check if it's a text directory
            text_extensions = ['.txt', '.csv', '.json', '.xml', '.html']
            text_files = [f for f in files if f.suffix.lower() in text_extensions]
            
            if len(text_files) > 0 and len(text_files) / len(files) > 0.5:
                return 'text', path
        else:
            # It's a file, determine type from extension
            file_extension = os.path.splitext(path)[1].lower()
            
            if file_extension in ['.csv', '.xlsx', '.xls']:
                # Load tabular data
                if file_extension == '.csv':
                    data = pd.read_csv(path)
                else:
                    data = pd.read_excel(path)
                return 'tabular', data
            
            elif file_extension in ['.txt', '.json', '.xml', '.html']:
                return 'text', path
            
            elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
                return 'image', path
        
        # Default to tabular and try to load as CSV
        try:
            data = pd.read_csv(path)
            return 'tabular', data
        except:
            raise TaskDetectionError(f"Unable to determine data type from path: {path}")
    
    def _detect_tabular_task(self, data: pd.DataFrame, target: Optional[Union[str, int]] = None) -> Dict[str, Any]:
        """
        Detect the task type for tabular data.
        
        Args:
            data: Input tabular data.
            target: Target variable name or index.
            
        Returns:
            Dictionary with detected task information.
        """
        # If no target is specified, assume clustering or try to guess the target
        if target is None:
            # Try to find a likely target column (e.g., 'target', 'label', 'y', etc.)
            likely_targets = ['target', 'label', 'class', 'y', 'output', 'result']
            for col in likely_targets:
                if col in data.columns:
                    target = col
                    break
            
            # If still no target, check if there's a column that looks like a target
            if target is None:
                # Look for columns with few unique values relative to the dataset size
                for col in data.columns:
                    if pd.api.types.is_numeric_dtype(data[col].dtype):
                        n_unique = data[col].nunique()
                        if 1 < n_unique <= min(20, len(data) * 0.1):
                            target = col
                            break
            
            # If still no target, assume clustering
            if target is None:
                return {
                    'task_type': 'clustering',
                    'confidence': 0.8,
                    'data_type': 'tabular',
                    'details': {
                        'reason': 'No target variable specified or detected'
                    }
                }
        
        # Extract target variable
        if isinstance(target, int):
            y = data.iloc[:, target]
            target_name = data.columns[target]
        else:
            y = data[target]
            target_name = target
        
        # Check if it's a classification task
        if is_classification_target(y):
            n_classes = y.nunique()
            
            if n_classes == 2:
                return {
                    'task_type': 'binary_classification',
                    'confidence': 0.9,
                    'data_type': 'tabular',
                    'details': {
                        'n_classes': n_classes,
                        'target_column': target_name
                    }
                }
            else:
                return {
                    'task_type': 'multiclass_classification',
                    'confidence': 0.9,
                    'data_type': 'tabular',
                    'details': {
                        'n_classes': n_classes,
                        'target_column': target_name
                    }
                }
        
        # Check if it's a regression task
        if is_regression_target(y):
            return {
                'task_type': 'regression',
                'confidence': 0.9,
                'data_type': 'tabular',
                'details': {
                    'target_column': target_name
                }
            }
        
        # If we can't determine the task, default to classification
        return {
            'task_type': self.default_task,
            'confidence': 0.5,
            'data_type': 'tabular',
            'details': {
                'reason': 'Unable to confidently determine task type',
                'target_column': target_name
            }
        }
    
    def _detect_text_task(self, data: Union[pd.DataFrame, str], target: Optional[Union[str, int]] = None) -> Dict[str, Any]:
        """
        Detect the task type for text data.
        
        Args:
            data: Input text data or path to text data.
            target: Target variable name or index.
            
        Returns:
            Dictionary with detected task information.
        """
        # If data is a DataFrame with a target column, determine if it's classification or regression
        if isinstance(data, pd.DataFrame) and target is not None:
            # Extract target variable
            if isinstance(target, int):
                y = data.iloc[:, target]
                target_name = data.columns[target]
            else:
                y = data[target]
                target_name = target
            
            # Check if it's a classification task
            if is_classification_target(y):
                n_classes = y.nunique()
                
                if n_classes == 2:
                    return {
                        'task_type': 'nlp_classification',
                        'confidence': 0.9,
                        'data_type': 'text',
                        'details': {
                            'n_classes': n_classes,
                            'target_column': target_name,
                            'subtask': 'binary_classification'
                        }
                    }
                else:
                    return {
                        'task_type': 'nlp_classification',
                        'confidence': 0.9,
                        'data_type': 'text',
                        'details': {
                            'n_classes': n_classes,
                            'target_column': target_name,
                            'subtask': 'multiclass_classification'
                        }
                    }
            
            # Check if it's a regression task
            if is_regression_target(y):
                return {
                    'task_type': 'nlp_regression',
                    'confidence': 0.9,
                    'data_type': 'text',
                    'details': {
                        'target_column': target_name
                    }
                }
        
        # If we can't determine the task, default to NLP classification
        return {
            'task_type': 'nlp_classification',
            'confidence': 0.7,
            'data_type': 'text',
            'details': {
                'reason': 'Default NLP task without specific target information'
            }
        }
    
    def _detect_image_task(self, data: Union[np.ndarray, str], target: Optional[Union[str, int]] = None) -> Dict[str, Any]:
        """
        Detect the task type for image data.
        
        Args:
            data: Input image data or path to image data.
            target: Target variable name or index.
            
        Returns:
            Dictionary with detected task information.
        """
        # For image data, we typically assume computer vision tasks
        # If we have target information, we can determine if it's classification or regression
        if target is not None and isinstance(data, str) and os.path.isdir(data):
            # Check if subdirectories exist (common for image classification datasets)
            subdirs = [d for d in os.listdir(data) if os.path.isdir(os.path.join(data, d))]
            
            if len(subdirs) > 0:
                return {
                    'task_type': 'computer_vision',
                    'confidence': 0.9,
                    'data_type': 'image',
                    'details': {
                        'subtask': 'classification',
                        'n_classes': len(subdirs),
                        'classes': subdirs
                    }
                }
        
        # Default to general computer vision
        return {
            'task_type': 'computer_vision',
            'confidence': 0.8,
            'data_type': 'image',
            'details': {
                'reason': 'Default computer vision task without specific target information'
            }
        }
    
    def _detect_time_series_task(self, data: Union[pd.DataFrame, np.ndarray], target: Optional[Union[str, int]] = None) -> Dict[str, Any]:
        """
        Detect the task type for time series data.
        
        Args:
            data: Input time series data.
            target: Target variable name or index.
            
        Returns:
            Dictionary with detected task information.
        """
        # If data is a DataFrame, check for datetime columns
        if isinstance(data, pd.DataFrame):
            # Check for datetime columns
            datetime_cols = [col for col in data.columns if pd.api.types.is_datetime64_any_dtype(data[col].dtype)]
            
            if len(datetime_cols) > 0:
                # If we have a target column, determine if it's forecasting or classification
                if target is not None:
                    # Extract target variable
                    if isinstance(target, int):
                        y = data.iloc[:, target]
                        target_name = data.columns[target]
                    else:
                        y = data[target]
                        target_name = target
                    
                    # Check if it's a classification task
                    if is_classification_target(y):
                        return {
                            'task_type': 'time_series_classification',
                            'confidence': 0.9,
                            'data_type': 'time_series',
                            'details': {
                                'datetime_columns': datetime_cols,
                                'target_column': target_name,
                                'n_classes': y.nunique()
                            }
                        }
                    
                    # Otherwise, assume forecasting
                    return {
                        'task_type': 'time_series_forecasting',
                        'confidence': 0.9,
                        'data_type': 'time_series',
                        'details': {
                            'datetime_columns': datetime_cols,
                            'target_column': target_name
                        }
                    }
        
        # Default to time series forecasting
        return {
            'task_type': 'time_series_forecasting',
            'confidence': 0.7,
            'data_type': 'time_series',
            'details': {
                'reason': 'Default time series task without specific target information'
            }
        }
