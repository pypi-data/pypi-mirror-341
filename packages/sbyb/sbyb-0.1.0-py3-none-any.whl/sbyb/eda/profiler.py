"""
Data profiler for SBYB EDA.

This module provides functionality to automatically profile datasets
and generate comprehensive reports about their characteristics.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import datetime

from sbyb.core.base import SBYBComponent
from sbyb.core.config import Config


class DataProfiler(SBYBComponent):
    """
    Data profiler for exploratory data analysis.
    
    This component provides functionality to automatically profile datasets
    and generate comprehensive reports about their characteristics.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the data profiler.
        
        Args:
            config: Configuration dictionary for the data profiler.
        """
        super().__init__(config)
        self.profile_results = {}
    
    def profile(self, data: pd.DataFrame, target_column: Optional[str] = None,
               include_correlations: bool = True,
               include_missing_analysis: bool = True,
               include_cardinality_analysis: bool = True,
               include_statistical_analysis: bool = True,
               include_distribution_analysis: bool = True) -> Dict[str, Any]:
        """
        Profile a dataset and generate a comprehensive report.
        
        Args:
            data: DataFrame to profile.
            target_column: Name of the target column, if any.
            include_correlations: Whether to include correlation analysis.
            include_missing_analysis: Whether to include missing value analysis.
            include_cardinality_analysis: Whether to include cardinality analysis.
            include_statistical_analysis: Whether to include statistical analysis.
            include_distribution_analysis: Whether to include distribution analysis.
            
        Returns:
            Dictionary containing the profile results.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame")
        
        # Create a copy to avoid modifying the original
        df = data.copy()
        
        # Initialize profile results
        profile = {
            "dataset_info": self._get_dataset_info(df),
            "columns": self._get_column_info(df),
            "summary_statistics": self._get_summary_statistics(df) if include_statistical_analysis else {},
        }
        
        # Add missing value analysis
        if include_missing_analysis:
            profile["missing_analysis"] = self._analyze_missing_values(df)
        
        # Add cardinality analysis
        if include_cardinality_analysis:
            profile["cardinality_analysis"] = self._analyze_cardinality(df)
        
        # Add correlation analysis
        if include_correlations:
            profile["correlation_analysis"] = self._analyze_correlations(df, target_column)
        
        # Add distribution analysis
        if include_distribution_analysis:
            profile["distribution_analysis"] = self._analyze_distributions(df)
        
        # Add target analysis if target column is provided
        if target_column is not None and target_column in df.columns:
            profile["target_analysis"] = self._analyze_target(df, target_column)
        
        # Store profile results
        self.profile_results = profile
        
        return profile
    
    def _get_dataset_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get basic information about the dataset.
        
        Args:
            df: DataFrame to analyze.
            
        Returns:
            Dictionary containing dataset information.
        """
        return {
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "memory_usage_formatted": f"{df.memory_usage(deep=True).sum() / (1024 * 1024):.2f} MB",
            "num_duplicate_rows": df.duplicated().sum(),
            "percent_duplicate_rows": f"{df.duplicated().mean() * 100:.2f}%",
            "column_types": {
                "numeric": len(df.select_dtypes(include=["number"]).columns),
                "categorical": len(df.select_dtypes(include=["object", "category"]).columns),
                "datetime": len(df.select_dtypes(include=["datetime"]).columns),
                "boolean": len(df.select_dtypes(include=["bool"]).columns),
                "other": len(df.columns) - len(df.select_dtypes(include=["number", "object", "category", "datetime", "bool"]).columns)
            },
            "profiling_timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _get_column_info(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Get information about each column in the dataset.
        
        Args:
            df: DataFrame to analyze.
            
        Returns:
            Dictionary containing column information.
        """
        column_info = {}
        
        for column in df.columns:
            col_type = str(df[column].dtype)
            
            # Determine column category
            if pd.api.types.is_numeric_dtype(df[column]):
                category = "numeric"
            elif pd.api.types.is_datetime64_dtype(df[column]):
                category = "datetime"
            elif pd.api.types.is_bool_dtype(df[column]):
                category = "boolean"
            elif pd.api.types.is_categorical_dtype(df[column]):
                category = "categorical"
            elif pd.api.types.is_object_dtype(df[column]):
                # Check if it might be a datetime
                if df[column].dropna().apply(lambda x: isinstance(x, str) and self._is_date_string(x)).all():
                    category = "potential_datetime"
                else:
                    category = "categorical"
            else:
                category = "other"
            
            # Get basic column stats
            missing_count = df[column].isna().sum()
            missing_percent = missing_count / len(df) * 100
            
            column_info[column] = {
                "type": col_type,
                "category": category,
                "missing_count": missing_count,
                "missing_percent": f"{missing_percent:.2f}%",
                "unique_count": df[column].nunique(),
                "unique_percent": f"{df[column].nunique() / len(df) * 100:.2f}%",
                "memory_usage": df[column].memory_usage(deep=True),
                "memory_usage_formatted": f"{df[column].memory_usage(deep=True) / (1024 * 1024):.4f} MB"
            }
            
            # Add category-specific information
            if category == "numeric":
                column_info[column].update({
                    "min": df[column].min(),
                    "max": df[column].max(),
                    "mean": df[column].mean(),
                    "median": df[column].median(),
                    "std": df[column].std(),
                    "skewness": df[column].skew(),
                    "kurtosis": df[column].kurtosis(),
                    "zeros_count": (df[column] == 0).sum(),
                    "zeros_percent": f"{(df[column] == 0).mean() * 100:.2f}%",
                    "negative_count": (df[column] < 0).sum(),
                    "negative_percent": f"{(df[column] < 0).mean() * 100:.2f}%"
                })
            elif category in ["categorical", "potential_datetime"]:
                # Get top values and their frequencies
                value_counts = df[column].value_counts().head(10).to_dict()
                column_info[column]["top_values"] = value_counts
                
                # Check if it might be a boolean
                if df[column].nunique() == 2:
                    column_info[column]["potential_boolean"] = True
                    column_info[column]["boolean_values"] = df[column].dropna().unique().tolist()
            elif category == "datetime":
                column_info[column].update({
                    "min": df[column].min(),
                    "max": df[column].max(),
                    "range_days": (df[column].max() - df[column].min()).days,
                    "year_distribution": df[column].dt.year.value_counts().to_dict()
                })
            elif category == "boolean":
                column_info[column].update({
                    "true_count": df[column].sum(),
                    "true_percent": f"{df[column].mean() * 100:.2f}%",
                    "false_count": (~df[column]).sum(),
                    "false_percent": f"{(~df[column]).mean() * 100:.2f}%"
                })
        
        return column_info
    
    def _get_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary statistics for the dataset.
        
        Args:
            df: DataFrame to analyze.
            
        Returns:
            Dictionary containing summary statistics.
        """
        # Get basic summary statistics
        summary = {}
        
        # Numeric columns
        numeric_df = df.select_dtypes(include=["number"])
        if not numeric_df.empty:
            summary["numeric"] = numeric_df.describe().to_dict()
        
        # Categorical columns
        categorical_df = df.select_dtypes(include=["object", "category"])
        if not categorical_df.empty:
            cat_summary = {}
            for column in categorical_df.columns:
                cat_summary[column] = {
                    "count": categorical_df[column].count(),
                    "unique": categorical_df[column].nunique(),
                    "top": categorical_df[column].value_counts().index[0] if not categorical_df[column].value_counts().empty else None,
                    "freq": categorical_df[column].value_counts().iloc[0] if not categorical_df[column].value_counts().empty else 0,
                    "top_5": categorical_df[column].value_counts().head(5).to_dict()
                }
            summary["categorical"] = cat_summary
        
        # Datetime columns
        datetime_df = df.select_dtypes(include=["datetime"])
        if not datetime_df.empty:
            dt_summary = {}
            for column in datetime_df.columns:
                dt_summary[column] = {
                    "count": datetime_df[column].count(),
                    "min": datetime_df[column].min(),
                    "max": datetime_df[column].max(),
                    "range_days": (datetime_df[column].max() - datetime_df[column].min()).days
                }
            summary["datetime"] = dt_summary
        
        return summary
    
    def _analyze_missing_values(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze missing values in the dataset.
        
        Args:
            df: DataFrame to analyze.
            
        Returns:
            Dictionary containing missing value analysis.
        """
        # Get missing value counts and percentages
        missing_counts = df.isna().sum()
        missing_percents = df.isna().mean() * 100
        
        # Create missing value summary
        missing_summary = {
            "total_missing_values": df.isna().sum().sum(),
            "total_missing_percent": f"{df.isna().mean().mean() * 100:.2f}%",
            "columns_with_missing": missing_counts[missing_counts > 0].shape[0],
            "columns_without_missing": missing_counts[missing_counts == 0].shape[0],
            "column_missing_counts": missing_counts[missing_counts > 0].to_dict(),
            "column_missing_percents": {col: f"{percent:.2f}%" for col, percent in missing_percents[missing_percents > 0].to_dict().items()},
            "rows_with_missing": df.isna().any(axis=1).sum(),
            "rows_with_missing_percent": f"{df.isna().any(axis=1).mean() * 100:.2f}%",
            "rows_without_missing": (~df.isna().any(axis=1)).sum(),
            "rows_without_missing_percent": f"{(~df.isna().any(axis=1)).mean() * 100:.2f}%"
        }
        
        # Add missing patterns
        missing_patterns = df.isna().groupby(list(df.columns)).size().reset_index(name="count")
        if not missing_patterns.empty:
            # Convert to more readable format
            patterns = []
            for _, row in missing_patterns.iterrows():
                pattern = {col: "Missing" if row[col] else "Present" for col in df.columns}
                pattern["count"] = row["count"]
                pattern["percent"] = f"{row['count'] / len(df) * 100:.2f}%"
                patterns.append(pattern)
            
            missing_summary["missing_patterns"] = patterns
        
        return missing_summary
    
    def _analyze_cardinality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze cardinality of columns in the dataset.
        
        Args:
            df: DataFrame to analyze.
            
        Returns:
            Dictionary containing cardinality analysis.
        """
        # Get unique counts and percentages
        unique_counts = df.nunique()
        unique_percents = unique_counts / len(df) * 100
        
        # Categorize columns by cardinality
        high_cardinality = unique_percents[unique_percents > 90].index.tolist()
        medium_cardinality = unique_percents[(unique_percents > 50) & (unique_percents <= 90)].index.tolist()
        low_cardinality = unique_percents[(unique_percents > 10) & (unique_percents <= 50)].index.tolist()
        very_low_cardinality = unique_percents[unique_percents <= 10].index.tolist()
        
        # Create cardinality summary
        cardinality_summary = {
            "column_unique_counts": unique_counts.to_dict(),
            "column_unique_percents": {col: f"{percent:.2f}%" for col, percent in unique_percents.to_dict().items()},
            "high_cardinality_columns": high_cardinality,
            "medium_cardinality_columns": medium_cardinality,
            "low_cardinality_columns": low_cardinality,
            "very_low_cardinality_columns": very_low_cardinality,
            "potential_id_columns": high_cardinality
        }
        
        # Identify potential categorical columns that should be encoded
        categorical_df = df.select_dtypes(include=["object", "category"])
        if not categorical_df.empty:
            potential_encoded = []
            for column in categorical_df.columns:
                if unique_counts[column] <= 50:  # Reasonable number of categories
                    potential_encoded.append(column)
            
            cardinality_summary["potential_encoded_columns"] = potential_encoded
        
        # Identify potential continuous columns that should be binned
        numeric_df = df.select_dtypes(include=["number"])
        if not numeric_df.empty:
            potential_binned = []
            for column in numeric_df.columns:
                if unique_counts[column] > 100:  # Many unique values
                    potential_binned.append(column)
            
            cardinality_summary["potential_binned_columns"] = potential_binned
        
        return cardinality_summary
    
    def _analyze_correlations(self, df: pd.DataFrame, target_column: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze correlations between columns in the dataset.
        
        Args:
            df: DataFrame to analyze.
            target_column: Name of the target column, if any.
            
        Returns:
            Dictionary containing correlation analysis.
        """
        # Get numeric columns for correlation analysis
        numeric_df = df.select_dtypes(include=["number"])
        
        if numeric_df.empty:
            return {"message": "No numeric columns found for correlation analysis"}
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr().round(3)
        
        # Create correlation summary
        correlation_summary = {
            "correlation_matrix": corr_matrix.to_dict()
        }
        
        # Find highly correlated pairs
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                corr_value = corr_matrix.iloc[i, j]
                
                if abs(corr_value) > 0.7:  # High correlation threshold
                    corr_pairs.append({
                        "column1": col1,
                        "column2": col2,
                        "correlation": corr_value,
                        "strength": "strong positive" if corr_value > 0.7 else "strong negative"
                    })
        
        correlation_summary["highly_correlated_pairs"] = corr_pairs
        
        # Add target correlation if target column is provided
        if target_column is not None and target_column in numeric_df.columns:
            target_corrs = corr_matrix[target_column].drop(target_column).sort_values(ascending=False)
            
            correlation_summary["target_correlations"] = target_corrs.to_dict()
            
            # Identify top features by correlation
            correlation_summary["top_positive_features"] = target_corrs[target_corrs > 0].head(5).to_dict()
            correlation_summary["top_negative_features"] = target_corrs[target_corrs < 0].sort_values().head(5).to_dict()
        
        return correlation_summary
    
    def _analyze_distributions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze distributions of columns in the dataset.
        
        Args:
            df: DataFrame to analyze.
            
        Returns:
            Dictionary containing distribution analysis.
        """
        distribution_summary = {}
        
        # Analyze numeric columns
        numeric_df = df.select_dtypes(include=["number"])
        if not numeric_df.empty:
            numeric_summary = {}
            
            for column in numeric_df.columns:
                # Skip columns with too many missing values
                if numeric_df[column].isna().mean() > 0.5:
                    continue
                
                # Calculate distribution statistics
                skewness = numeric_df[column].skew()
                kurtosis = numeric_df[column].kurtosis()
                
                # Determine distribution type
                dist_type = "unknown"
                if abs(skewness) < 0.5 and abs(kurtosis) < 0.5:
                    dist_type = "normal"
                elif skewness > 1:
                    dist_type = "right-skewed"
                elif skewness < -1:
                    dist_type = "left-skewed"
                
                # Check for outliers
                q1 = numeric_df[column].quantile(0.25)
                q3 = numeric_df[column].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                outliers = numeric_df[(numeric_df[column] < lower_bound) | (numeric_df[column] > upper_bound)][column]
                
                numeric_summary[column] = {
                    "skewness": skewness,
                    "kurtosis": kurtosis,
                    "distribution_type": dist_type,
                    "quartiles": {
                        "q1": q1,
                        "q2": numeric_df[column].median(),
                        "q3": q3,
                        "iqr": iqr
                    },
                    "outliers": {
                        "count": len(outliers),
                        "percent": f"{len(outliers) / len(numeric_df) * 100:.2f}%",
                        "min": outliers.min() if not outliers.empty else None,
                        "max": outliers.max() if not outliers.empty else None
                    }
                }
                
                # Suggest transformations for skewed distributions
                if abs(skewness) > 1:
                    transformations = []
                    if skewness > 1:  # Right-skewed
                        transformations.extend(["log", "sqrt", "box-cox"])
                    else:  # Left-skewed
                        transformations.extend(["square", "cube", "exponential"])
                    
                    numeric_summary[column]["suggested_transformations"] = transformations
            
            distribution_summary["numeric"] = numeric_summary
        
        # Analyze categorical columns
        categorical_df = df.select_dtypes(include=["object", "category"])
        if not categorical_df.empty:
            categorical_summary = {}
            
            for column in categorical_df.columns:
                # Skip columns with too many missing values
                if categorical_df[column].isna().mean() > 0.5:
                    continue
                
                # Calculate value counts
                value_counts = categorical_df[column].value_counts()
                
                # Check for imbalance
                if len(value_counts) > 1:
                    imbalance_ratio = value_counts.max() / value_counts.min()
                    is_imbalanced = imbalance_ratio > 10  # Arbitrary threshold
                else:
                    imbalance_ratio = float('inf')
                    is_imbalanced = True
                
                categorical_summary[column] = {
                    "value_counts": value_counts.head(10).to_dict(),
                    "imbalance_ratio": imbalance_ratio,
                    "is_imbalanced": is_imbalanced,
                    "entropy": self._calculate_entropy(value_counts / value_counts.sum()),
                    "suggested_encoding": self._suggest_encoding(value_counts)
                }
            
            distribution_summary["categorical"] = categorical_summary
        
        return distribution_summary
    
    def _analyze_target(self, df: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """
        Analyze the target column.
        
        Args:
            df: DataFrame to analyze.
            target_column: Name of the target column.
            
        Returns:
            Dictionary containing target analysis.
        """
        if target_column not in df.columns:
            return {"error": f"Target column '{target_column}' not found in the dataset"}
        
        target_series = df[target_column]
        target_type = str(target_series.dtype)
        
        # Determine target category
        if pd.api.types.is_numeric_dtype(target_series):
            category = "numeric"
        elif pd.api.types.is_datetime64_dtype(target_series):
            category = "datetime"
        elif pd.api.types.is_bool_dtype(target_series):
            category = "boolean"
        elif pd.api.types.is_categorical_dtype(target_series) or pd.api.types.is_object_dtype(target_series):
            category = "categorical"
        else:
            category = "other"
        
        # Initialize target analysis
        target_analysis = {
            "column": target_column,
            "type": target_type,
            "category": category,
            "missing_count": target_series.isna().sum(),
            "missing_percent": f"{target_series.isna().mean() * 100:.2f}%"
        }
        
        # Add category-specific analysis
        if category == "numeric":
            # Basic statistics
            target_analysis.update({
                "min": target_series.min(),
                "max": target_series.max(),
                "mean": target_series.mean(),
                "median": target_series.median(),
                "std": target_series.std(),
                "skewness": target_series.skew(),
                "kurtosis": target_series.kurtosis()
            })
            
            # Distribution analysis
            q1 = target_series.quantile(0.25)
            q3 = target_series.quantile(0.75)
            iqr = q3 - q1
            
            target_analysis["distribution"] = {
                "quartiles": {
                    "q1": q1,
                    "q2": target_series.median(),
                    "q3": q3,
                    "iqr": iqr
                },
                "distribution_type": "unknown"
            }
            
            # Determine distribution type
            skewness = target_series.skew()
            if abs(skewness) < 0.5:
                target_analysis["distribution"]["distribution_type"] = "normal"
            elif skewness > 1:
                target_analysis["distribution"]["distribution_type"] = "right-skewed"
            elif skewness < -1:
                target_analysis["distribution"]["distribution_type"] = "left-skewed"
            
            # Suggest task type
            target_analysis["suggested_task"] = "regression"
            
            # Suggest transformations for skewed distributions
            if abs(skewness) > 1:
                transformations = []
                if skewness > 1:  # Right-skewed
                    transformations.extend(["log", "sqrt", "box-cox"])
                else:  # Left-skewed
                    transformations.extend(["square", "cube", "exponential"])
                
                target_analysis["suggested_transformations"] = transformations
        
        elif category == "categorical":
            # Value counts
            value_counts = target_series.value_counts()
            
            target_analysis.update({
                "unique_count": target_series.nunique(),
                "unique_values": target_series.unique().tolist(),
                "value_counts": value_counts.to_dict()
            })
            
            # Check for imbalance
            if len(value_counts) > 1:
                imbalance_ratio = value_counts.max() / value_counts.min()
                is_imbalanced = imbalance_ratio > 10  # Arbitrary threshold
            else:
                imbalance_ratio = float('inf')
                is_imbalanced = True
            
            target_analysis["imbalance"] = {
                "imbalance_ratio": imbalance_ratio,
                "is_imbalanced": is_imbalanced
            }
            
            # Suggest task type
            if target_series.nunique() == 2:
                target_analysis["suggested_task"] = "binary_classification"
            else:
                target_analysis["suggested_task"] = "multiclass_classification"
            
            # Suggest handling for imbalanced data
            if is_imbalanced:
                target_analysis["suggested_handling"] = [
                    "class_weights",
                    "oversampling",
                    "undersampling",
                    "SMOTE"
                ]
        
        elif category == "boolean":
            # Value counts
            value_counts = target_series.value_counts()
            
            target_analysis.update({
                "true_count": target_series.sum(),
                "true_percent": f"{target_series.mean() * 100:.2f}%",
                "false_count": (~target_series).sum(),
                "false_percent": f"{(~target_series).mean() * 100:.2f}%"
            })
            
            # Check for imbalance
            imbalance_ratio = max(target_series.mean(), 1 - target_series.mean()) / min(target_series.mean(), 1 - target_series.mean())
            is_imbalanced = imbalance_ratio > 3  # Arbitrary threshold
            
            target_analysis["imbalance"] = {
                "imbalance_ratio": imbalance_ratio,
                "is_imbalanced": is_imbalanced
            }
            
            # Suggest task type
            target_analysis["suggested_task"] = "binary_classification"
            
            # Suggest handling for imbalanced data
            if is_imbalanced:
                target_analysis["suggested_handling"] = [
                    "class_weights",
                    "oversampling",
                    "undersampling",
                    "SMOTE"
                ]
        
        elif category == "datetime":
            # Basic statistics
            target_analysis.update({
                "min": target_series.min(),
                "max": target_series.max(),
                "range_days": (target_series.max() - target_series.min()).days
            })
            
            # Suggest task type
            target_analysis["suggested_task"] = "time_series"
        
        return target_analysis
    
    def _calculate_entropy(self, probabilities: pd.Series) -> float:
        """
        Calculate entropy of a probability distribution.
        
        Args:
            probabilities: Series of probabilities.
            
        Returns:
            Entropy value.
        """
        return -np.sum(probabilities * np.log2(probabilities))
    
    def _suggest_encoding(self, value_counts: pd.Series) -> str:
        """
        Suggest encoding method for a categorical column.
        
        Args:
            value_counts: Series of value counts.
            
        Returns:
            Suggested encoding method.
        """
        num_categories = len(value_counts)
        
        if num_categories == 2:
            return "binary"
        elif num_categories <= 10:
            return "one-hot"
        elif num_categories <= 50:
            return "label"
        else:
            return "target"
    
    def _is_date_string(self, value: str) -> bool:
        """
        Check if a string might be a date.
        
        Args:
            value: String to check.
            
        Returns:
            True if the string might be a date, False otherwise.
        """
        import re
        
        # Common date patterns
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY or MM-DD-YYYY
            r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY or MM/DD/YYYY
            r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
            r'\d{2}\.\d{2}\.\d{4}',  # DD.MM.YYYY or MM.DD.YYYY
            r'\d{4}\.\d{2}\.\d{2}'   # YYYY.MM.DD
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, value):
                return True
        
        return False
    
    def generate_html_report(self, output_path: str) -> str:
        """
        Generate an HTML report from the profile results.
        
        Args:
            output_path: Path to save the HTML report.
            
        Returns:
            Path to the generated HTML report.
        """
        if not self.profile_results:
            raise ValueError("No profile results available. Run profile() first.")
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SBYB Data Profile Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    color: #333;
                }}
                h1, h2, h3, h4 {{
                    color: #2c3e50;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                .section {{
                    margin-bottom: 30px;
                    padding: 20px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                th, td {{
                    padding: 12px 15px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                .highlight {{
                    background-color: #ffffcc;
                }}
                .warning {{
                    color: #e74c3c;
                }}
                .success {{
                    color: #2ecc71;
                }}
                .info {{
                    color: #3498db;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>SBYB Data Profile Report</h1>
                <p>Generated on {self.profile_results.get('dataset_info', {}).get('profiling_timestamp', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}</p>
                
                <div class="section">
                    <h2>Dataset Overview</h2>
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Number of Rows</td>
                            <td>{self.profile_results.get('dataset_info', {}).get('num_rows', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Number of Columns</td>
                            <td>{self.profile_results.get('dataset_info', {}).get('num_columns', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Memory Usage</td>
                            <td>{self.profile_results.get('dataset_info', {}).get('memory_usage_formatted', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Duplicate Rows</td>
                            <td>{self.profile_results.get('dataset_info', {}).get('num_duplicate_rows', 'N/A')} ({self.profile_results.get('dataset_info', {}).get('percent_duplicate_rows', 'N/A')})</td>
                        </tr>
                    </table>
                    
                    <h3>Column Types</h3>
                    <table>
                        <tr>
                            <th>Type</th>
                            <th>Count</th>
                        </tr>
                        <tr>
                            <td>Numeric</td>
                            <td>{self.profile_results.get('dataset_info', {}).get('column_types', {}).get('numeric', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Categorical</td>
                            <td>{self.profile_results.get('dataset_info', {}).get('column_types', {}).get('categorical', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Datetime</td>
                            <td>{self.profile_results.get('dataset_info', {}).get('column_types', {}).get('datetime', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Boolean</td>
                            <td>{self.profile_results.get('dataset_info', {}).get('column_types', {}).get('boolean', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Other</td>
                            <td>{self.profile_results.get('dataset_info', {}).get('column_types', {}).get('other', 'N/A')}</td>
                        </tr>
                    </table>
                </div>
        """
        
        # Add missing values section
        if 'missing_analysis' in self.profile_results:
            missing = self.profile_results['missing_analysis']
            html_content += f"""
                <div class="section">
                    <h2>Missing Values</h2>
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Total Missing Values</td>
                            <td>{missing.get('total_missing_values', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Total Missing Percent</td>
                            <td>{missing.get('total_missing_percent', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Columns With Missing</td>
                            <td>{missing.get('columns_with_missing', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Columns Without Missing</td>
                            <td>{missing.get('columns_without_missing', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Rows With Missing</td>
                            <td>{missing.get('rows_with_missing', 'N/A')} ({missing.get('rows_with_missing_percent', 'N/A')})</td>
                        </tr>
                        <tr>
                            <td>Rows Without Missing</td>
                            <td>{missing.get('rows_without_missing', 'N/A')} ({missing.get('rows_without_missing_percent', 'N/A')})</td>
                        </tr>
                    </table>
                    
                    <h3>Columns with Missing Values</h3>
                    <table>
                        <tr>
                            <th>Column</th>
                            <th>Missing Count</th>
                            <th>Missing Percent</th>
                        </tr>
            """
            
            for col, count in missing.get('column_missing_counts', {}).items():
                percent = missing.get('column_missing_percents', {}).get(col, 'N/A')
                html_content += f"""
                        <tr>
                            <td>{col}</td>
                            <td>{count}</td>
                            <td>{percent}</td>
                        </tr>
                """
            
            html_content += """
                    </table>
                </div>
            """
        
        # Add column details section
        if 'columns' in self.profile_results:
            html_content += """
                <div class="section">
                    <h2>Column Details</h2>
                    <table>
                        <tr>
                            <th>Column</th>
                            <th>Type</th>
                            <th>Category</th>
                            <th>Missing</th>
                            <th>Unique</th>
                            <th>Details</th>
                        </tr>
            """
            
            for col, info in self.profile_results['columns'].items():
                details = ""
                
                if info.get('category') == 'numeric':
                    details = f"Min: {info.get('min', 'N/A')}, Max: {info.get('max', 'N/A')}, Mean: {info.get('mean', 'N/A'):.2f}, Median: {info.get('median', 'N/A'):.2f}"
                elif info.get('category') in ['categorical', 'potential_datetime']:
                    top_values = info.get('top_values', {})
                    if top_values:
                        top_item = list(top_values.items())[0]
                        details = f"Most common: {top_item[0]} ({top_item[1]} occurrences)"
                elif info.get('category') == 'datetime':
                    details = f"Range: {info.get('min', 'N/A')} to {info.get('max', 'N/A')}"
                elif info.get('category') == 'boolean':
                    details = f"True: {info.get('true_percent', 'N/A')}, False: {info.get('false_percent', 'N/A')}"
                
                html_content += f"""
                        <tr>
                            <td>{col}</td>
                            <td>{info.get('type', 'N/A')}</td>
                            <td>{info.get('category', 'N/A')}</td>
                            <td>{info.get('missing_percent', 'N/A')}</td>
                            <td>{info.get('unique_count', 'N/A')} ({info.get('unique_percent', 'N/A')})</td>
                            <td>{details}</td>
                        </tr>
                """
            
            html_content += """
                    </table>
                </div>
            """
        
        # Add correlation section
        if 'correlation_analysis' in self.profile_results and 'highly_correlated_pairs' in self.profile_results['correlation_analysis']:
            corr_pairs = self.profile_results['correlation_analysis']['highly_correlated_pairs']
            
            if corr_pairs:
                html_content += """
                    <div class="section">
                        <h2>Correlations</h2>
                        <h3>Highly Correlated Pairs</h3>
                        <table>
                            <tr>
                                <th>Column 1</th>
                                <th>Column 2</th>
                                <th>Correlation</th>
                                <th>Strength</th>
                            </tr>
                """
                
                for pair in corr_pairs:
                    html_content += f"""
                            <tr>
                                <td>{pair.get('column1', 'N/A')}</td>
                                <td>{pair.get('column2', 'N/A')}</td>
                                <td>{pair.get('correlation', 'N/A')}</td>
                                <td>{pair.get('strength', 'N/A')}</td>
                            </tr>
                    """
                
                html_content += """
                        </table>
                    </div>
                """
        
        # Add target analysis section
        if 'target_analysis' in self.profile_results:
            target = self.profile_results['target_analysis']
            
            html_content += f"""
                <div class="section">
                    <h2>Target Analysis</h2>
                    <h3>Target: {target.get('column', 'N/A')}</h3>
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Type</td>
                            <td>{target.get('type', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Category</td>
                            <td>{target.get('category', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Missing</td>
                            <td>{target.get('missing_count', 'N/A')} ({target.get('missing_percent', 'N/A')})</td>
                        </tr>
                        <tr>
                            <td>Suggested Task</td>
                            <td>{target.get('suggested_task', 'N/A')}</td>
                        </tr>
            """
            
            if target.get('category') == 'numeric':
                html_content += f"""
                        <tr>
                            <td>Min</td>
                            <td>{target.get('min', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Max</td>
                            <td>{target.get('max', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Mean</td>
                            <td>{target.get('mean', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Median</td>
                            <td>{target.get('median', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Standard Deviation</td>
                            <td>{target.get('std', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Skewness</td>
                            <td>{target.get('skewness', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Distribution Type</td>
                            <td>{target.get('distribution', {}).get('distribution_type', 'N/A')}</td>
                        </tr>
                """
                
                if 'suggested_transformations' in target:
                    html_content += f"""
                        <tr>
                            <td>Suggested Transformations</td>
                            <td>{', '.join(target.get('suggested_transformations', []))}</td>
                        </tr>
                    """
            
            elif target.get('category') in ['categorical', 'boolean']:
                html_content += f"""
                        <tr>
                            <td>Unique Values</td>
                            <td>{target.get('unique_count', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Imbalanced</td>
                            <td>{'Yes' if target.get('imbalance', {}).get('is_imbalanced', False) else 'No'}</td>
                        </tr>
                        <tr>
                            <td>Imbalance Ratio</td>
                            <td>{target.get('imbalance', {}).get('imbalance_ratio', 'N/A')}</td>
                        </tr>
                """
                
                if 'suggested_handling' in target:
                    html_content += f"""
                        <tr>
                            <td>Suggested Handling</td>
                            <td>{', '.join(target.get('suggested_handling', []))}</td>
                        </tr>
                    """
            
            html_content += """
                    </table>
                </div>
            """
        
        # Close HTML
        html_content += """
            </div>
        </body>
        </html>
        """
        
        # Write HTML to file
        with open(output_path, "w") as f:
            f.write(html_content)
        
        return output_path
    
    def generate_json_report(self, output_path: str) -> str:
        """
        Generate a JSON report from the profile results.
        
        Args:
            output_path: Path to save the JSON report.
            
        Returns:
            Path to the generated JSON report.
        """
        if not self.profile_results:
            raise ValueError("No profile results available. Run profile() first.")
        
        # Convert non-serializable objects to strings
        def json_serializable(obj):
            if isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
                return int(obj)
            elif isinstance(obj, (np.float64, np.float32, np.float16)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, pd.Series):
                return obj.to_dict()
            elif isinstance(obj, pd.DataFrame):
                return obj.to_dict(orient='records')
            elif isinstance(obj, (pd.Timestamp, datetime.datetime, datetime.date)):
                return str(obj)
            elif isinstance(obj, set):
                return list(obj)
            else:
                return str(obj)
        
        # Write JSON to file
        with open(output_path, "w") as f:
            json.dump(self.profile_results, f, default=json_serializable, indent=2)
        
        return output_path
    
    def plot_missing_values(self, output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot missing values in the dataset.
        
        Args:
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        if not self.profile_results or 'missing_analysis' not in self.profile_results:
            raise ValueError("No missing value analysis available. Run profile() first.")
        
        missing = self.profile_results['missing_analysis']
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Get columns with missing values
        columns = list(missing.get('column_missing_counts', {}).keys())
        counts = list(missing.get('column_missing_counts', {}).values())
        
        # Sort by missing count
        sorted_indices = np.argsort(counts)
        columns = [columns[i] for i in sorted_indices]
        counts = [counts[i] for i in sorted_indices]
        
        # Plot
        ax.barh(columns, counts, color='skyblue')
        ax.set_xlabel('Missing Count')
        ax.set_ylabel('Column')
        ax.set_title('Missing Values by Column')
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Add percentages
        for i, count in enumerate(counts):
            percent = missing.get('column_missing_percents', {}).get(columns[i], 'N/A')
            ax.text(count + 0.5, i, percent, va='center')
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_correlations(self, output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot correlation matrix.
        
        Args:
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        if not self.profile_results or 'correlation_analysis' not in self.profile_results:
            raise ValueError("No correlation analysis available. Run profile() first.")
        
        if 'correlation_matrix' not in self.profile_results['correlation_analysis']:
            raise ValueError("No correlation matrix available.")
        
        # Get correlation matrix
        corr_matrix = self.profile_results['correlation_analysis']['correlation_matrix']
        
        # Convert to DataFrame
        corr_df = pd.DataFrame(corr_matrix)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Plot
        mask = np.triu(np.ones_like(corr_df, dtype=bool))
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        
        sns.heatmap(corr_df, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                   square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True, fmt=".2f")
        
        ax.set_title('Correlation Matrix')
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_distributions(self, columns: Optional[List[str]] = None, 
                          output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot distributions of numeric columns.
        
        Args:
            columns: List of columns to plot. If None, plot all numeric columns.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        if not self.profile_results or 'columns' not in self.profile_results:
            raise ValueError("No column information available. Run profile() first.")
        
        # Get numeric columns
        numeric_columns = [col for col, info in self.profile_results['columns'].items() 
                          if info.get('category') == 'numeric']
        
        if not numeric_columns:
            raise ValueError("No numeric columns available.")
        
        # Filter columns if provided
        if columns:
            numeric_columns = [col for col in columns if col in numeric_columns]
            
            if not numeric_columns:
                raise ValueError("No valid numeric columns provided.")
        
        # Limit to 16 columns for readability
        if len(numeric_columns) > 16:
            numeric_columns = numeric_columns[:16]
        
        # Calculate grid dimensions
        n_cols = min(4, len(numeric_columns))
        n_rows = (len(numeric_columns) + n_cols - 1) // n_cols
        
        # Create figure
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 3 * n_rows))
        
        # Flatten axes for easy iteration
        if n_rows == 1 and n_cols == 1:
            axes = np.array([axes])
        axes = axes.flatten()
        
        # Plot distributions
        for i, col in enumerate(numeric_columns):
            if i < len(axes):
                # Get distribution info
                if 'distribution_analysis' in self.profile_results and 'numeric' in self.profile_results['distribution_analysis']:
                    dist_info = self.profile_results['distribution_analysis']['numeric'].get(col, {})
                    dist_type = dist_info.get('distribution_type', 'unknown')
                    skewness = dist_info.get('skewness', 0)
                else:
                    dist_type = 'unknown'
                    skewness = 0
                
                # Add title with distribution type
                title = f"{col}\n(Distribution: {dist_type}, Skewness: {skewness:.2f})"
                axes[i].set_title(title)
                
                # Add grid
                axes[i].grid(linestyle='--', alpha=0.7)
        
        # Hide unused subplots
        for i in range(len(numeric_columns), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_categorical_distributions(self, columns: Optional[List[str]] = None,
                                      max_categories: int = 10,
                                      output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot distributions of categorical columns.
        
        Args:
            columns: List of columns to plot. If None, plot all categorical columns.
            max_categories: Maximum number of categories to show per column.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        if not self.profile_results or 'columns' not in self.profile_results:
            raise ValueError("No column information available. Run profile() first.")
        
        # Get categorical columns
        categorical_columns = [col for col, info in self.profile_results['columns'].items() 
                              if info.get('category') in ['categorical', 'potential_datetime']]
        
        if not categorical_columns:
            raise ValueError("No categorical columns available.")
        
        # Filter columns if provided
        if columns:
            categorical_columns = [col for col in columns if col in categorical_columns]
            
            if not categorical_columns:
                raise ValueError("No valid categorical columns provided.")
        
        # Limit to 9 columns for readability
        if len(categorical_columns) > 9:
            categorical_columns = categorical_columns[:9]
        
        # Calculate grid dimensions
        n_cols = min(3, len(categorical_columns))
        n_rows = (len(categorical_columns) + n_cols - 1) // n_cols
        
        # Create figure
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows))
        
        # Flatten axes for easy iteration
        if n_rows == 1 and n_cols == 1:
            axes = np.array([axes])
        axes = axes.flatten()
        
        # Plot distributions
        for i, col in enumerate(categorical_columns):
            if i < len(axes):
                # Get value counts
                if 'distribution_analysis' in self.profile_results and 'categorical' in self.profile_results['distribution_analysis']:
                    value_counts = self.profile_results['distribution_analysis']['categorical'].get(col, {}).get('value_counts', {})
                else:
                    value_counts = self.profile_results['columns'][col].get('top_values', {})
                
                # Convert to Series for easier handling
                value_counts = pd.Series(value_counts)
                
                # Limit categories
                if len(value_counts) > max_categories:
                    other_count = value_counts.iloc[max_categories:].sum()
                    value_counts = value_counts.iloc[:max_categories]
                    value_counts['Other'] = other_count
                
                # Plot
                value_counts.plot(kind='bar', ax=axes[i], color='skyblue')
                
                # Add title
                axes[i].set_title(col)
                
                # Rotate x-axis labels
                axes[i].set_xticklabels(axes[i].get_xticklabels(), rotation=45, ha='right')
                
                # Add grid
                axes[i].grid(axis='y', linestyle='--', alpha=0.7)
        
        # Hide unused subplots
        for i in range(len(categorical_columns), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
