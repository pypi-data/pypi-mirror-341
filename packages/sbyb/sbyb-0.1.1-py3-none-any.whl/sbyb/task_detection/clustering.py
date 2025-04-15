"""
Clustering task detection for SBYB.

This module provides specialized components for detecting clustering tasks.
"""

from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import TaskDetectionError
from sbyb.core.utils import get_column_types


class ClusteringDetector(SBYBComponent):
    """
    Clustering task detection component.
    
    This component specializes in detecting clustering tasks and suggesting
    appropriate clustering algorithms.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the clustering detector.
        
        Args:
            config: Configuration dictionary for the detector.
        """
        super().__init__(config)
    
    def detect(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect if the data is suitable for clustering and suggest algorithms.
        
        Args:
            data: Input data.
            
        Returns:
            Dictionary with detection results:
                - is_clustering: Whether the task is suitable for clustering
                - confidence: Confidence score for the detection
                - suggested_algorithms: List of suggested clustering algorithms
                - details: Additional details about the detection
        """
        # Get column types
        column_types = get_column_types(data)
        numeric_columns = column_types['numeric']
        
        # Check if there are enough numeric features for clustering
        if len(numeric_columns) < 2:
            return {
                'is_clustering': False,
                'confidence': 0.8,
                'details': {
                    'reason': 'Not enough numeric features for clustering',
                    'n_numeric_features': len(numeric_columns)
                }
            }
        
        # Extract numeric data for analysis
        numeric_data = data[numeric_columns].copy()
        
        # Handle missing values for analysis
        numeric_data = numeric_data.fillna(numeric_data.mean())
        
        # Analyze data characteristics to suggest algorithms
        n_samples, n_features = numeric_data.shape
        
        # Standardize data for analysis
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_data)
        
        # Check for high-dimensional data
        is_high_dimensional = n_features > 10
        
        # Estimate data density
        try:
            # Use PCA to reduce dimensionality for density estimation
            if n_features > 2:
                pca = PCA(n_components=2)
                reduced_data = pca.fit_transform(scaled_data)
                explained_variance = pca.explained_variance_ratio_.sum()
            else:
                reduced_data = scaled_data
                explained_variance = 1.0
            
            # Calculate average distance between points as a density measure
            from scipy.spatial.distance import pdist
            distances = pdist(reduced_data)
            avg_distance = np.mean(distances)
            std_distance = np.std(distances)
            
            # Coefficient of variation as a measure of density variation
            cv_distance = std_distance / avg_distance if avg_distance > 0 else 0
            
            # Determine if data is likely to have well-separated clusters
            has_well_separated_clusters = cv_distance > 0.5
            
            # Suggest algorithms based on data characteristics
            suggested_algorithms = self._suggest_algorithms(
                n_samples=n_samples,
                n_features=n_features,
                is_high_dimensional=is_high_dimensional,
                has_well_separated_clusters=has_well_separated_clusters
            )
            
            return {
                'is_clustering': True,
                'confidence': 0.9,
                'suggested_algorithms': suggested_algorithms,
                'details': {
                    'n_samples': n_samples,
                    'n_features': n_features,
                    'is_high_dimensional': is_high_dimensional,
                    'pca_explained_variance': explained_variance,
                    'avg_distance': avg_distance,
                    'cv_distance': cv_distance,
                    'has_well_separated_clusters': has_well_separated_clusters
                }
            }
        
        except Exception as e:
            # If analysis fails, still return a basic result
            suggested_algorithms = self._suggest_algorithms(
                n_samples=n_samples,
                n_features=n_features,
                is_high_dimensional=is_high_dimensional,
                has_well_separated_clusters=None
            )
            
            return {
                'is_clustering': True,
                'confidence': 0.7,
                'suggested_algorithms': suggested_algorithms,
                'details': {
                    'n_samples': n_samples,
                    'n_features': n_features,
                    'is_high_dimensional': is_high_dimensional,
                    'note': 'Detailed analysis failed, using basic suggestions',
                    'error': str(e)
                }
            }
    
    def _suggest_algorithms(self, n_samples: int, n_features: int, 
                           is_high_dimensional: bool, 
                           has_well_separated_clusters: Optional[bool]) -> List[Dict[str, Any]]:
        """
        Suggest clustering algorithms based on data characteristics.
        
        Args:
            n_samples: Number of samples in the data.
            n_features: Number of features in the data.
            is_high_dimensional: Whether the data is high-dimensional.
            has_well_separated_clusters: Whether the data has well-separated clusters.
            
        Returns:
            List of suggested algorithms with their parameters.
        """
        suggestions = []
        
        # K-means is generally a good default
        suggestions.append({
            'algorithm': 'k_means',
            'suitability': 'high' if has_well_separated_clusters else 'medium',
            'params': {
                'n_clusters': 'auto',
                'init': 'k-means++',
                'n_init': 10
            },
            'notes': 'Fast and works well for globular clusters'
        })
        
        # DBSCAN for density-based clustering
        if n_samples <= 10000:  # DBSCAN can be slow for large datasets
            suggestions.append({
                'algorithm': 'dbscan',
                'suitability': 'high' if not has_well_separated_clusters else 'medium',
                'params': {
                    'eps': 'auto',
                    'min_samples': max(5, n_samples // 100)
                },
                'notes': 'Good for finding clusters of arbitrary shape and handling noise'
            })
        
        # Agglomerative clustering
        if n_samples <= 5000:  # Agglomerative can be very slow for large datasets
            suggestions.append({
                'algorithm': 'agglomerative',
                'suitability': 'medium',
                'params': {
                    'n_clusters': 'auto',
                    'linkage': 'ward'
                },
                'notes': 'Hierarchical clustering, good for creating dendrograms'
            })
        
        # Gaussian Mixture Models
        suggestions.append({
            'algorithm': 'gaussian_mixture',
            'suitability': 'high' if has_well_separated_clusters else 'medium',
            'params': {
                'n_components': 'auto',
                'covariance_type': 'full'
            },
            'notes': 'Probabilistic model, good when clusters have Gaussian distribution'
        })
        
        # OPTICS for varying density clusters
        if n_samples <= 10000:
            suggestions.append({
                'algorithm': 'optics',
                'suitability': 'high' if not has_well_separated_clusters else 'medium',
                'params': {
                    'min_samples': max(5, n_samples // 100),
                    'xi': 0.05
                },
                'notes': 'Similar to DBSCAN but better for varying density clusters'
            })
        
        # For high-dimensional data
        if is_high_dimensional:
            suggestions.append({
                'algorithm': 'birch',
                'suitability': 'high' if n_samples > 10000 else 'medium',
                'params': {
                    'threshold': 0.5,
                    'n_clusters': 'auto'
                },
                'notes': 'Efficient for large datasets with many features'
            })
        
        # Sort by suitability
        suitability_score = {'high': 3, 'medium': 2, 'low': 1}
        suggestions.sort(key=lambda x: suitability_score.get(x['suitability'], 0), reverse=True)
        
        return suggestions
    
    def suggest_n_clusters(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Suggest the optimal number of clusters using various methods.
        
        Args:
            data: Input data.
            
        Returns:
            Dictionary with suggested number of clusters and method details.
        """
        # Get numeric columns
        column_types = get_column_types(data)
        numeric_columns = column_types['numeric']
        
        if len(numeric_columns) < 2:
            return {
                'error': 'Not enough numeric features for clustering',
                'n_numeric_features': len(numeric_columns)
            }
        
        # Extract numeric data
        numeric_data = data[numeric_columns].copy()
        
        # Handle missing values
        numeric_data = numeric_data.fillna(numeric_data.mean())
        
        # Standardize data
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_data)
        
        results = {}
        
        try:
            # Elbow method using inertia
            from sklearn.cluster import KMeans
            inertia_values = []
            max_clusters = min(10, len(numeric_data) // 5)
            k_range = range(2, max_clusters + 1)
            
            for k in k_range:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                kmeans.fit(scaled_data)
                inertia_values.append(kmeans.inertia_)
            
            # Find elbow point
            from kneed import KneeLocator
            try:
                kneedle = KneeLocator(
                    list(k_range), inertia_values, curve='convex', direction='decreasing'
                )
                elbow_k = kneedle.elbow
            except:
                # If KneeLocator fails, use a simple heuristic
                inertia_diffs = np.diff(inertia_values)
                elbow_k = k_range[np.argmin(inertia_diffs) + 1]
            
            results['elbow_method'] = {
                'suggested_n_clusters': elbow_k,
                'inertia_values': dict(zip(k_range, inertia_values))
            }
        except Exception as e:
            results['elbow_method'] = {
                'error': str(e)
            }
        
        try:
            # Silhouette method
            from sklearn.metrics import silhouette_score
            silhouette_scores = []
            
            for k in k_range:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                cluster_labels = kmeans.fit_predict(scaled_data)
                silhouette_avg = silhouette_score(scaled_data, cluster_labels)
                silhouette_scores.append(silhouette_avg)
            
            best_k = k_range[np.argmax(silhouette_scores)]
            
            results['silhouette_method'] = {
                'suggested_n_clusters': best_k,
                'silhouette_scores': dict(zip(k_range, silhouette_scores))
            }
        except Exception as e:
            results['silhouette_method'] = {
                'error': str(e)
            }
        
        # Determine final suggestion
        if 'suggested_n_clusters' in results.get('silhouette_method', {}):
            final_suggestion = results['silhouette_method']['suggested_n_clusters']
            method = 'silhouette'
        elif 'suggested_n_clusters' in results.get('elbow_method', {}):
            final_suggestion = results['elbow_method']['suggested_n_clusters']
            method = 'elbow'
        else:
            # Default suggestion
            final_suggestion = min(5, len(numeric_data) // 20)
            method = 'default'
        
        return {
            'suggested_n_clusters': final_suggestion,
            'method': method,
            'details': results
        }
