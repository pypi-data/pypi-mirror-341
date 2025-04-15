"""
Feature scaling for SBYB.

This module provides components for scaling numeric features.
"""

from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler

from sbyb.core.exceptions import PreprocessingError
from sbyb.core.utils import get_column_types
from sbyb.preprocessing.base import ColumnBasedPreprocessor


class FeatureScaler(ColumnBasedPreprocessor):
    """
    Feature scaling component.
    
    This component scales numeric features using various methods.
    """
    
    SCALING_METHODS = ['standard', 'minmax', 'robust', 'maxabs']
    
    def __init__(self, columns: Optional[List[str]] = None,
                 method: str = 'standard',
                 with_mean: bool = True,
                 with_std: bool = True,
                 feature_range: tuple = (0, 1),
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the feature scaler.
        
        Args:
            columns: List of column names to scale. If None, all numeric columns will be processed.
            method: Scaling method ('standard', 'minmax', 'robust', 'maxabs').
            with_mean: Whether to center the data before scaling (for standard scaling).
            with_std: Whether to scale the data to unit variance (for standard scaling).
            feature_range: Range of transformed values (for minmax scaling).
            config: Configuration dictionary for the scaler.
        """
        super().__init__(columns, config)
        
        # Validate parameters
        if method not in self.SCALING_METHODS:
            raise ValueError(f"Invalid scaling method: {method}. Must be one of {self.SCALING_METHODS}")
        
        self.method = method
        self.with_mean = with_mean
        self.with_std = with_std
        self.feature_range = feature_range
        
        # Scaler for all columns
        self._scaler = None
    
    def _select_columns(self, data: pd.DataFrame) -> List[str]:
        """
        Select numeric columns for scaling.
        
        Args:
            data: Input data.
            
        Returns:
            List of numeric column names.
        """
        column_types = get_column_types(data)
        return column_types['numeric']
    
    def fit(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> 'FeatureScaler':
        """
        Fit the feature scaler to the data.
        
        Args:
            data: Input data to fit the scaler.
            **kwargs: Additional keyword arguments.
            
        Returns:
            self: The fitted scaler.
        """
        data = self._validate_input(data)
        self._fitted_columns = self._get_columns(data)
        
        # Create scaler based on method
        if self.method == 'standard':
            self._scaler = StandardScaler(with_mean=self.with_mean, with_std=self.with_std)
        elif self.method == 'minmax':
            self._scaler = MinMaxScaler(feature_range=self.feature_range)
        elif self.method == 'robust':
            self._scaler = RobustScaler(with_centering=self.with_mean, with_scaling=self.with_std)
        elif self.method == 'maxabs':
            self._scaler = MaxAbsScaler()
        
        # Fit scaler on selected columns
        if self._fitted_columns:
            self._scaler.fit(data[self._fitted_columns])
        
        self._is_fitted = True
        return self
    
    def transform(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> pd.DataFrame:
        """
        Scale numeric features in the data.
        
        Args:
            data: Input data to scale.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Data with scaled numeric features.
        """
        self._check_is_fitted()
        data = self._validate_input(data).copy()
        
        # Scale selected columns
        if self._fitted_columns and self._scaler:
            columns_to_scale = [col for col in self._fitted_columns if col in data.columns]
            if columns_to_scale:
                scaled_data = self._scaler.transform(data[columns_to_scale])
                for i, col in enumerate(columns_to_scale):
                    data[col] = scaled_data[:, i]
        
        return data
