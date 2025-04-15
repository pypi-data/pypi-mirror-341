"""
Utility functions for SBYB.

This module provides utility functions used throughout the SBYB library.
"""

import os
import pickle
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def load_data(data_source: Union[str, pd.DataFrame, np.ndarray]) -> pd.DataFrame:
    """
    Load data from various sources into a pandas DataFrame.
    
    Args:
        data_source: Data source, which can be:
            - Path to a CSV, Excel, or JSON file
            - pandas DataFrame
            - numpy array
            
    Returns:
        Loaded data as a pandas DataFrame.
        
    Raises:
        ValueError: If the data source is invalid or cannot be loaded.
    """
    if isinstance(data_source, pd.DataFrame):
        return data_source
    
    if isinstance(data_source, np.ndarray):
        return pd.DataFrame(data_source)
    
    if isinstance(data_source, str):
        file_extension = os.path.splitext(data_source)[1].lower()
        
        if file_extension == '.csv':
            return pd.read_csv(data_source)
        elif file_extension in ['.xls', '.xlsx']:
            return pd.read_excel(data_source)
        elif file_extension == '.json':
            return pd.read_json(data_source)
        elif file_extension == '.pkl':
            with open(data_source, 'rb') as f:
                return pickle.load(f)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
    
    raise ValueError(f"Unsupported data source type: {type(data_source)}")


def split_data(data: pd.DataFrame, target: Union[str, int], 
               test_size: float = 0.2, random_state: Optional[int] = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split data into training and testing sets.
    
    Args:
        data: Input data.
        target: Target variable name or column index.
        test_size: Proportion of the data to include in the test split.
        random_state: Random seed for reproducibility.
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    if isinstance(target, int):
        X = data.drop(data.columns[target], axis=1)
        y = data.iloc[:, target]
    else:
        X = data.drop(target, axis=1)
        y = data[target]
    
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def get_column_types(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Categorize DataFrame columns by data type.
    
    Args:
        df: Input DataFrame.
        
    Returns:
        Dictionary mapping data type categories to lists of column names.
    """
    column_types = {
        'numeric': [],
        'categorical': [],
        'datetime': [],
        'text': [],
        'boolean': [],
        'other': []
    }
    
    for col in df.columns:
        dtype = df[col].dtype
        
        # Check for numeric columns
        if np.issubdtype(dtype, np.number):
            column_types['numeric'].append(col)
        
        # Check for boolean columns
        elif dtype == bool:
            column_types['boolean'].append(col)
        
        # Check for datetime columns
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            column_types['datetime'].append(col)
        
        # Check for categorical or text columns
        elif pd.api.types.is_string_dtype(dtype) or pd.api.types.is_categorical_dtype(dtype):
            # Heuristic: if the number of unique values is small relative to the dataframe size,
            # it's likely categorical, otherwise it's text
            n_unique = df[col].nunique()
            if n_unique < min(50, len(df) * 0.1):
                column_types['categorical'].append(col)
            else:
                column_types['text'].append(col)
        
        # Other types
        else:
            column_types['other'].append(col)
    
    return column_types


def generate_timestamp() -> str:
    """
    Generate a timestamp string.
    
    Returns:
        Timestamp string in the format 'YYYYMMDD_HHMMSS'.
    """
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def save_model(model: Any, path: str) -> None:
    """
    Save a model to disk.
    
    Args:
        model: Model to save.
        path: Path to save the model.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(model, f)


def load_model(path: str) -> Any:
    """
    Load a model from disk.
    
    Args:
        path: Path to the saved model.
        
    Returns:
        Loaded model.
    """
    with open(path, 'rb') as f:
        return pickle.load(f)


def is_classification_target(y: pd.Series) -> bool:
    """
    Determine if a target variable is for a classification task.
    
    Args:
        y: Target variable.
        
    Returns:
        True if the target is for classification, False otherwise.
    """
    # If the target is categorical or has a small number of unique values, it's likely classification
    if pd.api.types.is_categorical_dtype(y.dtype) or pd.api.types.is_string_dtype(y.dtype):
        return True
    
    # If the target is numeric but has a small number of unique values, it's likely classification
    if pd.api.types.is_numeric_dtype(y.dtype):
        n_unique = y.nunique()
        if n_unique < min(10, len(y) * 0.05):
            return True
    
    return False


def is_regression_target(y: pd.Series) -> bool:
    """
    Determine if a target variable is for a regression task.
    
    Args:
        y: Target variable.
        
    Returns:
        True if the target is for regression, False otherwise.
    """
    # If the target is numeric and has many unique values, it's likely regression
    if pd.api.types.is_numeric_dtype(y.dtype):
        n_unique = y.nunique()
        if n_unique >= min(10, len(y) * 0.05):
            return True
    
    return False
