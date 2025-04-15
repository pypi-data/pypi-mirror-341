"""
Base preprocessor classes for SBYB.

This module defines the base classes for data preprocessing components.
"""

from abc import abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from sbyb.core.base import DataProcessor, SBYBComponent
from sbyb.core.exceptions import NotFittedError, PreprocessingError


class BasePreprocessor(DataProcessor):
    """Base class for all preprocessors in SBYB."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the preprocessor.
        
        Args:
            config: Configuration dictionary for the preprocessor.
        """
        super().__init__(config)
        self._is_fitted = False
    
    @property
    def is_fitted(self) -> bool:
        """Check if the preprocessor is fitted."""
        return self._is_fitted
    
    def _check_is_fitted(self) -> None:
        """
        Check if the preprocessor is fitted.
        
        Raises:
            NotFittedError: If the preprocessor is not fitted.
        """
        if not self._is_fitted:
            raise NotFittedError(f"{self.__class__.__name__} is not fitted yet. Call 'fit' before using this method.")
    
    def _validate_input(self, data: Union[pd.DataFrame, np.ndarray]) -> pd.DataFrame:
        """
        Validate and convert input data to pandas DataFrame.
        
        Args:
            data: Input data.
            
        Returns:
            Validated data as pandas DataFrame.
            
        Raises:
            PreprocessingError: If the data is invalid.
        """
        if isinstance(data, np.ndarray):
            return pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            return data
        else:
            raise PreprocessingError(f"Unsupported data type: {type(data)}. Expected pandas DataFrame or numpy array.")
    
    @abstractmethod
    def fit(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> 'BasePreprocessor':
        """
        Fit the preprocessor to the data.
        
        Args:
            data: Input data to fit the preprocessor.
            **kwargs: Additional keyword arguments.
            
        Returns:
            self: The fitted preprocessor.
        """
        pass
    
    @abstractmethod
    def transform(self, data: Union[pd.DataFrame, np.ndarray], **kwargs) -> pd.DataFrame:
        """
        Transform the data using the fitted preprocessor.
        
        Args:
            data: Input data to transform.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Transformed data.
        """
        pass


class ColumnBasedPreprocessor(BasePreprocessor):
    """Base class for preprocessors that operate on specific columns."""
    
    def __init__(self, columns: Optional[List[str]] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the column-based preprocessor.
        
        Args:
            columns: List of column names to process. If None, all suitable columns will be processed.
            config: Configuration dictionary for the preprocessor.
        """
        super().__init__(config)
        self.columns = columns
        self._fitted_columns: List[str] = []
    
    def _get_columns(self, data: pd.DataFrame) -> List[str]:
        """
        Get the columns to process.
        
        Args:
            data: Input data.
            
        Returns:
            List of column names to process.
        """
        if self.columns is not None:
            # Verify that all specified columns exist in the data
            missing_columns = set(self.columns) - set(data.columns)
            if missing_columns:
                raise PreprocessingError(f"Columns {missing_columns} not found in the data.")
            return self.columns
        
        # If no columns are specified, select columns based on the preprocessor's criteria
        return self._select_columns(data)
    
    @abstractmethod
    def _select_columns(self, data: pd.DataFrame) -> List[str]:
        """
        Select columns to process based on the preprocessor's criteria.
        
        Args:
            data: Input data.
            
        Returns:
            List of column names to process.
        """
        pass
