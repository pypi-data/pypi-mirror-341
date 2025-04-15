"""
Base classes and interfaces for SBYB.

This module defines the abstract base classes and interfaces that form the foundation
of the SBYB library's architecture.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd


class SBYBComponent(ABC):
    """Base class for all SBYB components."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the component.
        
        Args:
            config: Configuration dictionary for the component.
        """
        self.config = config or {}
        self._validate_config()
        
    def _validate_config(self) -> None:
        """Validate the configuration."""
        pass
    
    @property
    def name(self) -> str:
        """Return the name of the component."""
        return self.__class__.__name__


class DataProcessor(SBYBComponent):
    """Base class for all data processors."""
    
    @abstractmethod
    def fit(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> 'DataProcessor':
        """
        Fit the processor to the data.
        
        Args:
            data: Input data to fit the processor.
            **kwargs: Additional keyword arguments.
            
        Returns:
            self: The fitted processor.
        """
        pass
    
    @abstractmethod
    def transform(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> Union[pd.DataFrame, np.ndarray]:
        """
        Transform the data using the fitted processor.
        
        Args:
            data: Input data to transform.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Transformed data.
        """
        pass
    
    def fit_transform(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> Union[pd.DataFrame, np.ndarray]:
        """
        Fit the processor to the data and transform it.
        
        Args:
            data: Input data to fit and transform.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Transformed data.
        """
        return self.fit(data, **kwargs).transform(data, **kwargs)


class Model(SBYBComponent):
    """Base class for all models."""
    
    @abstractmethod
    def fit(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray], **kwargs) -> 'Model':
        """
        Fit the model to the data.
        
        Args:
            X: Input features.
            y: Target variable.
            **kwargs: Additional keyword arguments.
            
        Returns:
            self: The fitted model.
        """
        pass
    
    @abstractmethod
    def predict(self, X: Union[pd.DataFrame, np.ndarray], **kwargs) -> Union[pd.Series, np.ndarray]:
        """
        Make predictions using the fitted model.
        
        Args:
            X: Input features.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Predictions.
        """
        pass
    
    def score(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray], **kwargs) -> float:
        """
        Calculate the score of the model on the given data.
        
        Args:
            X: Input features.
            y: Target variable.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Score value.
        """
        pass


class Pipeline(SBYBComponent):
    """Base class for pipelines that combine multiple components."""
    
    def __init__(self, steps: List[Tuple[str, SBYBComponent]], config: Optional[Dict[str, Any]] = None):
        """
        Initialize the pipeline.
        
        Args:
            steps: List of (name, component) tuples defining the pipeline steps.
            config: Configuration dictionary for the pipeline.
        """
        super().__init__(config)
        self.steps = steps
        
    @abstractmethod
    def fit(self, data: Any, **kwargs) -> 'Pipeline':
        """
        Fit the pipeline to the data.
        
        Args:
            data: Input data.
            **kwargs: Additional keyword arguments.
            
        Returns:
            self: The fitted pipeline.
        """
        pass
    
    @abstractmethod
    def transform(self, data: Any, **kwargs) -> Any:
        """
        Transform the data using the fitted pipeline.
        
        Args:
            data: Input data.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Transformed data.
        """
        pass
    
    def fit_transform(self, data: Any, **kwargs) -> Any:
        """
        Fit the pipeline to the data and transform it.
        
        Args:
            data: Input data.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Transformed data.
        """
        return self.fit(data, **kwargs).transform(data, **kwargs)


class TaskDetector(SBYBComponent):
    """Base class for task detection components."""
    
    @abstractmethod
    def detect(self, data: Union[pd.DataFrame, np.ndarray], target: Optional[Union[str, int]] = None) -> str:
        """
        Detect the machine learning task type from the data.
        
        Args:
            data: Input data.
            target: Target variable name or index.
            
        Returns:
            Detected task type.
        """
        pass


class Evaluator(SBYBComponent):
    """Base class for model evaluation components."""
    
    @abstractmethod
    def evaluate(self, model: Model, X: Union[pd.DataFrame, np.ndarray], 
                y: Union[pd.Series, np.ndarray], **kwargs) -> Dict[str, Any]:
        """
        Evaluate the model on the given data.
        
        Args:
            model: Fitted model to evaluate.
            X: Input features.
            y: Target variable.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Dictionary of evaluation metrics.
        """
        pass


class Deployer(SBYBComponent):
    """Base class for model deployment components."""
    
    @abstractmethod
    def deploy(self, model: Model, **kwargs) -> Dict[str, Any]:
        """
        Deploy the model.
        
        Args:
            model: Fitted model to deploy.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Dictionary with deployment information.
        """
        pass


class UIGenerator(SBYBComponent):
    """Base class for UI generation components."""
    
    @abstractmethod
    def generate(self, model: Model, **kwargs) -> Dict[str, Any]:
        """
        Generate a UI for the model.
        
        Args:
            model: Fitted model to create UI for.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Dictionary with UI information.
        """
        pass


class Plugin(SBYBComponent):
    """Base class for plugins."""
    
    @property
    @abstractmethod
    def plugin_type(self) -> str:
        """Return the type of the plugin."""
        pass
