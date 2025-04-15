"""
Data cleaning utilities for SBYB.

This module provides components for cleaning and validating data.
"""

from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd

from sbyb.core.exceptions import PreprocessingError
from sbyb.preprocessing.base import ColumnBasedPreprocessor


class DataCleaner(ColumnBasedPreprocessor):
    """
    Data cleaner component for handling various data quality issues.
    
    This component performs the following cleaning operations:
    - Removes duplicate rows
    - Handles inconsistent data types
    - Removes or flags invalid values
    - Standardizes text data (case, whitespace, etc.)
    """
    
    def __init__(self, columns: Optional[List[str]] = None, 
                 remove_duplicates: bool = True,
                 fix_data_types: bool = True,
                 handle_invalid_values: bool = True,
                 standardize_text: bool = True,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the data cleaner.
        
        Args:
            columns: List of column names to clean. If None, all columns will be processed.
            remove_duplicates: Whether to remove duplicate rows.
            fix_data_types: Whether to fix inconsistent data types.
            handle_invalid_values: Whether to handle invalid values.
            standardize_text: Whether to standardize text data.
            config: Configuration dictionary for the cleaner.
        """
        super().__init__(columns, config)
        self.remove_duplicates = remove_duplicates
        self.fix_data_types = fix_data_types
        self.handle_invalid_values = handle_invalid_values
        self.standardize_text = standardize_text
        self._column_dtypes = {}
    
    def _select_columns(self, data: pd.DataFrame) -> List[str]:
        """
        Select all columns for cleaning.
        
        Args:
            data: Input data.
            
        Returns:
            List of all column names.
        """
        return list(data.columns)
    
    def fit(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> 'DataCleaner':
        """
        Fit the data cleaner to the data.
        
        Args:
            data: Input data to fit the cleaner.
            **kwargs: Additional keyword arguments.
            
        Returns:
            self: The fitted cleaner.
        """
        data = self._validate_input(data)
        self._fitted_columns = self._get_columns(data)
        
        # Store the data types of columns for later use
        if self.fix_data_types:
            for col in self._fitted_columns:
                self._column_dtypes[col] = data[col].dtype
        
        self._is_fitted = True
        return self
    
    def transform(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> pd.DataFrame:
        """
        Clean the data.
        
        Args:
            data: Input data to clean.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Cleaned data.
        """
        self._check_is_fitted()
        data = self._validate_input(data)
        
        # Remove duplicate rows
        if self.remove_duplicates:
            data = data.drop_duplicates().reset_index(drop=True)
        
        # Process each column
        for col in self._fitted_columns:
            if col not in data.columns:
                continue
            
            # Fix data types
            if self.fix_data_types and col in self._column_dtypes:
                data[col] = self._fix_data_type(data[col], self._column_dtypes[col])
            
            # Handle invalid values
            if self.handle_invalid_values:
                data[col] = self._handle_invalid_values(data[col])
            
            # Standardize text data
            if self.standardize_text and pd.api.types.is_string_dtype(data[col].dtype):
                data[col] = self._standardize_text(data[col])
        
        return data
    
    def _fix_data_type(self, series: pd.Series, target_dtype: np.dtype) -> pd.Series:
        """
        Fix the data type of a series.
        
        Args:
            series: Input series.
            target_dtype: Target data type.
            
        Returns:
            Series with fixed data type.
        """
        try:
            # Handle special case for datetime
            if pd.api.types.is_datetime64_any_dtype(target_dtype):
                return pd.to_datetime(series, errors='coerce')
            
            # Handle special case for categorical
            if pd.api.types.is_categorical_dtype(target_dtype):
                return series.astype('category')
            
            # General case
            return series.astype(target_dtype)
        except (ValueError, TypeError):
            # If conversion fails, return the original series
            return series
    
    def _handle_invalid_values(self, series: pd.Series) -> pd.Series:
        """
        Handle invalid values in a series.
        
        Args:
            series: Input series.
            
        Returns:
            Series with invalid values handled.
        """
        # Handle NaN, Inf, -Inf in numeric data
        if pd.api.types.is_numeric_dtype(series.dtype):
            return series.replace([np.inf, -np.inf], np.nan)
        
        # Handle empty strings in string data
        if pd.api.types.is_string_dtype(series.dtype):
            return series.replace('', np.nan)
        
        return series
    
    def _standardize_text(self, series: pd.Series) -> pd.Series:
        """
        Standardize text data in a series.
        
        Args:
            series: Input series.
            
        Returns:
            Series with standardized text.
        """
        # Convert to string type if not already
        if not pd.api.types.is_string_dtype(series.dtype):
            series = series.astype(str)
        
        # Trim whitespace
        series = series.str.strip()
        
        # Replace multiple spaces with a single space
        series = series.str.replace(r'\s+', ' ', regex=True)
        
        return series
