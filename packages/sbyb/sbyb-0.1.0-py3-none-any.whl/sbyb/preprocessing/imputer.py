"""
Missing value imputation for SBYB.

This module provides components for detecting and imputing missing values in data.
"""

from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer, KNNImputer

from sbyb.core.exceptions import PreprocessingError
from sbyb.core.utils import get_column_types
from sbyb.preprocessing.base import ColumnBasedPreprocessor


class MissingValueImputer(ColumnBasedPreprocessor):
    """
    Missing value imputation component.
    
    This component detects and imputes missing values in data using various strategies.
    """
    
    STRATEGIES = {
        'numeric': ['mean', 'median', 'constant', 'knn'],
        'categorical': ['most_frequent', 'constant']
    }
    
    def __init__(self, columns: Optional[List[str]] = None,
                 numeric_strategy: str = 'mean',
                 categorical_strategy: str = 'most_frequent',
                 constant_value: Any = 0,
                 knn_neighbors: int = 5,
                 max_missing_ratio: float = 0.8,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the missing value imputer.
        
        Args:
            columns: List of column names to impute. If None, all columns with missing values will be processed.
            numeric_strategy: Strategy for imputing numeric columns ('mean', 'median', 'constant', 'knn').
            categorical_strategy: Strategy for imputing categorical columns ('most_frequent', 'constant').
            constant_value: Value to use for constant imputation.
            knn_neighbors: Number of neighbors to use for KNN imputation.
            max_missing_ratio: Maximum ratio of missing values allowed for a column. Columns with more missing values will be dropped.
            config: Configuration dictionary for the imputer.
        """
        super().__init__(columns, config)
        
        # Validate strategies
        if numeric_strategy not in self.STRATEGIES['numeric']:
            raise ValueError(f"Invalid numeric strategy: {numeric_strategy}. Must be one of {self.STRATEGIES['numeric']}")
        if categorical_strategy not in self.STRATEGIES['categorical']:
            raise ValueError(f"Invalid categorical strategy: {categorical_strategy}. Must be one of {self.STRATEGIES['categorical']}")
        
        self.numeric_strategy = numeric_strategy
        self.categorical_strategy = categorical_strategy
        self.constant_value = constant_value
        self.knn_neighbors = knn_neighbors
        self.max_missing_ratio = max_missing_ratio
        
        # Imputers for different column types
        self._numeric_imputer = None
        self._categorical_imputer = None
        self._columns_to_drop = []
    
    def _select_columns(self, data: pd.DataFrame) -> List[str]:
        """
        Select columns with missing values.
        
        Args:
            data: Input data.
            
        Returns:
            List of column names with missing values.
        """
        return [col for col in data.columns if data[col].isna().any()]
    
    def fit(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> 'MissingValueImputer':
        """
        Fit the missing value imputer to the data.
        
        Args:
            data: Input data to fit the imputer.
            **kwargs: Additional keyword arguments.
            
        Returns:
            self: The fitted imputer.
        """
        data = self._validate_input(data)
        self._fitted_columns = self._get_columns(data)
        
        # Get column types
        column_types = get_column_types(data)
        
        # Identify columns to drop (too many missing values)
        self._columns_to_drop = []
        for col in self._fitted_columns:
            missing_ratio = data[col].isna().mean()
            if missing_ratio > self.max_missing_ratio:
                self._columns_to_drop.append(col)
        
        # Remove columns to drop from fitted columns
        self._fitted_columns = [col for col in self._fitted_columns if col not in self._columns_to_drop]
        
        # Separate numeric and categorical columns
        numeric_columns = [col for col in self._fitted_columns if col in column_types['numeric']]
        categorical_columns = [col for col in self._fitted_columns if col in column_types['categorical']]
        
        # Fit numeric imputer
        if numeric_columns:
            if self.numeric_strategy == 'knn':
                self._numeric_imputer = KNNImputer(n_neighbors=self.knn_neighbors)
                # KNN requires all numeric data, so we fit on all numeric columns
                numeric_data = data[numeric_columns].copy()
                self._numeric_imputer.fit(numeric_data)
            else:
                self._numeric_imputer = SimpleImputer(
                    strategy=self.numeric_strategy if self.numeric_strategy != 'constant' else 'constant',
                    fill_value=self.constant_value
                )
                numeric_data = data[numeric_columns].copy()
                self._numeric_imputer.fit(numeric_data)
        
        # Fit categorical imputer
        if categorical_columns:
            self._categorical_imputer = SimpleImputer(
                strategy=self.categorical_strategy if self.categorical_strategy != 'constant' else 'constant',
                fill_value=self.constant_value
            )
            # Convert categorical data to string for imputation
            categorical_data = data[categorical_columns].astype(str)
            self._categorical_imputer.fit(categorical_data)
        
        self._is_fitted = True
        return self
    
    def transform(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> pd.DataFrame:
        """
        Impute missing values in the data.
        
        Args:
            data: Input data to impute.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Data with imputed values.
        """
        self._check_is_fitted()
        data = self._validate_input(data).copy()
        
        # Drop columns with too many missing values
        for col in self._columns_to_drop:
            if col in data.columns:
                data[col] = np.nan
        
        # Get column types
        column_types = get_column_types(data)
        
        # Separate numeric and categorical columns
        numeric_columns = [col for col in self._fitted_columns if col in column_types['numeric'] and col in data.columns]
        categorical_columns = [col for col in self._fitted_columns if col in column_types['categorical'] and col in data.columns]
        
        # Impute numeric columns
        if numeric_columns and self._numeric_imputer:
            numeric_data = data[numeric_columns].copy()
            imputed_numeric = self._numeric_imputer.transform(numeric_data)
            for i, col in enumerate(numeric_columns):
                data[col] = imputed_numeric[:, i]
        
        # Impute categorical columns
        if categorical_columns and self._categorical_imputer:
            # Convert categorical data to string for imputation
            categorical_data = data[categorical_columns].astype(str)
            imputed_categorical = self._categorical_imputer.transform(categorical_data)
            for i, col in enumerate(categorical_columns):
                # Convert back to original dtype if possible
                original_dtype = data[col].dtype
                try:
                    data[col] = pd.Series(imputed_categorical[:, i], index=data.index).astype(original_dtype)
                except (ValueError, TypeError):
                    data[col] = pd.Series(imputed_categorical[:, i], index=data.index)
        
        return data
