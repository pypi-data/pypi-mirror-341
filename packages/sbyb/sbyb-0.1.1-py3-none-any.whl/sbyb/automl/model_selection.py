"""
Model selection component for SBYB AutoML.

This module provides functionality for selecting appropriate machine learning models
based on the task type and data characteristics.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import ModelError
from sbyb.automl.models import get_models_for_task


class ModelSelector(SBYBComponent):
    """
    Model selection component.
    
    This component selects appropriate machine learning models based on the task type
    and data characteristics.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the model selector.
        
        Args:
            config: Configuration dictionary for the model selector.
        """
        super().__init__(config)
    
    def select_models(self, task: str, models: Optional[List[str]] = None, 
                     data_size: Optional[Tuple[int, int]] = None) -> List[Tuple[str, type, Dict[str, Any]]]:
        """
        Select appropriate models for the given task.
        
        Args:
            task: Machine learning task type ('binary', 'multiclass', 'regression', etc.).
            models: List of model names to consider. If None, all suitable models will be used.
            data_size: Tuple of (n_samples, n_features) representing the data size.
                Used to filter out models that are not suitable for the data size.
            
        Returns:
            List of tuples (model_name, model_class, default_params) for suitable models.
        """
        # Get all available models for the task
        available_models = get_models_for_task(task)
        
        # Filter by specified models if provided
        if models is not None:
            available_models = {name: model for name, model in available_models.items() if name in models}
            
            if not available_models:
                raise ModelError(f"None of the specified models are suitable for task '{task}'")
        
        # Filter by data size if provided
        if data_size is not None:
            n_samples, n_features = data_size
            
            # Filter out models that are not suitable for the data size
            filtered_models = {}
            for name, (model_class, default_params, metadata) in available_models.items():
                min_samples = metadata.get('min_samples', 0)
                max_features = metadata.get('max_features', float('inf'))
                
                if n_samples >= min_samples and n_features <= max_features:
                    filtered_models[name] = (model_class, default_params, metadata)
            
            available_models = filtered_models
            
            if not available_models:
                raise ModelError(f"No suitable models found for task '{task}' with data size {data_size}")
        
        # Convert to list of tuples (model_name, model_class, default_params)
        model_list = [(name, model_class, default_params) 
                     for name, (model_class, default_params, _) in available_models.items()]
        
        # Sort by priority (if available in metadata)
        model_list.sort(key=lambda x: available_models[x[0]][2].get('priority', 0), reverse=True)
        
        return model_list
    
    def get_model_info(self, model_name: str, task: str) -> Dict[str, Any]:
        """
        Get information about a specific model.
        
        Args:
            model_name: Name of the model.
            task: Machine learning task type.
            
        Returns:
            Dictionary with model information.
        """
        # Get all available models for the task
        available_models = get_models_for_task(task)
        
        if model_name not in available_models:
            raise ModelError(f"Model '{model_name}' is not available for task '{task}'")
        
        model_class, default_params, metadata = available_models[model_name]
        
        return {
            'name': model_name,
            'class': model_class.__name__,
            'module': model_class.__module__,
            'default_params': default_params,
            'metadata': metadata
        }
    
    def get_available_models(self, task: str) -> List[str]:
        """
        Get a list of all available models for the given task.
        
        Args:
            task: Machine learning task type.
            
        Returns:
            List of model names.
        """
        # Get all available models for the task
        available_models = get_models_for_task(task)
        
        return list(available_models.keys())
