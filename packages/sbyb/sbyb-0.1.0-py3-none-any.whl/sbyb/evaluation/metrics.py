"""
Metrics calculation component for SBYB evaluation.

This module provides functionality for calculating various performance metrics
for different types of machine learning models.
"""

from typing import Any, Dict, List, Optional, Union, Callable

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    mean_squared_error, mean_absolute_error, r2_score,
    explained_variance_score, median_absolute_error,
    silhouette_score, calinski_harabasz_score, davies_bouldin_score
)

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import EvaluationError


class MetricsCalculator(SBYBComponent):
    """
    Metrics calculation component.
    
    This component calculates various performance metrics for different types of
    machine learning models.
    """
    
    def __init__(self, task: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the metrics calculator.
        
        Args:
            task: Machine learning task type. If None, will be auto-detected.
            config: Configuration dictionary for the metrics calculator.
        """
        super().__init__(config)
        self.task = task
        self.metrics = {}
    
    def calculate_metrics(self, y_true: Union[pd.Series, np.ndarray], 
                         y_pred: Union[pd.Series, np.ndarray],
                         y_prob: Optional[Union[pd.Series, np.ndarray]] = None,
                         task: Optional[str] = None,
                         sample_weight: Optional[Union[pd.Series, np.ndarray]] = None) -> Dict[str, Any]:
        """
        Calculate performance metrics.
        
        Args:
            y_true: True target values.
            y_pred: Predicted target values.
            y_prob: Predicted probabilities (for classification tasks).
            task: Machine learning task type. If None, will use the task specified in the constructor
                or auto-detect it.
            sample_weight: Sample weights.
            
        Returns:
            Dictionary of calculated metrics.
        """
        # Convert to numpy arrays
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        if y_prob is not None:
            y_prob = np.array(y_prob)
        if sample_weight is not None:
            sample_weight = np.array(sample_weight)
        
        # Determine the task if not specified
        if task is not None:
            self.task = task
        elif self.task is None:
            self.task = self._detect_task(y_true)
        
        # Calculate metrics based on task
        if self.task == 'binary':
            metrics = self._calculate_binary_classification_metrics(y_true, y_pred, y_prob, sample_weight)
        elif self.task == 'multiclass':
            metrics = self._calculate_multiclass_classification_metrics(y_true, y_pred, y_prob, sample_weight)
        elif self.task == 'regression':
            metrics = self._calculate_regression_metrics(y_true, y_pred, sample_weight)
        elif self.task == 'clustering':
            metrics = self._calculate_clustering_metrics(y_true, y_pred)
        else:
            raise EvaluationError(f"Unsupported task type for metrics calculation: {self.task}")
        
        # Store metrics
        self.metrics = metrics
        
        return metrics
    
    def _calculate_binary_classification_metrics(self, y_true: np.ndarray, y_pred: np.ndarray,
                                               y_prob: Optional[np.ndarray] = None,
                                               sample_weight: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Calculate metrics for binary classification.
        
        Args:
            y_true: True target values.
            y_pred: Predicted target values.
            y_prob: Predicted probabilities.
            sample_weight: Sample weights.
            
        Returns:
            Dictionary of calculated metrics.
        """
        metrics = {}
        
        # Basic metrics
        metrics['accuracy'] = accuracy_score(y_true, y_pred, sample_weight=sample_weight)
        metrics['precision'] = precision_score(y_true, y_pred, average='binary', sample_weight=sample_weight)
        metrics['recall'] = recall_score(y_true, y_pred, average='binary', sample_weight=sample_weight)
        metrics['f1'] = f1_score(y_true, y_pred, average='binary', sample_weight=sample_weight)
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred, sample_weight=sample_weight)
        metrics['confusion_matrix'] = cm
        
        # True positives, false positives, true negatives, false negatives
        tn, fp, fn, tp = cm.ravel()
        metrics['true_positives'] = tp
        metrics['false_positives'] = fp
        metrics['true_negatives'] = tn
        metrics['false_negatives'] = fn
        
        # Derived metrics
        metrics['specificity'] = tn / (tn + fp) if (tn + fp) > 0 else 0
        metrics['negative_predictive_value'] = tn / (tn + fn) if (tn + fn) > 0 else 0
        metrics['false_positive_rate'] = fp / (fp + tn) if (fp + tn) > 0 else 0
        metrics['false_negative_rate'] = fn / (fn + tp) if (fn + tp) > 0 else 0
        metrics['prevalence'] = (tp + fn) / (tp + fp + tn + fn) if (tp + fp + tn + fn) > 0 else 0
        
        # ROC AUC if probabilities are provided
        if y_prob is not None:
            try:
                if y_prob.ndim > 1 and y_prob.shape[1] > 1:
                    # If multi-dimensional, take the second column (probability of positive class)
                    y_prob_pos = y_prob[:, 1]
                else:
                    # Otherwise, use as is
                    y_prob_pos = y_prob.ravel()
                
                metrics['roc_auc'] = roc_auc_score(y_true, y_prob_pos, sample_weight=sample_weight)
            except Exception as e:
                metrics['roc_auc'] = None
                metrics['roc_auc_error'] = str(e)
        
        # Classification report
        try:
            report = classification_report(y_true, y_pred, output_dict=True, sample_weight=sample_weight)
            metrics['classification_report'] = report
        except Exception as e:
            metrics['classification_report'] = None
            metrics['classification_report_error'] = str(e)
        
        return metrics
    
    def _calculate_multiclass_classification_metrics(self, y_true: np.ndarray, y_pred: np.ndarray,
                                                   y_prob: Optional[np.ndarray] = None,
                                                   sample_weight: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Calculate metrics for multiclass classification.
        
        Args:
            y_true: True target values.
            y_pred: Predicted target values.
            y_prob: Predicted probabilities.
            sample_weight: Sample weights.
            
        Returns:
            Dictionary of calculated metrics.
        """
        metrics = {}
        
        # Basic metrics
        metrics['accuracy'] = accuracy_score(y_true, y_pred, sample_weight=sample_weight)
        
        # Precision, recall, F1 for each class and average
        for average in ['micro', 'macro', 'weighted']:
            metrics[f'precision_{average}'] = precision_score(y_true, y_pred, average=average, sample_weight=sample_weight)
            metrics[f'recall_{average}'] = recall_score(y_true, y_pred, average=average, sample_weight=sample_weight)
            metrics[f'f1_{average}'] = f1_score(y_true, y_pred, average=average, sample_weight=sample_weight)
        
        # Confusion matrix
        metrics['confusion_matrix'] = confusion_matrix(y_true, y_pred, sample_weight=sample_weight)
        
        # ROC AUC if probabilities are provided
        if y_prob is not None:
            try:
                # For multiclass, use one-vs-rest ROC AUC
                metrics['roc_auc_ovr'] = roc_auc_score(y_true, y_prob, multi_class='ovr', sample_weight=sample_weight)
                metrics['roc_auc_ovo'] = roc_auc_score(y_true, y_prob, multi_class='ovo', sample_weight=sample_weight)
            except Exception as e:
                metrics['roc_auc_ovr'] = None
                metrics['roc_auc_ovo'] = None
                metrics['roc_auc_error'] = str(e)
        
        # Classification report
        try:
            report = classification_report(y_true, y_pred, output_dict=True, sample_weight=sample_weight)
            metrics['classification_report'] = report
        except Exception as e:
            metrics['classification_report'] = None
            metrics['classification_report_error'] = str(e)
        
        return metrics
    
    def _calculate_regression_metrics(self, y_true: np.ndarray, y_pred: np.ndarray,
                                    sample_weight: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Calculate metrics for regression.
        
        Args:
            y_true: True target values.
            y_pred: Predicted target values.
            sample_weight: Sample weights.
            
        Returns:
            Dictionary of calculated metrics.
        """
        metrics = {}
        
        # Basic metrics
        metrics['mean_squared_error'] = mean_squared_error(y_true, y_pred, sample_weight=sample_weight)
        metrics['root_mean_squared_error'] = np.sqrt(metrics['mean_squared_error'])
        metrics['mean_absolute_error'] = mean_absolute_error(y_true, y_pred, sample_weight=sample_weight)
        metrics['r2'] = r2_score(y_true, y_pred, sample_weight=sample_weight)
        metrics['explained_variance'] = explained_variance_score(y_true, y_pred, sample_weight=sample_weight)
        metrics['median_absolute_error'] = median_absolute_error(y_true, y_pred)
        
        # Additional metrics
        metrics['mean_absolute_percentage_error'] = np.mean(np.abs((y_true - y_pred) / np.maximum(np.abs(y_true), 1e-10))) * 100
        
        # Residuals
        residuals = y_true - y_pred
        metrics['residuals_mean'] = np.mean(residuals)
        metrics['residuals_std'] = np.std(residuals)
        
        return metrics
    
    def _calculate_clustering_metrics(self, X: np.ndarray, labels: np.ndarray) -> Dict[str, Any]:
        """
        Calculate metrics for clustering.
        
        Args:
            X: Input features.
            labels: Cluster labels.
            
        Returns:
            Dictionary of calculated metrics.
        """
        metrics = {}
        
        # Number of clusters
        n_clusters = len(np.unique(labels))
        metrics['n_clusters'] = n_clusters
        
        # Cluster sizes
        unique_labels, counts = np.unique(labels, return_counts=True)
        metrics['cluster_sizes'] = dict(zip(unique_labels, counts))
        
        # Silhouette score
        try:
            metrics['silhouette_score'] = silhouette_score(X, labels)
        except Exception as e:
            metrics['silhouette_score'] = None
            metrics['silhouette_score_error'] = str(e)
        
        # Calinski-Harabasz Index
        try:
            metrics['calinski_harabasz_score'] = calinski_harabasz_score(X, labels)
        except Exception as e:
            metrics['calinski_harabasz_score'] = None
            metrics['calinski_harabasz_score_error'] = str(e)
        
        # Davies-Bouldin Index
        try:
            metrics['davies_bouldin_score'] = davies_bouldin_score(X, labels)
        except Exception as e:
            metrics['davies_bouldin_score'] = None
            metrics['davies_bouldin_score_error'] = str(e)
        
        return metrics
    
    def _detect_task(self, y: np.ndarray) -> str:
        """
        Detect the machine learning task type from the target variable.
        
        Args:
            y: Target variable.
            
        Returns:
            Task type ('binary', 'multiclass', or 'regression').
        """
        # Check if it's classification or regression
        if np.issubdtype(y.dtype, np.number):
            n_unique = len(np.unique(y))
            
            if n_unique == 2:
                return 'binary'
            elif n_unique <= 20:  # Arbitrary threshold for multiclass
                return 'multiclass'
            else:
                return 'regression'
        else:
            # Non-numeric types are assumed to be classification
            n_unique = len(np.unique(y))
            return 'binary' if n_unique == 2 else 'multiclass'
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get the calculated metrics.
        
        Returns:
            Dictionary of calculated metrics.
        """
        if not self.metrics:
            raise EvaluationError("No metrics have been calculated yet. Call 'calculate_metrics' first.")
        
        return self.metrics
    
    def get_metric(self, metric_name: str) -> Any:
        """
        Get a specific metric.
        
        Args:
            metric_name: Name of the metric.
            
        Returns:
            Value of the metric.
        """
        if not self.metrics:
            raise EvaluationError("No metrics have been calculated yet. Call 'calculate_metrics' first.")
        
        if metric_name not in self.metrics:
            raise EvaluationError(f"Metric '{metric_name}' not found in calculated metrics.")
        
        return self.metrics[metric_name]
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the most important metrics.
        
        Returns:
            Dictionary of important metrics.
        """
        if not self.metrics:
            raise EvaluationError("No metrics have been calculated yet. Call 'calculate_metrics' first.")
        
        summary = {}
        
        if self.task == 'binary':
            summary = {
                'accuracy': self.metrics.get('accuracy'),
                'precision': self.metrics.get('precision'),
                'recall': self.metrics.get('recall'),
                'f1': self.metrics.get('f1'),
                'roc_auc': self.metrics.get('roc_auc')
            }
        elif self.task == 'multiclass':
            summary = {
                'accuracy': self.metrics.get('accuracy'),
                'precision_macro': self.metrics.get('precision_macro'),
                'recall_macro': self.metrics.get('recall_macro'),
                'f1_macro': self.metrics.get('f1_macro')
            }
        elif self.task == 'regression':
            summary = {
                'r2': self.metrics.get('r2'),
                'mean_squared_error': self.metrics.get('mean_squared_error'),
                'root_mean_squared_error': self.metrics.get('root_mean_squared_error'),
                'mean_absolute_error': self.metrics.get('mean_absolute_error')
            }
        elif self.task == 'clustering':
            summary = {
                'n_clusters': self.metrics.get('n_clusters'),
                'silhouette_score': self.metrics.get('silhouette_score'),
                'calinski_harabasz_score': self.metrics.get('calinski_harabasz_score'),
                'davies_bouldin_score': self.metrics.get('davies_bouldin_score')
            }
        
        return summary
