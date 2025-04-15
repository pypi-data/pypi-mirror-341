"""
Outlier detection and handling for SBYB.

This module provides components for detecting and handling outliers in data.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

from sbyb.core.exceptions import PreprocessingError
from sbyb.core.utils import get_column_types
from sbyb.preprocessing.base import ColumnBasedPreprocessor


class OutlierHandler(ColumnBasedPreprocessor):
    """
    Outlier detection and handling component.
    
    This component detects and handles outliers in numeric data using various methods.
    """
    
    DETECTION_METHODS = ['iqr', 'zscore', 'isolation_forest', 'lof']
    HANDLING_STRATEGIES = ['clip', 'remove', 'impute', 'flag']
    
    def __init__(self, columns: Optional[List[str]] = None,
                 detection_method: str = 'iqr',
                 threshold: float = 1.5,
                 handling_strategy: str = 'clip',
                 contamination: float = 0.05,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the outlier handler.
        
        Args:
            columns: List of column names to process. If None, all numeric columns will be processed.
            detection_method: Method for detecting outliers ('iqr', 'zscore', 'isolation_forest', 'lof').
            threshold: Threshold for outlier detection (multiplier for IQR or Z-score).
            handling_strategy: Strategy for handling outliers ('clip', 'remove', 'impute', 'flag').
            contamination: Expected proportion of outliers in the data (for isolation_forest and lof).
            config: Configuration dictionary for the outlier handler.
        """
        super().__init__(columns, config)
        
        # Validate parameters
        if detection_method not in self.DETECTION_METHODS:
            raise ValueError(f"Invalid detection method: {detection_method}. Must be one of {self.DETECTION_METHODS}")
        if handling_strategy not in self.HANDLING_STRATEGIES:
            raise ValueError(f"Invalid handling strategy: {handling_strategy}. Must be one of {self.HANDLING_STRATEGIES}")
        
        self.detection_method = detection_method
        self.threshold = threshold
        self.handling_strategy = handling_strategy
        self.contamination = contamination
        
        # Store parameters for each column
        self._column_params = {}
        self._outlier_detector = None
    
    def _select_columns(self, data: pd.DataFrame) -> List[str]:
        """
        Select numeric columns for outlier handling.
        
        Args:
            data: Input data.
            
        Returns:
            List of numeric column names.
        """
        column_types = get_column_types(data)
        return column_types['numeric']
    
    def fit(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> 'OutlierHandler':
        """
        Fit the outlier handler to the data.
        
        Args:
            data: Input data to fit the outlier handler.
            **kwargs: Additional keyword arguments.
            
        Returns:
            self: The fitted outlier handler.
        """
        data = self._validate_input(data)
        self._fitted_columns = self._get_columns(data)
        
        # For global methods (isolation_forest, lof), fit on all numeric columns together
        if self.detection_method in ['isolation_forest', 'lof']:
            numeric_data = data[self._fitted_columns].copy()
            
            # Handle NaN values for fitting
            numeric_data = numeric_data.fillna(numeric_data.mean())
            
            if self.detection_method == 'isolation_forest':
                self._outlier_detector = IsolationForest(
                    contamination=self.contamination,
                    random_state=42
                )
            else:  # lof
                self._outlier_detector = LocalOutlierFactor(
                    n_neighbors=20,
                    contamination=self.contamination,
                    novelty=True
                )
            
            self._outlier_detector.fit(numeric_data)
        
        # For column-wise methods (iqr, zscore), compute parameters for each column
        else:
            for col in self._fitted_columns:
                if self.detection_method == 'iqr':
                    q1 = data[col].quantile(0.25)
                    q3 = data[col].quantile(0.75)
                    iqr = q3 - q1
                    lower_bound = q1 - self.threshold * iqr
                    upper_bound = q3 + self.threshold * iqr
                    self._column_params[col] = {
                        'lower_bound': lower_bound,
                        'upper_bound': upper_bound
                    }
                elif self.detection_method == 'zscore':
                    mean = data[col].mean()
                    std = data[col].std()
                    self._column_params[col] = {
                        'mean': mean,
                        'std': std,
                        'threshold': self.threshold
                    }
        
        self._is_fitted = True
        return self
    
    def transform(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> pd.DataFrame:
        """
        Detect and handle outliers in the data.
        
        Args:
            data: Input data to process.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Data with outliers handled.
        """
        self._check_is_fitted()
        data = self._validate_input(data).copy()
        
        # Create a flag column for outliers if needed
        if self.handling_strategy == 'flag':
            for col in self._fitted_columns:
                if col in data.columns:
                    data[f"{col}_outlier"] = False
        
        # For global methods (isolation_forest, lof), process all columns together
        if self.detection_method in ['isolation_forest', 'lof'] and self._outlier_detector:
            numeric_data = data[self._fitted_columns].copy()
            
            # Handle NaN values for prediction
            numeric_data = numeric_data.fillna(numeric_data.mean())
            
            # Predict outliers
            if self.detection_method == 'isolation_forest':
                outlier_labels = self._outlier_detector.predict(numeric_data)
            else:  # lof
                outlier_labels = self._outlier_detector.predict(numeric_data)
            
            # Convert to boolean mask (True for outliers)
            outlier_mask = outlier_labels == -1
            
            # Handle outliers for each column
            for col in self._fitted_columns:
                if col in data.columns:
                    self._handle_outliers_for_column(data, col, outlier_mask)
        
        # For column-wise methods (iqr, zscore), process each column separately
        else:
            for col in self._fitted_columns:
                if col not in data.columns or col not in self._column_params:
                    continue
                
                # Detect outliers
                if self.detection_method == 'iqr':
                    params = self._column_params[col]
                    outlier_mask = (data[col] < params['lower_bound']) | (data[col] > params['upper_bound'])
                elif self.detection_method == 'zscore':
                    params = self._column_params[col]
                    z_scores = np.abs((data[col] - params['mean']) / params['std'])
                    outlier_mask = z_scores > params['threshold']
                
                # Handle outliers
                self._handle_outliers_for_column(data, col, outlier_mask)
        
        return data
    
    def _handle_outliers_for_column(self, data: pd.DataFrame, column: str, outlier_mask: np.ndarray) -> None:
        """
        Handle outliers for a specific column.
        
        Args:
            data: Input data.
            column: Column name.
            outlier_mask: Boolean mask indicating outliers.
        """
        if self.handling_strategy == 'clip':
            if self.detection_method in ['iqr', 'zscore']:
                params = self._column_params[column]
                if self.detection_method == 'iqr':
                    data.loc[data[column] < params['lower_bound'], column] = params['lower_bound']
                    data.loc[data[column] > params['upper_bound'], column] = params['upper_bound']
                else:  # zscore
                    lower_bound = params['mean'] - params['threshold'] * params['std']
                    upper_bound = params['mean'] + params['threshold'] * params['std']
                    data.loc[data[column] < lower_bound, column] = lower_bound
                    data.loc[data[column] > upper_bound, column] = upper_bound
            else:
                # For global methods, use percentiles for clipping
                lower_bound = data[column].quantile(0.01)
                upper_bound = data[column].quantile(0.99)
                data.loc[outlier_mask, column] = data.loc[outlier_mask, column].clip(lower_bound, upper_bound)
        
        elif self.handling_strategy == 'remove':
            # Set outliers to NaN (they will be handled by imputation later)
            data.loc[outlier_mask, column] = np.nan
        
        elif self.handling_strategy == 'impute':
            # Replace outliers with the median
            median_value = data[column].median()
            data.loc[outlier_mask, column] = median_value
        
        elif self.handling_strategy == 'flag':
            # Flag outliers in a separate column
            data.loc[outlier_mask, f"{column}_outlier"] = True
