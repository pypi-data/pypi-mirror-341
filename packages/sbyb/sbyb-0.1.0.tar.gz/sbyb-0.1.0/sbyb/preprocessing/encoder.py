"""
Categorical encoding for SBYB.

This module provides components for encoding categorical data.
"""

from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, OrdinalEncoder

from sbyb.core.exceptions import PreprocessingError
from sbyb.core.utils import get_column_types
from sbyb.preprocessing.base import ColumnBasedPreprocessor


class CategoricalEncoder(ColumnBasedPreprocessor):
    """
    Categorical encoding component.
    
    This component encodes categorical variables using various encoding methods.
    """
    
    ENCODING_METHODS = ['onehot', 'label', 'ordinal', 'binary', 'frequency']
    
    def __init__(self, columns: Optional[List[str]] = None,
                 method: str = 'auto',
                 max_categories: int = 20,
                 handle_unknown: str = 'ignore',
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the categorical encoder.
        
        Args:
            columns: List of column names to encode. If None, all categorical columns will be processed.
            method: Encoding method ('onehot', 'label', 'ordinal', 'binary', 'frequency', 'auto').
                If 'auto', the method will be selected based on the number of categories.
            max_categories: Maximum number of categories for one-hot encoding.
            handle_unknown: Strategy for handling unknown categories ('ignore', 'error').
            config: Configuration dictionary for the encoder.
        """
        super().__init__(columns, config)
        
        # Validate parameters
        if method != 'auto' and method not in self.ENCODING_METHODS:
            raise ValueError(f"Invalid encoding method: {method}. Must be one of {self.ENCODING_METHODS} or 'auto'")
        
        self.method = method
        self.max_categories = max_categories
        self.handle_unknown = handle_unknown
        
        # Encoders for each column
        self._encoders = {}
        self._column_methods = {}
        self._category_counts = {}
    
    def _select_columns(self, data: pd.DataFrame) -> List[str]:
        """
        Select categorical columns for encoding.
        
        Args:
            data: Input data.
            
        Returns:
            List of categorical column names.
        """
        column_types = get_column_types(data)
        return column_types['categorical']
    
    def fit(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> 'CategoricalEncoder':
        """
        Fit the categorical encoder to the data.
        
        Args:
            data: Input data to fit the encoder.
            **kwargs: Additional keyword arguments.
            
        Returns:
            self: The fitted encoder.
        """
        data = self._validate_input(data)
        self._fitted_columns = self._get_columns(data)
        
        for col in self._fitted_columns:
            # Count categories
            n_categories = data[col].nunique()
            self._category_counts[col] = n_categories
            
            # Select encoding method
            if self.method == 'auto':
                if n_categories <= 2:
                    method = 'label'  # Binary classification
                elif n_categories <= self.max_categories:
                    method = 'onehot'  # Reasonable number of categories
                else:
                    method = 'label'  # Too many categories for one-hot
            else:
                method = self.method
            
            self._column_methods[col] = method
            
            # Create and fit encoder
            if method == 'onehot':
                encoder = OneHotEncoder(sparse=False, handle_unknown=self.handle_unknown)
                # Reshape for sklearn API
                encoder.fit(data[[col]])
            elif method == 'label':
                encoder = LabelEncoder()
                encoder.fit(data[col].astype(str).fillna('missing'))
            elif method == 'ordinal':
                encoder = OrdinalEncoder(handle_unknown=self.handle_unknown)
                encoder.fit(data[[col]].astype(str).fillna('missing'))
            elif method == 'binary':
                # Binary encoding is a combination of ordinal encoding and binary representation
                ordinal_encoder = OrdinalEncoder(handle_unknown=self.handle_unknown)
                ordinal_encoder.fit(data[[col]].astype(str).fillna('missing'))
                encoder = {'ordinal': ordinal_encoder, 'n_categories': n_categories}
            elif method == 'frequency':
                # Frequency encoding replaces categories with their frequencies
                value_counts = data[col].value_counts(normalize=True)
                encoder = {'mapping': value_counts}
            
            self._encoders[col] = encoder
        
        self._is_fitted = True
        return self
    
    def transform(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> pd.DataFrame:
        """
        Encode categorical columns in the data.
        
        Args:
            data: Input data to encode.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Data with encoded categorical columns.
        """
        self._check_is_fitted()
        data = self._validate_input(data).copy()
        
        for col in self._fitted_columns:
            if col not in data.columns:
                continue
            
            method = self._column_methods[col]
            encoder = self._encoders[col]
            
            if method == 'onehot':
                # Apply one-hot encoding
                encoded = encoder.transform(data[[col]])
                # Create new columns for each category
                categories = encoder.categories_[0]
                for i, category in enumerate(categories):
                    data[f"{col}_{category}"] = encoded[:, i]
                # Drop original column
                data = data.drop(col, axis=1)
            
            elif method == 'label':
                # Apply label encoding
                data[col] = encoder.transform(data[col].astype(str).fillna('missing'))
            
            elif method == 'ordinal':
                # Apply ordinal encoding
                data[col] = encoder.transform(data[[col]].astype(str).fillna('missing')).flatten()
            
            elif method == 'binary':
                # Apply binary encoding
                ordinal_encoder = encoder['ordinal']
                n_categories = encoder['n_categories']
                
                # First apply ordinal encoding
                ordinal_values = ordinal_encoder.transform(data[[col]].astype(str).fillna('missing')).flatten()
                
                # Then convert to binary representation
                n_bits = int(np.ceil(np.log2(n_categories)))
                for bit in range(n_bits):
                    data[f"{col}_bit{bit}"] = ((ordinal_values >> bit) & 1).astype(int)
                
                # Drop original column
                data = data.drop(col, axis=1)
            
            elif method == 'frequency':
                # Apply frequency encoding
                mapping = encoder['mapping']
                data[col] = data[col].map(mapping).fillna(0)
        
        return data
