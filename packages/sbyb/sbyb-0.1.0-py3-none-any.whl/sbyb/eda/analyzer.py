"""
Data analyzer for SBYB EDA.

This module provides functionality to analyze datasets and extract insights
through statistical analysis and machine learning techniques.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
import datetime
import warnings
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif

from sbyb.core.base import SBYBComponent
from sbyb.core.config import Config


class DataAnalyzer(SBYBComponent):
    """
    Data analyzer for exploratory data analysis.
    
    This component provides functionality to analyze datasets and extract insights
    through statistical analysis and machine learning techniques.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the data analyzer.
        
        Args:
            config: Configuration dictionary for the data analyzer.
        """
        super().__init__(config)
        self.analysis_results = {}
    
    def analyze(self, data: pd.DataFrame, target_column: Optional[str] = None,
               include_outlier_detection: bool = True,
               include_feature_importance: bool = True,
               include_dimensionality_reduction: bool = True,
               include_clustering: bool = True) -> Dict[str, Any]:
        """
        Analyze a dataset and extract insights.
        
        Args:
            data: DataFrame to analyze.
            target_column: Name of the target column, if any.
            include_outlier_detection: Whether to include outlier detection.
            include_feature_importance: Whether to include feature importance analysis.
            include_dimensionality_reduction: Whether to include dimensionality reduction.
            include_clustering: Whether to include clustering analysis.
            
        Returns:
            Dictionary containing the analysis results.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame")
        
        # Create a copy to avoid modifying the original
        df = data.copy()
        
        # Initialize analysis results
        analysis = {
            "dataset_info": {
                "num_rows": len(df),
                "num_columns": len(df.columns),
                "column_types": {
                    "numeric": len(df.select_dtypes(include=["number"]).columns),
                    "categorical": len(df.select_dtypes(include=["object", "category"]).columns),
                    "datetime": len(df.select_dtypes(include=["datetime"]).columns),
                    "boolean": len(df.select_dtypes(include=["bool"]).columns),
                    "other": len(df.columns) - len(df.select_dtypes(include=["number", "object", "category", "datetime", "bool"]).columns)
                },
                "analysis_timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "statistical_analysis": self._perform_statistical_analysis(df)
        }
        
        # Add outlier detection
        if include_outlier_detection:
            analysis["outlier_detection"] = self._detect_outliers(df)
        
        # Add feature importance
        if include_feature_importance and target_column is not None:
            analysis["feature_importance"] = self._analyze_feature_importance(df, target_column)
        
        # Add dimensionality reduction
        if include_dimensionality_reduction:
            analysis["dimensionality_reduction"] = self._perform_dimensionality_reduction(df)
        
        # Add clustering analysis
        if include_clustering:
            analysis["clustering"] = self._perform_clustering(df)
        
        # Store analysis results
        self.analysis_results = analysis
        
        return analysis
    
    def _perform_statistical_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform statistical analysis on the dataset.
        
        Args:
            df: DataFrame to analyze.
            
        Returns:
            Dictionary containing statistical analysis results.
        """
        # Initialize results
        stats = {}
        
        # Analyze numeric columns
        numeric_df = df.select_dtypes(include=["number"])
        if not numeric_df.empty:
            # Basic statistics
            numeric_stats = numeric_df.describe().to_dict()
            
            # Add additional statistics
            for column in numeric_df.columns:
                numeric_stats[column]["skewness"] = numeric_df[column].skew()
                numeric_stats[column]["kurtosis"] = numeric_df[column].kurtosis()
                numeric_stats[column]["zeros_count"] = (numeric_df[column] == 0).sum()
                numeric_stats[column]["zeros_percent"] = (numeric_df[column] == 0).mean() * 100
                numeric_stats[column]["negative_count"] = (numeric_df[column] < 0).sum()
                numeric_stats[column]["negative_percent"] = (numeric_df[column] < 0).mean() * 100
            
            stats["numeric"] = numeric_stats
            
            # Correlation analysis
            if len(numeric_df.columns) > 1:
                corr_matrix = numeric_df.corr().round(3)
                
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
                
                stats["correlation"] = {
                    "matrix": corr_matrix.to_dict(),
                    "highly_correlated_pairs": corr_pairs
                }
        
        # Analyze categorical columns
        categorical_df = df.select_dtypes(include=["object", "category"])
        if not categorical_df.empty:
            cat_stats = {}
            
            for column in categorical_df.columns:
                value_counts = categorical_df[column].value_counts()
                
                cat_stats[column] = {
                    "count": categorical_df[column].count(),
                    "unique": categorical_df[column].nunique(),
                    "top": value_counts.index[0] if not value_counts.empty else None,
                    "freq": value_counts.iloc[0] if not value_counts.empty else 0,
                    "top_5": value_counts.head(5).to_dict(),
                    "entropy": self._calculate_entropy(value_counts / value_counts.sum())
                }
                
                # Check for imbalance
                if len(value_counts) > 1:
                    imbalance_ratio = value_counts.max() / value_counts.min()
                    is_imbalanced = imbalance_ratio > 10  # Arbitrary threshold
                else:
                    imbalance_ratio = float('inf')
                    is_imbalanced = True
                
                cat_stats[column]["imbalance_ratio"] = imbalance_ratio
                cat_stats[column]["is_imbalanced"] = is_imbalanced
            
            stats["categorical"] = cat_stats
        
        # Analyze datetime columns
        datetime_df = df.select_dtypes(include=["datetime"])
        if not datetime_df.empty:
            dt_stats = {}
            
            for column in datetime_df.columns:
                dt_stats[column] = {
                    "count": datetime_df[column].count(),
                    "min": datetime_df[column].min(),
                    "max": datetime_df[column].max(),
                    "range_days": (datetime_df[column].max() - datetime_df[column].min()).days,
                    "year_distribution": datetime_df[column].dt.year.value_counts().to_dict(),
                    "month_distribution": datetime_df[column].dt.month.value_counts().to_dict(),
                    "weekday_distribution": datetime_df[column].dt.dayofweek.value_counts().to_dict()
                }
            
            stats["datetime"] = dt_stats
        
        return stats
    
    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect outliers in the dataset.
        
        Args:
            df: DataFrame to analyze.
            
        Returns:
            Dictionary containing outlier detection results.
        """
        # Initialize results
        outliers = {}
        
        # Get numeric columns
        numeric_df = df.select_dtypes(include=["number"])
        
        if numeric_df.empty:
            return {"message": "No numeric columns found for outlier detection"}
        
        # Method 1: IQR method
        iqr_outliers = {}
        
        for column in numeric_df.columns:
            q1 = numeric_df[column].quantile(0.25)
            q3 = numeric_df[column].quantile(0.75)
            iqr = q3 - q1
            
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outlier_mask = (numeric_df[column] < lower_bound) | (numeric_df[column] > upper_bound)
            outlier_indices = outlier_mask[outlier_mask].index.tolist()
            
            iqr_outliers[column] = {
                "count": len(outlier_indices),
                "percent": len(outlier_indices) / len(numeric_df) * 100,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "min_outlier": numeric_df.loc[outlier_mask, column].min() if not outlier_mask.empty else None,
                "max_outlier": numeric_df.loc[outlier_mask, column].max() if not outlier_mask.empty else None,
                "indices": outlier_indices[:100]  # Limit to 100 indices
            }
        
        outliers["iqr_method"] = iqr_outliers
        
        # Method 2: Z-score method
        z_score_outliers = {}
        
        for column in numeric_df.columns:
            mean = numeric_df[column].mean()
            std = numeric_df[column].std()
            
            if std == 0:  # Skip columns with zero standard deviation
                continue
            
            z_scores = (numeric_df[column] - mean) / std
            
            outlier_mask = (z_scores.abs() > 3)  # Z-score > 3 or < -3
            outlier_indices = outlier_mask[outlier_mask].index.tolist()
            
            z_score_outliers[column] = {
                "count": len(outlier_indices),
                "percent": len(outlier_indices) / len(numeric_df) * 100,
                "lower_bound": mean - 3 * std,
                "upper_bound": mean + 3 * std,
                "min_outlier": numeric_df.loc[outlier_mask, column].min() if not outlier_mask.empty else None,
                "max_outlier": numeric_df.loc[outlier_mask, column].max() if not outlier_mask.empty else None,
                "indices": outlier_indices[:100]  # Limit to 100 indices
            }
        
        outliers["z_score_method"] = z_score_outliers
        
        # Method 3: Isolation Forest (multivariate)
        try:
            # Prepare data
            X = numeric_df.copy()
            
            # Handle missing values
            X = X.fillna(X.mean())
            
            # Apply Isolation Forest
            iso_forest = IsolationForest(contamination=0.05, random_state=42)
            outlier_predictions = iso_forest.fit_predict(X)
            
            # Get outlier indices
            outlier_mask = (outlier_predictions == -1)
            outlier_indices = np.where(outlier_mask)[0].tolist()
            
            outliers["isolation_forest"] = {
                "count": len(outlier_indices),
                "percent": len(outlier_indices) / len(numeric_df) * 100,
                "indices": outlier_indices[:100]  # Limit to 100 indices
            }
        except Exception as e:
            outliers["isolation_forest"] = {"error": str(e)}
        
        # Summary
        outliers["summary"] = {
            "total_columns_analyzed": len(numeric_df.columns),
            "columns_with_iqr_outliers": sum(1 for col in iqr_outliers if iqr_outliers[col]["count"] > 0),
            "columns_with_z_score_outliers": sum(1 for col in z_score_outliers if z_score_outliers[col]["count"] > 0),
            "multivariate_outliers_count": outliers.get("isolation_forest", {}).get("count", 0)
        }
        
        return outliers
    
    def _analyze_feature_importance(self, df: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """
        Analyze feature importance with respect to a target column.
        
        Args:
            df: DataFrame to analyze.
            target_column: Name of the target column.
            
        Returns:
            Dictionary containing feature importance analysis results.
        """
        if target_column not in df.columns:
            return {"error": f"Target column '{target_column}' not found in the dataset"}
        
        # Initialize results
        importance = {}
        
        # Get target and feature columns
        y = df[target_column]
        
        # Handle different target types
        is_classification = False
        
        if not pd.api.types.is_numeric_dtype(y):
            is_classification = True
        elif y.nunique() < 10 and all(y.dropna() == y.dropna().astype(int)):
            is_classification = True
        
        # Get numeric feature columns (excluding target)
        numeric_features = df.select_dtypes(include=["number"]).columns.tolist()
        if target_column in numeric_features:
            numeric_features.remove(target_column)
        
        if not numeric_features:
            return {"error": "No numeric feature columns found for importance analysis"}
        
        # Prepare feature data
        X = df[numeric_features].copy()
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Method 1: Correlation with target (for regression)
        if not is_classification and pd.api.types.is_numeric_dtype(y):
            # Calculate correlations
            correlations = {}
            
            for feature in numeric_features:
                corr = df[[feature, target_column]].corr().iloc[0, 1]
                correlations[feature] = corr
            
            # Sort by absolute correlation
            sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
            
            importance["correlation"] = {
                "method": "Pearson correlation",
                "feature_importance": dict(sorted_correlations),
                "top_positive_features": dict(sorted(correlations.items(), key=lambda x: x[1], reverse=True)[:5]),
                "top_negative_features": dict(sorted(correlations.items(), key=lambda x: x[1])[:5])
            }
        
        # Method 2: Mutual Information
        try:
            # Calculate mutual information
            if is_classification:
                mi_scores = mutual_info_classif(X, y, random_state=42)
                method = "Mutual Information Classification"
            else:
                mi_scores = mutual_info_regression(X, y, random_state=42)
                method = "Mutual Information Regression"
            
            # Create dictionary of feature importance
            mi_importance = dict(zip(numeric_features, mi_scores))
            
            # Sort by importance
            sorted_mi = sorted(mi_importance.items(), key=lambda x: x[1], reverse=True)
            
            importance["mutual_information"] = {
                "method": method,
                "feature_importance": dict(sorted_mi),
                "top_features": dict(sorted_mi[:10])
            }
        except Exception as e:
            importance["mutual_information"] = {"error": str(e)}
        
        # Method 3: Random Forest importance (if sklearn is available)
        try:
            from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
            
            # Train Random Forest
            if is_classification:
                model = RandomForestClassifier(n_estimators=50, random_state=42)
                model.fit(X, y)
                method = "Random Forest Classification"
            else:
                model = RandomForestRegressor(n_estimators=50, random_state=42)
                model.fit(X, y)
                method = "Random Forest Regression"
            
            # Get feature importance
            rf_importance = dict(zip(numeric_features, model.feature_importances_))
            
            # Sort by importance
            sorted_rf = sorted(rf_importance.items(), key=lambda x: x[1], reverse=True)
            
            importance["random_forest"] = {
                "method": method,
                "feature_importance": dict(sorted_rf),
                "top_features": dict(sorted_rf[:10])
            }
        except Exception as e:
            importance["random_forest"] = {"error": str(e)}
        
        # Summary
        top_features = set()
        
        # Collect top 5 features from each method
        for method in importance:
            if isinstance(importance[method], dict) and "feature_importance" in importance[method]:
                sorted_features = sorted(importance[method]["feature_importance"].items(), key=lambda x: abs(x[1]) if isinstance(x[1], (int, float)) else 0, reverse=True)
                top_features.update([feature for feature, _ in sorted_features[:5]])
        
        importance["summary"] = {
            "top_features_across_methods": list(top_features)
        }
        
        return importance
    
    def _perform_dimensionality_reduction(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform dimensionality reduction on the dataset.
        
        Args:
            df: DataFrame to analyze.
            
        Returns:
            Dictionary containing dimensionality reduction results.
        """
        # Initialize results
        dim_reduction = {}
        
        # Get numeric columns
        numeric_df = df.select_dtypes(include=["number"])
        
        if numeric_df.empty:
            return {"message": "No numeric columns found for dimensionality reduction"}
        
        if len(numeric_df.columns) < 2:
            return {"message": "At least 2 numeric columns are required for dimensionality reduction"}
        
        # Prepare data
        X = numeric_df.copy()
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Method 1: PCA
        try:
            # Standardize data
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Apply PCA
            n_components = min(len(X.columns), 10)  # Limit to 10 components
            pca = PCA(n_components=n_components)
            pca.fit(X_scaled)
            
            # Get explained variance
            explained_variance = pca.explained_variance_ratio_
            cumulative_variance = np.cumsum(explained_variance)
            
            # Get component loadings
            loadings = pca.components_
            
            # Create loadings dictionary
            loadings_dict = {}
            for i, component in enumerate(loadings):
                loadings_dict[f"PC{i+1}"] = dict(zip(X.columns, component))
            
            # Determine optimal number of components
            optimal_n_components = np.argmax(cumulative_variance >= 0.8) + 1
            if optimal_n_components == 0:  # If no component explains 80% variance
                optimal_n_components = len(cumulative_variance)
            
            dim_reduction["pca"] = {
                "n_components": n_components,
                "explained_variance": dict(zip([f"PC{i+1}" for i in range(n_components)], explained_variance)),
                "cumulative_variance": dict(zip([f"PC{i+1}" for i in range(n_components)], cumulative_variance)),
                "loadings": loadings_dict,
                "optimal_n_components": optimal_n_components,
                "optimal_variance_explained": cumulative_variance[optimal_n_components-1]
            }
            
            # Get top contributing features for each component
            top_features = {}
            for i, component in enumerate(loadings):
                # Get absolute loadings
                abs_loadings = np.abs(component)
                
                # Get indices of top 5 loadings
                top_indices = abs_loadings.argsort()[-5:][::-1]
                
                # Get corresponding features and loadings
                top_features[f"PC{i+1}"] = {
                    X.columns[idx]: component[idx] for idx in top_indices
                }
            
            dim_reduction["pca"]["top_features"] = top_features
        except Exception as e:
            dim_reduction["pca"] = {"error": str(e)}
        
        return dim_reduction
    
    def _perform_clustering(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform clustering analysis on the dataset.
        
        Args:
            df: DataFrame to analyze.
            
        Returns:
            Dictionary containing clustering analysis results.
        """
        # Initialize results
        clustering = {}
        
        # Get numeric columns
        numeric_df = df.select_dtypes(include=["number"])
        
        if numeric_df.empty:
            return {"message": "No numeric columns found for clustering analysis"}
        
        # Prepare data
        X = numeric_df.copy()
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Standardize data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Method 1: K-means
        try:
            # Determine optimal number of clusters using elbow method
            inertia = []
            max_clusters = min(10, len(X) // 10)  # Limit to 10 clusters or 1/10 of data points
            
            for k in range(2, max_clusters + 1):
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                kmeans.fit(X_scaled)
                inertia.append(kmeans.inertia_)
            
            # Calculate elbow point (using second derivative)
            if len(inertia) > 2:
                second_derivative = np.diff(np.diff(inertia))
                elbow_point = np.argmax(second_derivative) + 2
            else:
                elbow_point = 2
            
            # Apply K-means with optimal number of clusters
            kmeans = KMeans(n_clusters=elbow_point, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(X_scaled)
            
            # Get cluster centers
            cluster_centers = kmeans.cluster_centers_
            
            # Transform back to original scale
            cluster_centers_original = scaler.inverse_transform(cluster_centers)
            
            # Create cluster centers dictionary
            centers_dict = {}
            for i, center in enumerate(cluster_centers_original):
                centers_dict[f"Cluster_{i+1}"] = dict(zip(X.columns, center))
            
            # Get cluster sizes
            cluster_sizes = pd.Series(cluster_labels).value_counts().to_dict()
            
            # Calculate cluster statistics
            cluster_stats = {}
            for i in range(elbow_point):
                cluster_df = X.iloc[cluster_labels == i]
                
                if not cluster_df.empty:
                    cluster_stats[f"Cluster_{i+1}"] = {
                        "size": len(cluster_df),
                        "percent": len(cluster_df) / len(X) * 100,
                        "mean": cluster_df.mean().to_dict(),
                        "std": cluster_df.std().to_dict()
                    }
            
            clustering["kmeans"] = {
                "optimal_n_clusters": elbow_point,
                "inertia": dict(zip(range(2, max_clusters + 1), inertia)),
                "cluster_centers": centers_dict,
                "cluster_sizes": {f"Cluster_{k+1}": v for k, v in cluster_sizes.items()},
                "cluster_statistics": cluster_stats
            }
        except Exception as e:
            clustering["kmeans"] = {"error": str(e)}
        
        # Method 2: DBSCAN
        try:
            # Apply DBSCAN
            dbscan = DBSCAN(eps=0.5, min_samples=5)
            dbscan_labels = dbscan.fit_predict(X_scaled)
            
            # Get number of clusters (excluding noise points labeled as -1)
            n_clusters = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
            
            # Get cluster sizes
            dbscan_sizes = pd.Series(dbscan_labels).value_counts().to_dict()
            
            # Calculate cluster statistics
            dbscan_stats = {}
            for label in set(dbscan_labels):
                if label != -1:  # Skip noise points
                    cluster_df = X.iloc[dbscan_labels == label]
                    
                    if not cluster_df.empty:
                        dbscan_stats[f"Cluster_{label+1}"] = {
                            "size": len(cluster_df),
                            "percent": len(cluster_df) / len(X) * 100,
                            "mean": cluster_df.mean().to_dict(),
                            "std": cluster_df.std().to_dict()
                        }
            
            # Calculate noise points statistics
            noise_df = X.iloc[dbscan_labels == -1]
            noise_stats = {
                "size": len(noise_df),
                "percent": len(noise_df) / len(X) * 100
            }
            
            clustering["dbscan"] = {
                "n_clusters": n_clusters,
                "cluster_sizes": {f"Cluster_{k+1}" if k != -1 else "Noise": v for k, v in dbscan_sizes.items()},
                "cluster_statistics": dbscan_stats,
                "noise_statistics": noise_stats
            }
        except Exception as e:
            clustering["dbscan"] = {"error": str(e)}
        
        return clustering
    
    def _calculate_entropy(self, probabilities: pd.Series) -> float:
        """
        Calculate entropy of a probability distribution.
        
        Args:
            probabilities: Series of probabilities.
            
        Returns:
            Entropy value.
        """
        return -np.sum(probabilities * np.log2(probabilities))
    
    def generate_insights(self) -> List[Dict[str, Any]]:
        """
        Generate insights from the analysis results.
        
        Returns:
            List of insights.
        """
        if not self.analysis_results:
            raise ValueError("No analysis results available. Run analyze() first.")
        
        # Initialize insights
        insights = []
        
        # 1. Missing values insights
        if "statistical_analysis" in self.analysis_results:
            stats = self.analysis_results["statistical_analysis"]
            
            # Check for columns with high missing values
            if "numeric" in stats:
                for column, col_stats in stats["numeric"].items():
                    if "count" in col_stats and col_stats["count"] < self.analysis_results["dataset_info"]["num_rows"]:
                        missing_percent = (self.analysis_results["dataset_info"]["num_rows"] - col_stats["count"]) / self.analysis_results["dataset_info"]["num_rows"] * 100
                        
                        if missing_percent > 20:
                            insights.append({
                                "type": "missing_values",
                                "column": column,
                                "missing_percent": missing_percent,
                                "severity": "high" if missing_percent > 50 else "medium",
                                "description": f"Column '{column}' has {missing_percent:.1f}% missing values",
                                "recommendation": "Consider imputing missing values or dropping the column if not essential"
                            })
        
        # 2. Outlier insights
        if "outlier_detection" in self.analysis_results:
            outliers = self.analysis_results["outlier_detection"]
            
            if "iqr_method" in outliers:
                for column, outlier_stats in outliers["iqr_method"].items():
                    if outlier_stats["percent"] > 5:
                        insights.append({
                            "type": "outliers",
                            "column": column,
                            "outlier_percent": outlier_stats["percent"],
                            "severity": "high" if outlier_stats["percent"] > 10 else "medium",
                            "description": f"Column '{column}' has {outlier_stats['percent']:.1f}% outliers",
                            "recommendation": "Consider capping, transforming, or investigating these outliers"
                        })
        
        # 3. Correlation insights
        if "statistical_analysis" in self.analysis_results and "correlation" in self.analysis_results["statistical_analysis"]:
            correlation = self.analysis_results["statistical_analysis"]["correlation"]
            
            if "highly_correlated_pairs" in correlation:
                for pair in correlation["highly_correlated_pairs"]:
                    insights.append({
                        "type": "correlation",
                        "columns": [pair["column1"], pair["column2"]],
                        "correlation": pair["correlation"],
                        "severity": "high" if abs(pair["correlation"]) > 0.9 else "medium",
                        "description": f"Strong {pair['strength']} correlation ({pair['correlation']:.2f}) between '{pair['column1']}' and '{pair['column2']}'",
                        "recommendation": "Consider removing one of these features to reduce multicollinearity"
                    })
        
        # 4. Feature importance insights
        if "feature_importance" in self.analysis_results:
            importance = self.analysis_results["feature_importance"]
            
            if "summary" in importance and "top_features_across_methods" in importance["summary"]:
                top_features = importance["summary"]["top_features_across_methods"]
                
                if top_features:
                    insights.append({
                        "type": "feature_importance",
                        "top_features": top_features[:5],
                        "severity": "info",
                        "description": f"Top important features: {', '.join(top_features[:5])}",
                        "recommendation": "Focus on these features for modeling and further analysis"
                    })
        
        # 5. Dimensionality reduction insights
        if "dimensionality_reduction" in self.analysis_results and "pca" in self.analysis_results["dimensionality_reduction"]:
            pca = self.analysis_results["dimensionality_reduction"]["pca"]
            
            if "optimal_n_components" in pca and "optimal_variance_explained" in pca:
                insights.append({
                    "type": "dimensionality_reduction",
                    "optimal_components": pca["optimal_n_components"],
                    "variance_explained": pca["optimal_variance_explained"] * 100,
                    "severity": "info",
                    "description": f"{pca['optimal_n_components']} principal components explain {pca['optimal_variance_explained']*100:.1f}% of variance",
                    "recommendation": f"Consider reducing dimensionality to {pca['optimal_n_components']} components"
                })
        
        # 6. Clustering insights
        if "clustering" in self.analysis_results and "kmeans" in self.analysis_results["clustering"]:
            kmeans = self.analysis_results["clustering"]["kmeans"]
            
            if "optimal_n_clusters" in kmeans and "cluster_sizes" in kmeans:
                insights.append({
                    "type": "clustering",
                    "optimal_clusters": kmeans["optimal_n_clusters"],
                    "cluster_sizes": kmeans["cluster_sizes"],
                    "severity": "info",
                    "description": f"Data can be segmented into {kmeans['optimal_n_clusters']} distinct clusters",
                    "recommendation": "Consider using these clusters for segmentation or as features"
                })
        
        # 7. Imbalance insights
        if "statistical_analysis" in self.analysis_results and "categorical" in self.analysis_results["statistical_analysis"]:
            categorical = self.analysis_results["statistical_analysis"]["categorical"]
            
            for column, cat_stats in categorical.items():
                if "is_imbalanced" in cat_stats and cat_stats["is_imbalanced"]:
                    insights.append({
                        "type": "imbalance",
                        "column": column,
                        "imbalance_ratio": cat_stats["imbalance_ratio"],
                        "severity": "high" if cat_stats["imbalance_ratio"] > 20 else "medium",
                        "description": f"Column '{column}' is imbalanced with ratio {cat_stats['imbalance_ratio']:.1f}",
                        "recommendation": "Consider resampling techniques if this is a target variable"
                    })
        
        # 8. Skewness insights
        if "statistical_analysis" in self.analysis_results and "numeric" in self.analysis_results["statistical_analysis"]:
            numeric = self.analysis_results["statistical_analysis"]["numeric"]
            
            for column, num_stats in numeric.items():
                if "skewness" in num_stats and abs(num_stats["skewness"]) > 1:
                    skew_direction = "right" if num_stats["skewness"] > 0 else "left"
                    
                    insights.append({
                        "type": "skewness",
                        "column": column,
                        "skewness": num_stats["skewness"],
                        "severity": "medium",
                        "description": f"Column '{column}' is {skew_direction}-skewed (skewness: {num_stats['skewness']:.2f})",
                        "recommendation": f"Consider applying {'log or sqrt' if skew_direction == 'right' else 'square or cube'} transformation"
                    })
        
        # Sort insights by severity
        severity_order = {"high": 0, "medium": 1, "info": 2}
        insights.sort(key=lambda x: severity_order.get(x.get("severity", "info"), 3))
        
        return insights
    
    def recommend_preprocessing(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Recommend preprocessing steps based on the analysis results.
        
        Returns:
            Dictionary of preprocessing recommendations.
        """
        if not self.analysis_results:
            raise ValueError("No analysis results available. Run analyze() first.")
        
        # Initialize recommendations
        recommendations = {
            "missing_values": [],
            "outliers": [],
            "encoding": [],
            "scaling": [],
            "feature_engineering": [],
            "feature_selection": [],
            "dimensionality_reduction": [],
            "transformations": []
        }
        
        # 1. Missing values recommendations
        if "statistical_analysis" in self.analysis_results:
            stats = self.analysis_results["statistical_analysis"]
            
            # Check numeric columns
            if "numeric" in stats:
                for column, col_stats in stats["numeric"].items():
                    if "count" in col_stats and col_stats["count"] < self.analysis_results["dataset_info"]["num_rows"]:
                        missing_percent = (self.analysis_results["dataset_info"]["num_rows"] - col_stats["count"]) / self.analysis_results["dataset_info"]["num_rows"] * 100
                        
                        if missing_percent > 50:
                            recommendations["missing_values"].append({
                                "column": column,
                                "missing_percent": missing_percent,
                                "recommendation": "drop_column",
                                "description": f"Drop column '{column}' due to high missing values ({missing_percent:.1f}%)"
                            })
                        elif missing_percent > 0:
                            # Recommend imputation method based on distribution
                            if "skewness" in col_stats and abs(col_stats["skewness"]) > 1:
                                recommendations["missing_values"].append({
                                    "column": column,
                                    "missing_percent": missing_percent,
                                    "recommendation": "impute_median",
                                    "description": f"Impute missing values in '{column}' with median due to skewed distribution"
                                })
                            else:
                                recommendations["missing_values"].append({
                                    "column": column,
                                    "missing_percent": missing_percent,
                                    "recommendation": "impute_mean",
                                    "description": f"Impute missing values in '{column}' with mean"
                                })
            
            # Check categorical columns
            if "categorical" in stats:
                for column, cat_stats in stats["categorical"].items():
                    if "count" in cat_stats and cat_stats["count"] < self.analysis_results["dataset_info"]["num_rows"]:
                        missing_percent = (self.analysis_results["dataset_info"]["num_rows"] - cat_stats["count"]) / self.analysis_results["dataset_info"]["num_rows"] * 100
                        
                        if missing_percent > 50:
                            recommendations["missing_values"].append({
                                "column": column,
                                "missing_percent": missing_percent,
                                "recommendation": "drop_column",
                                "description": f"Drop column '{column}' due to high missing values ({missing_percent:.1f}%)"
                            })
                        elif missing_percent > 0:
                            recommendations["missing_values"].append({
                                "column": column,
                                "missing_percent": missing_percent,
                                "recommendation": "impute_mode",
                                "description": f"Impute missing values in '{column}' with mode (most frequent value)"
                            })
        
        # 2. Outlier recommendations
        if "outlier_detection" in self.analysis_results:
            outliers = self.analysis_results["outlier_detection"]
            
            if "iqr_method" in outliers:
                for column, outlier_stats in outliers["iqr_method"].items():
                    if outlier_stats["percent"] > 10:
                        recommendations["outliers"].append({
                            "column": column,
                            "outlier_percent": outlier_stats["percent"],
                            "recommendation": "winsorize",
                            "description": f"Winsorize outliers in '{column}' (cap at {outlier_stats['lower_bound']:.2f} and {outlier_stats['upper_bound']:.2f})"
                        })
                    elif outlier_stats["percent"] > 5:
                        recommendations["outliers"].append({
                            "column": column,
                            "outlier_percent": outlier_stats["percent"],
                            "recommendation": "investigate",
                            "description": f"Investigate outliers in '{column}' ({outlier_stats['count']} outliers detected)"
                        })
        
        # 3. Encoding recommendations
        if "statistical_analysis" in self.analysis_results and "categorical" in self.analysis_results["statistical_analysis"]:
            categorical = self.analysis_results["statistical_analysis"]["categorical"]
            
            for column, cat_stats in categorical.items():
                if "unique" in cat_stats:
                    if cat_stats["unique"] == 2:
                        recommendations["encoding"].append({
                            "column": column,
                            "unique_values": cat_stats["unique"],
                            "recommendation": "binary_encoding",
                            "description": f"Apply binary encoding to '{column}' (2 unique values)"
                        })
                    elif cat_stats["unique"] <= 10:
                        recommendations["encoding"].append({
                            "column": column,
                            "unique_values": cat_stats["unique"],
                            "recommendation": "one_hot_encoding",
                            "description": f"Apply one-hot encoding to '{column}' ({cat_stats['unique']} unique values)"
                        })
                    elif cat_stats["unique"] <= 50:
                        recommendations["encoding"].append({
                            "column": column,
                            "unique_values": cat_stats["unique"],
                            "recommendation": "label_encoding",
                            "description": f"Apply label encoding to '{column}' ({cat_stats['unique']} unique values)"
                        })
                    else:
                        recommendations["encoding"].append({
                            "column": column,
                            "unique_values": cat_stats["unique"],
                            "recommendation": "target_encoding",
                            "description": f"Apply target encoding to '{column}' (high cardinality with {cat_stats['unique']} unique values)"
                        })
        
        # 4. Scaling recommendations
        if "statistical_analysis" in self.analysis_results and "numeric" in self.analysis_results["statistical_analysis"]:
            numeric = self.analysis_results["statistical_analysis"]["numeric"]
            
            for column, num_stats in numeric.items():
                if "std" in num_stats and num_stats["std"] > 0:
                    # Check for outliers
                    has_outliers = False
                    if "outlier_detection" in self.analysis_results and "iqr_method" in self.analysis_results["outlier_detection"]:
                        if column in self.analysis_results["outlier_detection"]["iqr_method"]:
                            has_outliers = self.analysis_results["outlier_detection"]["iqr_method"][column]["percent"] > 5
                    
                    # Check for skewness
                    is_skewed = False
                    if "skewness" in num_stats:
                        is_skewed = abs(num_stats["skewness"]) > 1
                    
                    if has_outliers:
                        recommendations["scaling"].append({
                            "column": column,
                            "recommendation": "robust_scaling",
                            "description": f"Apply robust scaling to '{column}' due to presence of outliers"
                        })
                    elif is_skewed:
                        recommendations["scaling"].append({
                            "column": column,
                            "recommendation": "min_max_scaling",
                            "description": f"Apply min-max scaling to '{column}' due to skewed distribution"
                        })
                    else:
                        recommendations["scaling"].append({
                            "column": column,
                            "recommendation": "standard_scaling",
                            "description": f"Apply standard scaling to '{column}'"
                        })
        
        # 5. Feature engineering recommendations
        if "statistical_analysis" in self.analysis_results:
            # Recommend polynomial features for highly correlated features
            if "correlation" in self.analysis_results["statistical_analysis"] and "highly_correlated_pairs" in self.analysis_results["statistical_analysis"]["correlation"]:
                correlated_pairs = self.analysis_results["statistical_analysis"]["correlation"]["highly_correlated_pairs"]
                
                if correlated_pairs:
                    # Get unique columns from correlated pairs
                    correlated_columns = set()
                    for pair in correlated_pairs:
                        correlated_columns.add(pair["column1"])
                        correlated_columns.add(pair["column2"])
                    
                    if len(correlated_columns) >= 2:
                        recommendations["feature_engineering"].append({
                            "columns": list(correlated_columns),
                            "recommendation": "polynomial_features",
                            "description": f"Create polynomial features from correlated columns: {', '.join(list(correlated_columns)[:5])}"
                        })
            
            # Recommend datetime features for datetime columns
            if "datetime" in self.analysis_results["statistical_analysis"]:
                datetime_columns = list(self.analysis_results["statistical_analysis"]["datetime"].keys())
                
                for column in datetime_columns:
                    recommendations["feature_engineering"].append({
                        "column": column,
                        "recommendation": "datetime_features",
                        "description": f"Extract datetime features from '{column}' (year, month, day, weekday, etc.)"
                    })
        
        # 6. Feature selection recommendations
        if "feature_importance" in self.analysis_results and "summary" in self.analysis_results["feature_importance"]:
            if "top_features_across_methods" in self.analysis_results["feature_importance"]["summary"]:
                top_features = self.analysis_results["feature_importance"]["summary"]["top_features_across_methods"]
                
                if top_features:
                    recommendations["feature_selection"].append({
                        "columns": top_features,
                        "recommendation": "select_top_features",
                        "description": f"Select top important features: {', '.join(top_features[:5])}"
                    })
        
        # 7. Dimensionality reduction recommendations
        if "dimensionality_reduction" in self.analysis_results and "pca" in self.analysis_results["dimensionality_reduction"]:
            pca = self.analysis_results["dimensionality_reduction"]["pca"]
            
            if "optimal_n_components" in pca and "optimal_variance_explained" in pca:
                if pca["optimal_n_components"] < len(self.analysis_results["dataset_info"]["column_types"]["numeric"]) * 0.5:
                    recommendations["dimensionality_reduction"].append({
                        "n_components": pca["optimal_n_components"],
                        "variance_explained": pca["optimal_variance_explained"] * 100,
                        "recommendation": "apply_pca",
                        "description": f"Apply PCA to reduce dimensionality to {pca['optimal_n_components']} components ({pca['optimal_variance_explained']*100:.1f}% variance explained)"
                    })
        
        # 8. Transformation recommendations
        if "statistical_analysis" in self.analysis_results and "numeric" in self.analysis_results["statistical_analysis"]:
            numeric = self.analysis_results["statistical_analysis"]["numeric"]
            
            for column, num_stats in numeric.items():
                if "skewness" in num_stats:
                    if num_stats["skewness"] > 1:  # Right-skewed
                        recommendations["transformations"].append({
                            "column": column,
                            "skewness": num_stats["skewness"],
                            "recommendation": "log_transform",
                            "description": f"Apply log transformation to '{column}' to reduce right skewness ({num_stats['skewness']:.2f})"
                        })
                    elif num_stats["skewness"] < -1:  # Left-skewed
                        recommendations["transformations"].append({
                            "column": column,
                            "skewness": num_stats["skewness"],
                            "recommendation": "square_transform",
                            "description": f"Apply square transformation to '{column}' to reduce left skewness ({num_stats['skewness']:.2f})"
                        })
        
        return recommendations
    
    def recommend_models(self, task_type: str) -> List[Dict[str, Any]]:
        """
        Recommend models based on the analysis results and task type.
        
        Args:
            task_type: Type of machine learning task ('classification', 'regression', 'clustering', etc.).
            
        Returns:
            List of model recommendations.
        """
        if not self.analysis_results:
            raise ValueError("No analysis results available. Run analyze() first.")
        
        # Initialize recommendations
        model_recommendations = []
        
        # Get dataset characteristics
        n_rows = self.analysis_results["dataset_info"]["num_rows"]
        n_numeric = self.analysis_results["dataset_info"]["column_types"]["numeric"]
        n_categorical = self.analysis_results["dataset_info"]["column_types"]["categorical"]
        
        # Check for high dimensionality
        high_dimensionality = n_numeric > 50
        
        # Check for multicollinearity
        has_multicollinearity = False
        if "statistical_analysis" in self.analysis_results and "correlation" in self.analysis_results["statistical_analysis"]:
            if "highly_correlated_pairs" in self.analysis_results["statistical_analysis"]["correlation"]:
                has_multicollinearity = len(self.analysis_results["statistical_analysis"]["correlation"]["highly_correlated_pairs"]) > 0
        
        # Check for outliers
        has_outliers = False
        if "outlier_detection" in self.analysis_results and "summary" in self.analysis_results["outlier_detection"]:
            if "columns_with_iqr_outliers" in self.analysis_results["outlier_detection"]["summary"]:
                has_outliers = self.analysis_results["outlier_detection"]["summary"]["columns_with_iqr_outliers"] > 0
        
        # Check for imbalanced target
        has_imbalanced_target = False
        if "statistical_analysis" in self.analysis_results and "categorical" in self.analysis_results["statistical_analysis"]:
            for column, cat_stats in self.analysis_results["statistical_analysis"]["categorical"].items():
                if "is_imbalanced" in cat_stats and cat_stats["is_imbalanced"]:
                    has_imbalanced_target = True
                    break
        
        # Recommend models based on task type and dataset characteristics
        if task_type.lower() == "classification":
            # Linear models
            if not has_outliers and not high_dimensionality:
                model_recommendations.append({
                    "model": "LogisticRegression",
                    "suitability": "high" if not has_multicollinearity else "medium",
                    "description": "Good baseline model with interpretable results",
                    "hyperparameters": {
                        "C": [0.01, 0.1, 1.0, 10.0],
                        "penalty": ["l1", "l2"],
                        "solver": ["liblinear", "saga"]
                    }
                })
            
            # Tree-based models
            model_recommendations.append({
                "model": "RandomForest",
                "suitability": "high",
                "description": "Robust to outliers and multicollinearity, handles non-linear relationships well",
                "hyperparameters": {
                    "n_estimators": [100, 200, 500],
                    "max_depth": [None, 10, 20, 30],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4]
                }
            })
            
            model_recommendations.append({
                "model": "GradientBoosting",
                "suitability": "high",
                "description": "Often provides best performance, but may require more tuning",
                "hyperparameters": {
                    "n_estimators": [100, 200, 500],
                    "learning_rate": [0.01, 0.05, 0.1],
                    "max_depth": [3, 5, 7],
                    "subsample": [0.8, 1.0]
                }
            })
            
            # For imbalanced datasets
            if has_imbalanced_target:
                model_recommendations.append({
                    "model": "XGBoost",
                    "suitability": "high",
                    "description": "Handles imbalanced data well with scale_pos_weight parameter",
                    "hyperparameters": {
                        "n_estimators": [100, 200, 500],
                        "learning_rate": [0.01, 0.05, 0.1],
                        "max_depth": [3, 5, 7],
                        "scale_pos_weight": [1, 5, 10]
                    }
                })
            
            # For high dimensional data
            if high_dimensionality:
                model_recommendations.append({
                    "model": "SVM",
                    "suitability": "medium",
                    "description": "Can work well with high-dimensional data when using appropriate kernel",
                    "hyperparameters": {
                        "C": [0.1, 1.0, 10.0],
                        "kernel": ["linear", "rbf"],
                        "gamma": ["scale", "auto", 0.1, 0.01]
                    }
                })
            
            # Neural networks for complex relationships
            if n_rows > 1000:
                model_recommendations.append({
                    "model": "NeuralNetwork",
                    "suitability": "medium",
                    "description": "Can capture complex patterns but requires more data and tuning",
                    "hyperparameters": {
                        "hidden_layer_sizes": [[50], [100], [50, 50], [100, 50]],
                        "activation": ["relu", "tanh"],
                        "alpha": [0.0001, 0.001, 0.01],
                        "learning_rate": ["constant", "adaptive"]
                    }
                })
        
        elif task_type.lower() == "regression":
            # Linear models
            if not has_outliers and not high_dimensionality:
                model_recommendations.append({
                    "model": "LinearRegression",
                    "suitability": "high" if not has_multicollinearity else "low",
                    "description": "Simple baseline model with interpretable results",
                    "hyperparameters": {}
                })
                
                model_recommendations.append({
                    "model": "Ridge",
                    "suitability": "high" if has_multicollinearity else "medium",
                    "description": "Handles multicollinearity well with L2 regularization",
                    "hyperparameters": {
                        "alpha": [0.1, 1.0, 10.0, 100.0]
                    }
                })
                
                model_recommendations.append({
                    "model": "Lasso",
                    "suitability": "high" if high_dimensionality else "medium",
                    "description": "Good for feature selection with L1 regularization",
                    "hyperparameters": {
                        "alpha": [0.001, 0.01, 0.1, 1.0]
                    }
                })
            
            # Tree-based models
            model_recommendations.append({
                "model": "RandomForest",
                "suitability": "high",
                "description": "Robust to outliers and multicollinearity, handles non-linear relationships well",
                "hyperparameters": {
                    "n_estimators": [100, 200, 500],
                    "max_depth": [None, 10, 20, 30],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4]
                }
            })
            
            model_recommendations.append({
                "model": "GradientBoosting",
                "suitability": "high",
                "description": "Often provides best performance, but may require more tuning",
                "hyperparameters": {
                    "n_estimators": [100, 200, 500],
                    "learning_rate": [0.01, 0.05, 0.1],
                    "max_depth": [3, 5, 7],
                    "subsample": [0.8, 1.0]
                }
            })
            
            # For outliers
            if has_outliers:
                model_recommendations.append({
                    "model": "HuberRegressor",
                    "suitability": "high",
                    "description": "Robust to outliers with Huber loss function",
                    "hyperparameters": {
                        "epsilon": [1.1, 1.35, 1.5],
                        "alpha": [0.0001, 0.001, 0.01]
                    }
                })
            
            # For high dimensional data
            if high_dimensionality:
                model_recommendations.append({
                    "model": "ElasticNet",
                    "suitability": "high",
                    "description": "Combines L1 and L2 regularization, good for high-dimensional data",
                    "hyperparameters": {
                        "alpha": [0.001, 0.01, 0.1, 1.0],
                        "l1_ratio": [0.1, 0.5, 0.7, 0.9]
                    }
                })
            
            # Neural networks for complex relationships
            if n_rows > 1000:
                model_recommendations.append({
                    "model": "NeuralNetwork",
                    "suitability": "medium",
                    "description": "Can capture complex patterns but requires more data and tuning",
                    "hyperparameters": {
                        "hidden_layer_sizes": [[50], [100], [50, 50], [100, 50]],
                        "activation": ["relu", "tanh"],
                        "alpha": [0.0001, 0.001, 0.01],
                        "learning_rate": ["constant", "adaptive"]
                    }
                })
        
        elif task_type.lower() == "clustering":
            # K-means
            model_recommendations.append({
                "model": "KMeans",
                "suitability": "high" if not has_outliers else "medium",
                "description": "Fast and simple clustering algorithm, but sensitive to outliers",
                "hyperparameters": {
                    "n_clusters": list(range(2, 11)),
                    "init": ["k-means++", "random"],
                    "n_init": [10, 20]
                }
            })
            
            # DBSCAN for irregular clusters
            model_recommendations.append({
                "model": "DBSCAN",
                "suitability": "high" if has_outliers else "medium",
                "description": "Handles outliers well and can find clusters of arbitrary shape",
                "hyperparameters": {
                    "eps": [0.1, 0.5, 1.0],
                    "min_samples": [5, 10, 20]
                }
            })
            
            # Hierarchical clustering
            model_recommendations.append({
                "model": "AgglomerativeClustering",
                "suitability": "medium",
                "description": "Provides hierarchical structure of clusters",
                "hyperparameters": {
                    "n_clusters": list(range(2, 11)),
                    "linkage": ["ward", "complete", "average"]
                }
            })
            
            # Gaussian Mixture Models
            model_recommendations.append({
                "model": "GaussianMixture",
                "suitability": "medium",
                "description": "Soft clustering with probability of membership to each cluster",
                "hyperparameters": {
                    "n_components": list(range(2, 11)),
                    "covariance_type": ["full", "tied", "diag", "spherical"]
                }
            })
        
        # Sort recommendations by suitability
        suitability_order = {"high": 0, "medium": 1, "low": 2}
        model_recommendations.sort(key=lambda x: suitability_order.get(x.get("suitability", "low"), 3))
        
        return model_recommendations
    
    def generate_report(self, output_path: str) -> str:
        """
        Generate a comprehensive report from the analysis results.
        
        Args:
            output_path: Path to save the report.
            
        Returns:
            Path to the generated report.
        """
        if not self.analysis_results:
            raise ValueError("No analysis results available. Run analyze() first.")
        
        # Generate insights
        insights = self.generate_insights()
        
        # Generate preprocessing recommendations
        preprocessing = self.recommend_preprocessing()
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SBYB Data Analysis Report</title>
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
                .high {{
                    color: #e74c3c;
                    font-weight: bold;
                }}
                .medium {{
                    color: #f39c12;
                }}
                .low {{
                    color: #7f8c8d;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>SBYB Data Analysis Report</h1>
                <p>Generated on {self.analysis_results.get('dataset_info', {}).get('analysis_timestamp', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}</p>
                
                <div class="section">
                    <h2>Dataset Overview</h2>
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Number of Rows</td>
                            <td>{self.analysis_results.get('dataset_info', {}).get('num_rows', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Number of Columns</td>
                            <td>{self.analysis_results.get('dataset_info', {}).get('num_columns', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Numeric Columns</td>
                            <td>{self.analysis_results.get('dataset_info', {}).get('column_types', {}).get('numeric', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Categorical Columns</td>
                            <td>{self.analysis_results.get('dataset_info', {}).get('column_types', {}).get('categorical', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Datetime Columns</td>
                            <td>{self.analysis_results.get('dataset_info', {}).get('column_types', {}).get('datetime', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Boolean Columns</td>
                            <td>{self.analysis_results.get('dataset_info', {}).get('column_types', {}).get('boolean', 'N/A')}</td>
                        </tr>
                    </table>
                </div>
        """
        
        # Add insights section
        if insights:
            html_content += """
                <div class="section">
                    <h2>Key Insights</h2>
                    <table>
                        <tr>
                            <th>Type</th>
                            <th>Description</th>
                            <th>Recommendation</th>
                            <th>Severity</th>
                        </tr>
            """
            
            for insight in insights:
                html_content += f"""
                        <tr>
                            <td>{insight.get('type', 'N/A').replace('_', ' ').title()}</td>
                            <td>{insight.get('description', 'N/A')}</td>
                            <td>{insight.get('recommendation', 'N/A')}</td>
                            <td class="{insight.get('severity', 'info')}">{insight.get('severity', 'info').upper()}</td>
                        </tr>
                """
            
            html_content += """
                    </table>
                </div>
            """
        
        # Add preprocessing recommendations section
        if preprocessing:
            html_content += """
                <div class="section">
                    <h2>Preprocessing Recommendations</h2>
            """
            
            # Missing values
            if preprocessing.get('missing_values'):
                html_content += """
                    <h3>Missing Values</h3>
                    <table>
                        <tr>
                            <th>Column</th>
                            <th>Missing %</th>
                            <th>Recommendation</th>
                        </tr>
                """
                
                for rec in preprocessing.get('missing_values'):
                    html_content += f"""
                        <tr>
                            <td>{rec.get('column', 'N/A')}</td>
                            <td>{rec.get('missing_percent', 'N/A'):.1f}%</td>
                            <td>{rec.get('description', 'N/A')}</td>
                        </tr>
                    """
                
                html_content += """
                    </table>
                """
            
            # Outliers
            if preprocessing.get('outliers'):
                html_content += """
                    <h3>Outliers</h3>
                    <table>
                        <tr>
                            <th>Column</th>
                            <th>Outlier %</th>
                            <th>Recommendation</th>
                        </tr>
                """
                
                for rec in preprocessing.get('outliers'):
                    html_content += f"""
                        <tr>
                            <td>{rec.get('column', 'N/A')}</td>
                            <td>{rec.get('outlier_percent', 'N/A'):.1f}%</td>
                            <td>{rec.get('description', 'N/A')}</td>
                        </tr>
                    """
                
                html_content += """
                    </table>
                """
            
            # Encoding
            if preprocessing.get('encoding'):
                html_content += """
                    <h3>Categorical Encoding</h3>
                    <table>
                        <tr>
                            <th>Column</th>
                            <th>Unique Values</th>
                            <th>Recommendation</th>
                        </tr>
                """
                
                for rec in preprocessing.get('encoding'):
                    html_content += f"""
                        <tr>
                            <td>{rec.get('column', 'N/A')}</td>
                            <td>{rec.get('unique_values', 'N/A')}</td>
                            <td>{rec.get('description', 'N/A')}</td>
                        </tr>
                    """
                
                html_content += """
                    </table>
                """
            
            # Scaling
            if preprocessing.get('scaling'):
                html_content += """
                    <h3>Feature Scaling</h3>
                    <table>
                        <tr>
                            <th>Column</th>
                            <th>Recommendation</th>
                        </tr>
                """
                
                for rec in preprocessing.get('scaling'):
                    html_content += f"""
                        <tr>
                            <td>{rec.get('column', 'N/A')}</td>
                            <td>{rec.get('description', 'N/A')}</td>
                        </tr>
                    """
                
                html_content += """
                    </table>
                """
            
            # Transformations
            if preprocessing.get('transformations'):
                html_content += """
                    <h3>Feature Transformations</h3>
                    <table>
                        <tr>
                            <th>Column</th>
                            <th>Skewness</th>
                            <th>Recommendation</th>
                        </tr>
                """
                
                for rec in preprocessing.get('transformations'):
                    html_content += f"""
                        <tr>
                            <td>{rec.get('column', 'N/A')}</td>
                            <td>{rec.get('skewness', 'N/A'):.2f}</td>
                            <td>{rec.get('description', 'N/A')}</td>
                        </tr>
                    """
                
                html_content += """
                    </table>
                """
            
            # Feature engineering
            if preprocessing.get('feature_engineering'):
                html_content += """
                    <h3>Feature Engineering</h3>
                    <table>
                        <tr>
                            <th>Columns</th>
                            <th>Recommendation</th>
                        </tr>
                """
                
                for rec in preprocessing.get('feature_engineering'):
                    columns = rec.get('columns', rec.get('column', 'N/A'))
                    if isinstance(columns, list):
                        columns = ', '.join(columns[:5])
                    
                    html_content += f"""
                        <tr>
                            <td>{columns}</td>
                            <td>{rec.get('description', 'N/A')}</td>
                        </tr>
                    """
                
                html_content += """
                    </table>
                """
            
            # Feature selection
            if preprocessing.get('feature_selection'):
                html_content += """
                    <h3>Feature Selection</h3>
                    <table>
                        <tr>
                            <th>Columns</th>
                            <th>Recommendation</th>
                        </tr>
                """
                
                for rec in preprocessing.get('feature_selection'):
                    columns = rec.get('columns', rec.get('column', 'N/A'))
                    if isinstance(columns, list):
                        columns = ', '.join(columns[:5])
                    
                    html_content += f"""
                        <tr>
                            <td>{columns}</td>
                            <td>{rec.get('description', 'N/A')}</td>
                        </tr>
                    """
                
                html_content += """
                    </table>
                """
            
            # Dimensionality reduction
            if preprocessing.get('dimensionality_reduction'):
                html_content += """
                    <h3>Dimensionality Reduction</h3>
                    <table>
                        <tr>
                            <th>Method</th>
                            <th>Components</th>
                            <th>Variance Explained</th>
                            <th>Recommendation</th>
                        </tr>
                """
                
                for rec in preprocessing.get('dimensionality_reduction'):
                    html_content += f"""
                        <tr>
                            <td>PCA</td>
                            <td>{rec.get('n_components', 'N/A')}</td>
                            <td>{rec.get('variance_explained', 'N/A'):.1f}%</td>
                            <td>{rec.get('description', 'N/A')}</td>
                        </tr>
                    """
                
                html_content += """
                    </table>
                """
            
            html_content += """
                </div>
            """
        
        # Add statistical analysis section
        if "statistical_analysis" in self.analysis_results:
            html_content += """
                <div class="section">
                    <h2>Statistical Analysis</h2>
            """
            
            # Correlation analysis
            if "correlation" in self.analysis_results["statistical_analysis"] and "highly_correlated_pairs" in self.analysis_results["statistical_analysis"]["correlation"]:
                correlated_pairs = self.analysis_results["statistical_analysis"]["correlation"]["highly_correlated_pairs"]
                
                if correlated_pairs:
                    html_content += """
                        <h3>Highly Correlated Features</h3>
                        <table>
                            <tr>
                                <th>Feature 1</th>
                                <th>Feature 2</th>
                                <th>Correlation</th>
                                <th>Strength</th>
                            </tr>
                    """
                    
                    for pair in correlated_pairs:
                        html_content += f"""
                            <tr>
                                <td>{pair.get('column1', 'N/A')}</td>
                                <td>{pair.get('column2', 'N/A')}</td>
                                <td>{pair.get('correlation', 'N/A'):.2f}</td>
                                <td>{pair.get('strength', 'N/A')}</td>
                            </tr>
                        """
                    
                    html_content += """
                        </table>
                    """
            
            html_content += """
                </div>
            """
        
        # Add outlier detection section
        if "outlier_detection" in self.analysis_results and "summary" in self.analysis_results["outlier_detection"]:
            html_content += """
                <div class="section">
                    <h2>Outlier Detection</h2>
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
            """
            
            summary = self.analysis_results["outlier_detection"]["summary"]
            
            for key, value in summary.items():
                html_content += f"""
                        <tr>
                            <td>{key.replace('_', ' ').title()}</td>
                            <td>{value}</td>
                        </tr>
                """
            
            html_content += """
                    </table>
            """
            
            # Add details for columns with most outliers
            if "iqr_method" in self.analysis_results["outlier_detection"]:
                iqr_outliers = self.analysis_results["outlier_detection"]["iqr_method"]
                
                # Sort columns by outlier percentage
                sorted_columns = sorted(iqr_outliers.items(), key=lambda x: x[1].get("percent", 0), reverse=True)
                
                if sorted_columns:
                    html_content += """
                        <h3>Top Columns with Outliers (IQR Method)</h3>
                        <table>
                            <tr>
                                <th>Column</th>
                                <th>Outlier Count</th>
                                <th>Outlier Percent</th>
                                <th>Min Outlier</th>
                                <th>Max Outlier</th>
                            </tr>
                    """
                    
                    for column, stats in sorted_columns[:5]:  # Show top 5
                        html_content += f"""
                            <tr>
                                <td>{column}</td>
                                <td>{stats.get('count', 'N/A')}</td>
                                <td>{stats.get('percent', 'N/A'):.2f}%</td>
                                <td>{stats.get('min_outlier', 'N/A')}</td>
                                <td>{stats.get('max_outlier', 'N/A')}</td>
                            </tr>
                        """
                    
                    html_content += """
                        </table>
                    """
            
            html_content += """
                </div>
            """
        
        # Add feature importance section
        if "feature_importance" in self.analysis_results:
            html_content += """
                <div class="section">
                    <h2>Feature Importance</h2>
            """
            
            # Mutual information
            if "mutual_information" in self.analysis_results["feature_importance"] and "feature_importance" in self.analysis_results["feature_importance"]["mutual_information"]:
                mi_importance = self.analysis_results["feature_importance"]["mutual_information"]["feature_importance"]
                
                if mi_importance:
                    html_content += """
                        <h3>Mutual Information</h3>
                        <table>
                            <tr>
                                <th>Feature</th>
                                <th>Importance Score</th>
                            </tr>
                    """
                    
                    # Sort by importance
                    sorted_mi = sorted(mi_importance.items(), key=lambda x: x[1], reverse=True)
                    
                    for feature, score in sorted_mi[:10]:  # Show top 10
                        html_content += f"""
                            <tr>
                                <td>{feature}</td>
                                <td>{score:.4f}</td>
                            </tr>
                        """
                    
                    html_content += """
                        </table>
                    """
            
            # Random forest
            if "random_forest" in self.analysis_results["feature_importance"] and "feature_importance" in self.analysis_results["feature_importance"]["random_forest"]:
                rf_importance = self.analysis_results["feature_importance"]["random_forest"]["feature_importance"]
                
                if rf_importance:
                    html_content += """
                        <h3>Random Forest Importance</h3>
                        <table>
                            <tr>
                                <th>Feature</th>
                                <th>Importance Score</th>
                            </tr>
                    """
                    
                    # Sort by importance
                    sorted_rf = sorted(rf_importance.items(), key=lambda x: x[1], reverse=True)
                    
                    for feature, score in sorted_rf[:10]:  # Show top 10
                        html_content += f"""
                            <tr>
                                <td>{feature}</td>
                                <td>{score:.4f}</td>
                            </tr>
                        """
                    
                    html_content += """
                        </table>
                    """
            
            html_content += """
                </div>
            """
        
        # Add dimensionality reduction section
        if "dimensionality_reduction" in self.analysis_results and "pca" in self.analysis_results["dimensionality_reduction"]:
            pca = self.analysis_results["dimensionality_reduction"]["pca"]
            
            if "explained_variance" in pca and "loadings" in pca:
                html_content += """
                    <div class="section">
                        <h2>Dimensionality Reduction (PCA)</h2>
                        <h3>Explained Variance</h3>
                        <table>
                            <tr>
                                <th>Component</th>
                                <th>Explained Variance</th>
                                <th>Cumulative Variance</th>
                            </tr>
                """
                
                for i, (component, variance) in enumerate(pca["explained_variance"].items()):
                    cumulative = pca["cumulative_variance"].get(component, 0)
                    
                    html_content += f"""
                            <tr>
                                <td>{component}</td>
                                <td>{variance*100:.2f}%</td>
                                <td>{cumulative*100:.2f}%</td>
                            </tr>
                    """
                
                html_content += """
                        </table>
                        
                        <h3>Top Features by Component</h3>
                """
                
                if "top_features" in pca:
                    for component, features in pca["top_features"].items():
                        html_content += f"""
                            <h4>{component}</h4>
                            <table>
                                <tr>
                                    <th>Feature</th>
                                    <th>Loading</th>
                                </tr>
                        """
                        
                        for feature, loading in features.items():
                            html_content += f"""
                                <tr>
                                    <td>{feature}</td>
                                    <td>{loading:.4f}</td>
                                </tr>
                            """
                        
                        html_content += """
                            </table>
                        """
                
                html_content += """
                    </div>
                """
        
        # Add clustering section
        if "clustering" in self.analysis_results and "kmeans" in self.analysis_results["clustering"]:
            kmeans = self.analysis_results["clustering"]["kmeans"]
            
            if "optimal_n_clusters" in kmeans and "cluster_statistics" in kmeans:
                html_content += f"""
                    <div class="section">
                        <h2>Clustering Analysis</h2>
                        <h3>K-means Clustering (Optimal clusters: {kmeans["optimal_n_clusters"]})</h3>
                        <table>
                            <tr>
                                <th>Cluster</th>
                                <th>Size</th>
                                <th>Percent</th>
                            </tr>
                """
                
                for cluster, stats in kmeans["cluster_statistics"].items():
                    html_content += f"""
                            <tr>
                                <td>{cluster}</td>
                                <td>{stats.get('size', 'N/A')}</td>
                                <td>{stats.get('percent', 'N/A'):.2f}%</td>
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
