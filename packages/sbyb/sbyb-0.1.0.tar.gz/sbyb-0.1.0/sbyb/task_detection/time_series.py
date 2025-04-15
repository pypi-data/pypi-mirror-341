"""
Time series task detection for SBYB.

This module provides specialized components for detecting time series tasks.
"""

from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from scipy import stats

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import TaskDetectionError


class TimeSeriesDetector(SBYBComponent):
    """
    Time series task detection component.
    
    This component specializes in detecting time series tasks.
    """
    
    TIME_SERIES_TASKS = [
        'forecasting',
        'classification',
        'anomaly_detection',
        'clustering'
    ]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the time series detector.
        
        Args:
            config: Configuration dictionary for the detector.
        """
        super().__init__(config)
    
    def detect(self, data: pd.DataFrame, date_column: Optional[str] = None, 
               target: Optional[Union[str, int]] = None) -> Dict[str, Any]:
        """
        Detect if the data represents a time series task and identify the specific task type.
        
        Args:
            data: Input data.
            date_column: Column name containing date/time data. If None, will try to detect.
            target: Target variable name or index (if applicable).
            
        Returns:
            Dictionary with detection results:
                - is_time_series: Whether the task is a time series task
                - task_type: Specific time series task type
                - confidence: Confidence score for the detection
                - details: Additional details about the detection
        """
        # If date_column is not specified, try to find it
        if date_column is None:
            date_column = self._find_date_column(data)
            
            if date_column is None:
                return {
                    'is_time_series': False,
                    'confidence': 0.8,
                    'details': {
                        'reason': 'No suitable date/time column found in the DataFrame'
                    }
                }
        
        # Verify that the date column exists
        if date_column not in data.columns:
            return {
                'is_time_series': False,
                'confidence': 0.9,
                'details': {
                    'reason': f'Specified date column "{date_column}" not found in the DataFrame'
                }
            }
        
        # Convert to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(data[date_column].dtype):
            try:
                data[date_column] = pd.to_datetime(data[date_column])
            except:
                return {
                    'is_time_series': False,
                    'confidence': 0.9,
                    'details': {
                        'reason': f'Could not convert column "{date_column}" to datetime'
                    }
                }
        
        # Check if the data is sorted by date
        is_sorted = data[date_column].is_monotonic_increasing
        
        # Check for regular time intervals
        if len(data) > 1:
            time_diffs = data[date_column].diff().dropna()
            most_common_diff = time_diffs.mode().iloc[0]
            regular_interval_ratio = (time_diffs == most_common_diff).mean()
            has_regular_intervals = regular_interval_ratio > 0.7
        else:
            has_regular_intervals = False
        
        # If target is specified, determine the task type
        if target is not None:
            # Extract target variable
            if isinstance(target, int):
                y = data.iloc[:, target]
                target_name = data.columns[target]
            else:
                y = data[target]
                target_name = target
            
            # Check if it's classification or regression
            is_categorical = pd.api.types.is_categorical_dtype(y.dtype) or pd.api.types.is_string_dtype(y.dtype)
            n_unique = y.nunique()
            is_classification = is_categorical or (pd.api.types.is_numeric_dtype(y.dtype) and n_unique <= min(10, len(y) * 0.05))
            
            if is_classification:
                return {
                    'is_time_series': True,
                    'task_type': 'classification',
                    'confidence': 0.9,
                    'details': {
                        'date_column': date_column,
                        'target_column': target_name,
                        'n_classes': n_unique,
                        'is_sorted': is_sorted,
                        'has_regular_intervals': has_regular_intervals,
                        'regular_interval_ratio': regular_interval_ratio if 'regular_interval_ratio' in locals() else None
                    }
                }
            else:
                # For regression targets, it's likely forecasting
                return {
                    'is_time_series': True,
                    'task_type': 'forecasting',
                    'confidence': 0.9,
                    'details': {
                        'date_column': date_column,
                        'target_column': target_name,
                        'is_sorted': is_sorted,
                        'has_regular_intervals': has_regular_intervals,
                        'regular_interval_ratio': regular_interval_ratio if 'regular_interval_ratio' in locals() else None
                    }
                }
        
        # If no target is specified, try to guess the task type
        # Look for columns that might be targets
        numeric_columns = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col].dtype) and col != date_column]
        
        if not numeric_columns:
            # No numeric columns to forecast
            return {
                'is_time_series': True,
                'task_type': 'clustering',  # Default to clustering if no clear target
                'confidence': 0.6,
                'details': {
                    'date_column': date_column,
                    'is_sorted': is_sorted,
                    'has_regular_intervals': has_regular_intervals,
                    'regular_interval_ratio': regular_interval_ratio if 'regular_interval_ratio' in locals() else None,
                    'reason': 'No numeric columns found for forecasting'
                }
            }
        
        # Check for anomaly patterns
        has_anomaly_columns = any(col.lower() in ['anomaly', 'outlier', 'alert', 'alarm'] for col in data.columns)
        
        if has_anomaly_columns:
            return {
                'is_time_series': True,
                'task_type': 'anomaly_detection',
                'confidence': 0.8,
                'details': {
                    'date_column': date_column,
                    'is_sorted': is_sorted,
                    'has_regular_intervals': has_regular_intervals,
                    'regular_interval_ratio': regular_interval_ratio if 'regular_interval_ratio' in locals() else None,
                    'reason': 'Found columns suggesting anomaly detection'
                }
            }
        
        # Default to forecasting as the most common time series task
        return {
            'is_time_series': True,
            'task_type': 'forecasting',
            'confidence': 0.7,
            'details': {
                'date_column': date_column,
                'potential_target_columns': numeric_columns,
                'is_sorted': is_sorted,
                'has_regular_intervals': has_regular_intervals,
                'regular_interval_ratio': regular_interval_ratio if 'regular_interval_ratio' in locals() else None,
                'reason': 'Defaulting to forecasting as the most common time series task'
            }
        }
    
    def _find_date_column(self, data: pd.DataFrame) -> Optional[str]:
        """
        Find the most likely date/time column in a DataFrame.
        
        Args:
            data: Input DataFrame.
            
        Returns:
            Name of the most likely date/time column, or None if no suitable column is found.
        """
        # First, check for columns with datetime dtype
        datetime_columns = [col for col in data.columns if pd.api.types.is_datetime64_any_dtype(data[col].dtype)]
        
        if datetime_columns:
            # If multiple datetime columns, prefer the one with the name suggesting a timestamp
            for col in datetime_columns:
                if any(term in col.lower() for term in ['time', 'date', 'timestamp', 'dt', 'period']):
                    return col
            # Otherwise, return the first datetime column
            return datetime_columns[0]
        
        # If no datetime columns, try to convert string or object columns to datetime
        string_columns = [col for col in data.columns if pd.api.types.is_string_dtype(data[col].dtype) or 
                          pd.api.types.is_object_dtype(data[col].dtype)]
        
        for col in string_columns:
            # Check if the column name suggests a date
            if any(term in col.lower() for term in ['time', 'date', 'timestamp', 'dt', 'period']):
                try:
                    pd.to_datetime(data[col])
                    return col
                except:
                    continue
        
        # If no columns with date-like names, try all string/object columns
        for col in string_columns:
            try:
                pd.to_datetime(data[col])
                return col
            except:
                continue
        
        return None
    
    def suggest_preprocessing(self, data: pd.DataFrame, date_column: Optional[str] = None) -> Dict[str, Any]:
        """
        Suggest preprocessing steps for the time series data.
        
        Args:
            data: Input data.
            date_column: Column name containing date/time data. If None, will try to detect.
            
        Returns:
            Dictionary with suggested preprocessing steps.
        """
        # If date_column is not specified, try to find it
        if date_column is None:
            date_column = self._find_date_column(data)
            
            if date_column is None:
                return {
                    'error': 'No suitable date/time column found in the DataFrame'
                }
        
        # Verify that the date column exists
        if date_column not in data.columns:
            return {
                'error': f'Specified date column "{date_column}" not found in the DataFrame'
            }
        
        # Convert to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(data[date_column].dtype):
            try:
                data[date_column] = pd.to_datetime(data[date_column])
            except:
                return {
                    'error': f'Could not convert column "{date_column}" to datetime'
                }
        
        # Check if the data is sorted by date
        is_sorted = data[date_column].is_monotonic_increasing
        
        # Check for regular time intervals
        if len(data) > 1:
            time_diffs = data[date_column].diff().dropna()
            most_common_diff = time_diffs.mode().iloc[0]
            regular_interval_ratio = (time_diffs == most_common_diff).mean()
            has_regular_intervals = regular_interval_ratio > 0.7
        else:
            has_regular_intervals = False
            regular_interval_ratio = None
        
        # Check for missing values
        has_missing_values = data.isnull().any().any()
        
        # Check for multiple time series (if there's a grouping column)
        potential_group_columns = []
        for col in data.columns:
            if col != date_column and data[col].nunique() < min(20, len(data) * 0.1):
                potential_group_columns.append(col)
        
        has_multiple_series = len(potential_group_columns) > 0
        
        # Suggest preprocessing steps
        steps = []
        
        if not is_sorted:
            steps.append('sort_by_date')
        
        if has_missing_values:
            steps.append('handle_missing_values')
        
        if not has_regular_intervals and regular_interval_ratio is not None and regular_interval_ratio < 0.9:
            steps.append('resample_to_regular_intervals')
        
        # Always suggest these steps
        steps.extend([
            'extract_date_features',
            'lag_features',
            'rolling_statistics'
        ])
        
        # Suggest normalization for forecasting
        steps.append('normalize_features')
        
        # Suggest train-test split approach
        if len(data) > 100:
            split_strategy = 'temporal_split'
        else:
            split_strategy = 'cross_validation'
        
        return {
            'suggested_steps': steps,
            'date_features': [
                'year', 'month', 'day', 'dayofweek', 'quarter', 'is_weekend',
                'hour', 'minute' if data[date_column].dt.minute.nunique() > 1 else None
            ],
            'lag_features': {
                'suggestion': 'Create lag features based on the autocorrelation analysis',
                'typical_lags': [1, 7, 14, 30] if data[date_column].dt.day.nunique() > 1 else [1, 2, 3, 4, 5]
            },
            'rolling_statistics': [
                'rolling_mean',
                'rolling_std',
                'rolling_min',
                'rolling_max'
            ],
            'split_strategy': split_strategy,
            'details': {
                'date_column': date_column,
                'is_sorted': is_sorted,
                'has_regular_intervals': has_regular_intervals,
                'regular_interval_ratio': regular_interval_ratio,
                'has_missing_values': has_missing_values,
                'has_multiple_series': has_multiple_series,
                'potential_group_columns': potential_group_columns
            }
        }
    
    def analyze_seasonality(self, data: pd.DataFrame, date_column: str, 
                           target_column: str) -> Dict[str, Any]:
        """
        Analyze seasonality patterns in the time series data.
        
        Args:
            data: Input data.
            date_column: Column name containing date/time data.
            target_column: Target variable column name.
            
        Returns:
            Dictionary with seasonality analysis results.
        """
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(data[date_column].dtype):
            try:
                data[date_column] = pd.to_datetime(data[date_column])
            except:
                return {
                    'error': f'Could not convert column "{date_column}" to datetime'
                }
        
        # Ensure target column is numeric
        if not pd.api.types.is_numeric_dtype(data[target_column].dtype):
            return {
                'error': f'Target column "{target_column}" must be numeric'
            }
        
        # Sort data by date
        data = data.sort_values(date_column)
        
        # Analyze daily, weekly, monthly, and yearly patterns if enough data
        results = {}
        
        # Daily patterns
        if data[date_column].dt.hour.nunique() > 1:
            hourly_means = data.groupby(data[date_column].dt.hour)[target_column].mean()
            hourly_std = hourly_means.std()
            hourly_range = hourly_means.max() - hourly_means.min()
            hourly_mean = hourly_means.mean()
            
            results['daily'] = {
                'has_pattern': hourly_range > hourly_mean * 0.1,
                'strength': hourly_range / hourly_mean if hourly_mean > 0 else 0,
                'peak_hour': hourly_means.idxmax(),
                'trough_hour': hourly_means.idxmin()
            }
        
        # Weekly patterns
        if data[date_column].dt.dayofweek.nunique() > 1:
            daily_means = data.groupby(data[date_column].dt.dayofweek)[target_column].mean()
            daily_std = daily_means.std()
            daily_range = daily_means.max() - daily_means.min()
            daily_mean = daily_means.mean()
            
            results['weekly'] = {
                'has_pattern': daily_range > daily_mean * 0.1,
                'strength': daily_range / daily_mean if daily_mean > 0 else 0,
                'peak_day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][daily_means.idxmax()],
                'trough_day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][daily_means.idxmin()]
            }
        
        # Monthly patterns
        if data[date_column].dt.month.nunique() > 1:
            monthly_means = data.groupby(data[date_column].dt.month)[target_column].mean()
            monthly_std = monthly_means.std()
            monthly_range = monthly_means.max() - monthly_means.min()
            monthly_mean = monthly_means.mean()
            
            month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
            
            results['monthly'] = {
                'has_pattern': monthly_range > monthly_mean * 0.1,
                'strength': monthly_range / monthly_mean if monthly_mean > 0 else 0,
                'peak_month': month_names[monthly_means.idxmax() - 1],
                'trough_month': month_names[monthly_means.idxmin() - 1]
            }
        
        # Yearly patterns
        if data[date_column].dt.year.nunique() > 1:
            yearly_means = data.groupby(data[date_column].dt.year)[target_column].mean()
            yearly_std = yearly_means.std()
            yearly_range = yearly_means.max() - yearly_means.min()
            yearly_mean = yearly_means.mean()
            
            results['yearly'] = {
                'has_pattern': yearly_range > yearly_mean * 0.1,
                'strength': yearly_range / yearly_mean if yearly_mean > 0 else 0,
                'trend': 'increasing' if yearly_means.corr(pd.Series(yearly_means.index)) > 0.5 else
                         'decreasing' if yearly_means.corr(pd.Series(yearly_means.index)) < -0.5 else 'stable'
            }
        
        # Try to detect overall seasonality
        strongest_pattern = None
        max_strength = 0
        
        for period, info in results.items():
            if info.get('has_pattern', False) and info.get('strength', 0) > max_strength:
                strongest_pattern = period
                max_strength = info.get('strength', 0)
        
        return {
            'has_seasonality': strongest_pattern is not None,
            'strongest_pattern': strongest_pattern,
            'patterns': results
        }
