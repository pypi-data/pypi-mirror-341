"""
Preprocessing pipeline for SBYB.

This module provides a pipeline component that combines multiple preprocessing steps.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from sbyb.core.base import Pipeline, SBYBComponent
from sbyb.core.exceptions import PreprocessingError
from sbyb.preprocessing.base import BasePreprocessor
from sbyb.preprocessing.cleaner import DataCleaner
from sbyb.preprocessing.imputer import MissingValueImputer
from sbyb.preprocessing.outlier import OutlierHandler
from sbyb.preprocessing.encoder import CategoricalEncoder
from sbyb.preprocessing.scaler import FeatureScaler
from sbyb.preprocessing.feature_engineering import FeatureEngineer


class PreprocessingPipeline(Pipeline):
    """
    Preprocessing pipeline component.
    
    This component combines multiple preprocessing steps into a single pipeline.
    """
    
    def __init__(self, steps: Optional[List[Tuple[str, BasePreprocessor]]] = None,
                 include_cleaner: bool = True,
                 include_imputer: bool = True,
                 include_outlier_handler: bool = True,
                 include_encoder: bool = True,
                 include_scaler: bool = True,
                 include_feature_engineer: bool = False,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the preprocessing pipeline.
        
        Args:
            steps: List of (name, preprocessor) tuples defining the pipeline steps.
                If None, steps will be created based on the include_* parameters.
            include_cleaner: Whether to include a data cleaner step.
            include_imputer: Whether to include a missing value imputer step.
            include_outlier_handler: Whether to include an outlier handler step.
            include_encoder: Whether to include a categorical encoder step.
            include_scaler: Whether to include a feature scaler step.
            include_feature_engineer: Whether to include a feature engineer step.
            config: Configuration dictionary for the pipeline.
        """
        self.include_cleaner = include_cleaner
        self.include_imputer = include_imputer
        self.include_outlier_handler = include_outlier_handler
        self.include_encoder = include_encoder
        self.include_scaler = include_scaler
        self.include_feature_engineer = include_feature_engineer
        
        # Create default steps if not provided
        if steps is None:
            steps = self._create_default_steps(config)
        
        super().__init__(steps, config)
        self._is_fitted = False
    
    def _create_default_steps(self, config: Optional[Dict[str, Any]] = None) -> List[Tuple[str, BasePreprocessor]]:
        """
        Create default preprocessing steps.
        
        Args:
            config: Configuration dictionary.
            
        Returns:
            List of (name, preprocessor) tuples.
        """
        steps = []
        
        # Extract component-specific configs
        component_configs = {}
        if config:
            for component in ['cleaner', 'imputer', 'outlier', 'encoder', 'scaler', 'feature_engineer']:
                if component in config:
                    component_configs[component] = config[component]
        
        # Add cleaner
        if self.include_cleaner:
            cleaner_config = component_configs.get('cleaner')
            steps.append(('cleaner', DataCleaner(config=cleaner_config)))
        
        # Add imputer
        if self.include_imputer:
            imputer_config = component_configs.get('imputer')
            steps.append(('imputer', MissingValueImputer(config=imputer_config)))
        
        # Add outlier handler
        if self.include_outlier_handler:
            outlier_config = component_configs.get('outlier')
            steps.append(('outlier_handler', OutlierHandler(config=outlier_config)))
        
        # Add encoder
        if self.include_encoder:
            encoder_config = component_configs.get('encoder')
            steps.append(('encoder', CategoricalEncoder(config=encoder_config)))
        
        # Add scaler
        if self.include_scaler:
            scaler_config = component_configs.get('scaler')
            steps.append(('scaler', FeatureScaler(config=scaler_config)))
        
        # Add feature engineer
        if self.include_feature_engineer:
            feature_engineer_config = component_configs.get('feature_engineer')
            steps.append(('feature_engineer', FeatureEngineer(config=feature_engineer_config)))
        
        return steps
    
    def fit(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> 'PreprocessingPipeline':
        """
        Fit the preprocessing pipeline to the data.
        
        Args:
            data: Input data to fit the pipeline.
            **kwargs: Additional keyword arguments.
            
        Returns:
            self: The fitted pipeline.
        """
        # Convert to DataFrame if necessary
        if isinstance(data, np.ndarray):
            data = pd.DataFrame(data)
        
        # Fit each step
        for name, preprocessor in self.steps:
            data = preprocessor.fit_transform(data, **kwargs)
        
        self._is_fitted = True
        return self
    
    def transform(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> pd.DataFrame:
        """
        Transform the data using the fitted pipeline.
        
        Args:
            data: Input data to transform.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Transformed data.
        """
        if not self._is_fitted:
            raise PreprocessingError("Pipeline is not fitted. Call 'fit' before using 'transform'.")
        
        # Convert to DataFrame if necessary
        if isinstance(data, np.ndarray):
            data = pd.DataFrame(data)
        
        # Apply each step
        for name, preprocessor in self.steps:
            data = preprocessor.transform(data, **kwargs)
        
        return data
    
    def fit_transform(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> pd.DataFrame:
        """
        Fit the pipeline to the data and transform it.
        
        Args:
            data: Input data to fit and transform.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Transformed data.
        """
        return self.fit(data, **kwargs).transform(data, **kwargs)
    
    def get_step(self, name: str) -> Optional[BasePreprocessor]:
        """
        Get a step by name.
        
        Args:
            name: Name of the step.
            
        Returns:
            Preprocessor instance or None if not found.
        """
        for step_name, preprocessor in self.steps:
            if step_name == name:
                return preprocessor
        return None
