"""
Classification task detection for SBYB.

This module provides specialized components for detecting classification tasks.
"""

from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import TaskDetectionError


class ClassificationDetector(SBYBComponent):
    """
    Classification task detection component.
    
    This component specializes in detecting binary and multiclass classification tasks.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the classification detector.
        
        Args:
            config: Configuration dictionary for the detector.
        """
        super().__init__(config)
    
    def detect(self, data: pd.DataFrame, target: Union[str, int]) -> Dict[str, Any]:
        """
        Detect if the data represents a classification task.
        
        Args:
            data: Input data.
            target: Target variable name or index.
            
        Returns:
            Dictionary with detection results:
                - is_classification: Whether the task is classification
                - task_type: Specific classification task type ('binary' or 'multiclass')
                - confidence: Confidence score for the detection
                - details: Additional details about the detection
        """
        # Extract target variable
        if isinstance(target, int):
            y = data.iloc[:, target]
            target_name = data.columns[target]
        else:
            y = data[target]
            target_name = target
        
        # Check if the target is categorical or has a small number of unique values
        is_categorical = pd.api.types.is_categorical_dtype(y.dtype) or pd.api.types.is_string_dtype(y.dtype)
        n_unique = y.nunique()
        
        # Determine if it's a classification task
        is_classification = is_categorical or (pd.api.types.is_numeric_dtype(y.dtype) and n_unique <= min(10, len(y) * 0.05))
        
        if not is_classification:
            return {
                'is_classification': False,
                'confidence': 0.9,
                'details': {
                    'reason': 'Target variable has too many unique values or is not categorical',
                    'n_unique': n_unique,
                    'dtype': str(y.dtype)
                }
            }
        
        # Determine if it's binary or multiclass
        if n_unique == 2:
            return {
                'is_classification': True,
                'task_type': 'binary',
                'confidence': 0.95,
                'details': {
                    'n_classes': 2,
                    'class_distribution': y.value_counts().to_dict(),
                    'target_column': target_name
                }
            }
        else:
            return {
                'is_classification': True,
                'task_type': 'multiclass',
                'confidence': 0.95,
                'details': {
                    'n_classes': n_unique,
                    'class_distribution': y.value_counts().to_dict(),
                    'target_column': target_name
                }
            }
    
    def get_class_weights(self, data: pd.DataFrame, target: Union[str, int]) -> Dict[Any, float]:
        """
        Calculate class weights for imbalanced classification tasks.
        
        Args:
            data: Input data.
            target: Target variable name or index.
            
        Returns:
            Dictionary mapping class labels to weights.
        """
        # Extract target variable
        if isinstance(target, int):
            y = data.iloc[:, target]
        else:
            y = data[target]
        
        # Calculate class frequencies
        class_counts = y.value_counts()
        n_samples = len(y)
        n_classes = len(class_counts)
        
        # Calculate weights: n_samples / (n_classes * class_count)
        weights = {cls: n_samples / (n_classes * count) for cls, count in class_counts.items()}
        
        return weights
