"""
Feature engineering for SBYB.

This module provides components for generating new features from existing ones.
"""

from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import PolynomialFeatures

from sbyb.core.exceptions import PreprocessingError
from sbyb.core.utils import get_column_types
from sbyb.preprocessing.base import ColumnBasedPreprocessor


class FeatureEngineer(ColumnBasedPreprocessor):
    """
    Feature engineering component.
    
    This component generates new features from existing ones using various methods.
    """
    
    FEATURE_TYPES = ['polynomial', 'interaction', 'pca', 'datetime', 'statistical']
    
    def __init__(self, columns: Optional[List[str]] = None,
                 feature_types: Optional[List[str]] = None,
                 polynomial_degree: int = 2,
                 pca_components: Optional[int] = None,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the feature engineer.
        
        Args:
            columns: List of column names to use for feature engineering. If None, appropriate columns will be selected.
            feature_types: Types of features to generate. If None, all types will be used where appropriate.
            polynomial_degree: Degree of polynomial features.
            pca_components: Number of PCA components. If None, min(n_samples, n_features) will be used.
            config: Configuration dictionary for the feature engineer.
        """
        super().__init__(columns, config)
        
        # Validate parameters
        if feature_types is not None:
            for ft in feature_types:
                if ft not in self.FEATURE_TYPES:
                    raise ValueError(f"Invalid feature type: {ft}. Must be one of {self.FEATURE_TYPES}")
        
        self.feature_types = feature_types or self.FEATURE_TYPES
        self.polynomial_degree = polynomial_degree
        self.pca_components = pca_components
        
        # Feature generators
        self._poly_features = None
        self._pca = None
        self._datetime_columns = []
        self._numeric_columns = []
    
    def _select_columns(self, data: pd.DataFrame) -> List[str]:
        """
        Select appropriate columns for feature engineering.
        
        Args:
            data: Input data.
            
        Returns:
            List of column names.
        """
        column_types = get_column_types(data)
        selected_columns = []
        
        # Select columns based on feature types
        if 'polynomial' in self.feature_types or 'interaction' in self.feature_types:
            selected_columns.extend(column_types['numeric'])
        
        if 'pca' in self.feature_types:
            selected_columns.extend(column_types['numeric'])
        
        if 'datetime' in self.feature_types:
            selected_columns.extend(column_types['datetime'])
        
        if 'statistical' in self.feature_types:
            selected_columns.extend(column_types['numeric'])
        
        return list(set(selected_columns))  # Remove duplicates
    
    def fit(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> 'FeatureEngineer':
        """
        Fit the feature engineer to the data.
        
        Args:
            data: Input data to fit the feature engineer.
            **kwargs: Additional keyword arguments.
            
        Returns:
            self: The fitted feature engineer.
        """
        data = self._validate_input(data)
        self._fitted_columns = self._get_columns(data)
        
        # Get column types
        column_types = get_column_types(data)
        
        # Store column types for later use
        self._datetime_columns = [col for col in self._fitted_columns if col in column_types['datetime']]
        self._numeric_columns = [col for col in self._fitted_columns if col in column_types['numeric']]
        
        # Fit polynomial features
        if ('polynomial' in self.feature_types or 'interaction' in self.feature_types) and self._numeric_columns:
            interaction_only = 'polynomial' not in self.feature_types
            self._poly_features = PolynomialFeatures(
                degree=self.polynomial_degree,
                interaction_only=interaction_only,
                include_bias=False
            )
            self._poly_features.fit(data[self._numeric_columns])
        
        # Fit PCA
        if 'pca' in self.feature_types and self._numeric_columns:
            n_components = self.pca_components
            if n_components is None:
                n_components = min(len(data), len(self._numeric_columns))
            
            self._pca = PCA(n_components=n_components)
            self._pca.fit(data[self._numeric_columns])
        
        self._is_fitted = True
        return self
    
    def transform(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> pd.DataFrame:
        """
        Generate new features from the data.
        
        Args:
            data: Input data to transform.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Data with new features.
        """
        self._check_is_fitted()
        data = self._validate_input(data).copy()
        
        # Generate polynomial/interaction features
        if self._poly_features is not None and all(col in data.columns for col in self._numeric_columns):
            poly_features = self._poly_features.transform(data[self._numeric_columns])
            feature_names = self._poly_features.get_feature_names_out(self._numeric_columns)
            
            # Skip the first n_features columns as they are the original features
            for i, name in enumerate(feature_names[len(self._numeric_columns):], len(self._numeric_columns)):
                data[f"poly_{name}"] = poly_features[:, i]
        
        # Generate PCA features
        if self._pca is not None and all(col in data.columns for col in self._numeric_columns):
            pca_features = self._pca.transform(data[self._numeric_columns])
            for i in range(pca_features.shape[1]):
                data[f"pca_component_{i+1}"] = pca_features[:, i]
        
        # Generate datetime features
        if 'datetime' in self.feature_types:
            for col in self._datetime_columns:
                if col in data.columns:
                    # Convert to datetime if not already
                    if not pd.api.types.is_datetime64_any_dtype(data[col].dtype):
                        data[col] = pd.to_datetime(data[col], errors='coerce')
                    
                    # Extract datetime components
                    data[f"{col}_year"] = data[col].dt.year
                    data[f"{col}_month"] = data[col].dt.month
                    data[f"{col}_day"] = data[col].dt.day
                    data[f"{col}_dayofweek"] = data[col].dt.dayofweek
                    data[f"{col}_hour"] = data[col].dt.hour
                    data[f"{col}_quarter"] = data[col].dt.quarter
                    data[f"{col}_is_weekend"] = data[col].dt.dayofweek >= 5
        
        # Generate statistical features
        if 'statistical' in self.feature_types and len(self._numeric_columns) >= 2:
            # Calculate mean, std, min, max for each row
            data['stat_mean'] = data[self._numeric_columns].mean(axis=1)
            data['stat_std'] = data[self._numeric_columns].std(axis=1)
            data['stat_min'] = data[self._numeric_columns].min(axis=1)
            data['stat_max'] = data[self._numeric_columns].max(axis=1)
            
            # Calculate differences between consecutive columns
            for i in range(len(self._numeric_columns) - 1):
                col1 = self._numeric_columns[i]
                col2 = self._numeric_columns[i + 1]
                if col1 in data.columns and col2 in data.columns:
                    data[f"diff_{col1}_{col2}"] = data[col1] - data[col2]
        
        return data
