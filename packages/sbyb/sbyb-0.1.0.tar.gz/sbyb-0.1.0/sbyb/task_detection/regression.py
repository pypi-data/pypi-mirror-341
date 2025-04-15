"""
Regression task detection for SBYB.

This module provides specialized components for detecting regression tasks.
"""

from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from scipy import stats

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import TaskDetectionError


class RegressionDetector(SBYBComponent):
    """
    Regression task detection component.
    
    This component specializes in detecting regression tasks.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the regression detector.
        
        Args:
            config: Configuration dictionary for the detector.
        """
        super().__init__(config)
    
    def detect(self, data: pd.DataFrame, target: Union[str, int]) -> Dict[str, Any]:
        """
        Detect if the data represents a regression task.
        
        Args:
            data: Input data.
            target: Target variable name or index.
            
        Returns:
            Dictionary with detection results:
                - is_regression: Whether the task is regression
                - confidence: Confidence score for the detection
                - details: Additional details about the detection
        """
        # Extract target variable
        if isinstance(target, int):
            y = data.iloc[:, target]
            target_name = data.columns[target]
        else:
            y = data[target]
            target_name = target
        
        # Check if the target is numeric
        is_numeric = pd.api.types.is_numeric_dtype(y.dtype)
        
        if not is_numeric:
            return {
                'is_regression': False,
                'confidence': 0.9,
                'details': {
                    'reason': 'Target variable is not numeric',
                    'dtype': str(y.dtype)
                }
            }
        
        # Check the number of unique values
        n_unique = y.nunique()
        
        # If there are very few unique values, it's likely classification, not regression
        if n_unique <= min(10, len(y) * 0.05):
            return {
                'is_regression': False,
                'confidence': 0.8,
                'details': {
                    'reason': 'Target variable has too few unique values for regression',
                    'n_unique': n_unique,
                    'threshold': min(10, len(y) * 0.05)
                }
            }
        
        # Check distribution characteristics
        # Regression targets often have a continuous distribution
        try:
            # Calculate skewness and kurtosis
            skewness = stats.skew(y.dropna())
            kurtosis = stats.kurtosis(y.dropna())
            
            # Calculate additional statistics
            mean = y.mean()
            median = y.median()
            std = y.std()
            min_val = y.min()
            max_val = y.max()
            
            # Calculate confidence based on distribution characteristics
            # Higher confidence if the distribution is somewhat normal
            confidence = 0.9
            if abs(skewness) > 2 or abs(kurtosis) > 7:
                confidence = 0.8  # Less confident if highly skewed or heavy-tailed
            
            return {
                'is_regression': True,
                'confidence': confidence,
                'details': {
                    'target_column': target_name,
                    'n_unique': n_unique,
                    'distribution': {
                        'mean': mean,
                        'median': median,
                        'std': std,
                        'min': min_val,
                        'max': max_val,
                        'skewness': skewness,
                        'kurtosis': kurtosis
                    }
                }
            }
        except Exception as e:
            # If statistical analysis fails, still return a result based on basic checks
            return {
                'is_regression': True,
                'confidence': 0.7,
                'details': {
                    'target_column': target_name,
                    'n_unique': n_unique,
                    'note': 'Statistical analysis failed, confidence reduced',
                    'error': str(e)
                }
            }
    
    def suggest_transformations(self, data: pd.DataFrame, target: Union[str, int]) -> Dict[str, Any]:
        """
        Suggest transformations for the target variable to improve regression performance.
        
        Args:
            data: Input data.
            target: Target variable name or index.
            
        Returns:
            Dictionary with suggested transformations and their effects.
        """
        # Extract target variable
        if isinstance(target, int):
            y = data.iloc[:, target]
        else:
            y = data[target]
        
        # Skip if not numeric
        if not pd.api.types.is_numeric_dtype(y.dtype):
            return {'suggested_transformations': []}
        
        # Calculate skewness of original data
        original_skewness = stats.skew(y.dropna())
        
        suggestions = []
        
        # Try log transformation (for positive data)
        if y.min() > 0:
            log_y = np.log(y)
            log_skewness = stats.skew(log_y.dropna())
            
            if abs(log_skewness) < abs(original_skewness):
                suggestions.append({
                    'transformation': 'log',
                    'formula': 'np.log(y)',
                    'original_skewness': original_skewness,
                    'transformed_skewness': log_skewness,
                    'improvement': abs(original_skewness) - abs(log_skewness)
                })
        
        # Try square root transformation (for positive data)
        if y.min() >= 0:
            sqrt_y = np.sqrt(y)
            sqrt_skewness = stats.skew(sqrt_y.dropna())
            
            if abs(sqrt_skewness) < abs(original_skewness):
                suggestions.append({
                    'transformation': 'square_root',
                    'formula': 'np.sqrt(y)',
                    'original_skewness': original_skewness,
                    'transformed_skewness': sqrt_skewness,
                    'improvement': abs(original_skewness) - abs(sqrt_skewness)
                })
        
        # Try box-cox transformation (for positive data)
        if y.min() > 0:
            try:
                boxcox_y, lambda_param = stats.boxcox(y.dropna())
                boxcox_skewness = stats.skew(boxcox_y)
                
                if abs(boxcox_skewness) < abs(original_skewness):
                    suggestions.append({
                        'transformation': 'box_cox',
                        'formula': f'stats.boxcox(y, lambda={lambda_param:.4f})',
                        'lambda': lambda_param,
                        'original_skewness': original_skewness,
                        'transformed_skewness': boxcox_skewness,
                        'improvement': abs(original_skewness) - abs(boxcox_skewness)
                    })
            except:
                pass  # Box-Cox can fail for various reasons
        
        # Sort suggestions by improvement
        suggestions.sort(key=lambda x: x['improvement'], reverse=True)
        
        return {
            'original_skewness': original_skewness,
            'suggested_transformations': suggestions
        }
