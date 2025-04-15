"""
Feature selection component for SBYB AutoML.

This module provides functionality for selecting the most important features
for machine learning models.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.feature_selection import (
    SelectKBest, f_classif, f_regression, mutual_info_classif, 
    mutual_info_regression, VarianceThreshold, SelectFromModel
)
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import Lasso, LogisticRegression

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import FeatureSelectionError


class FeatureSelector(SBYBComponent):
    """
    Feature selection component.
    
    This component selects the most important features for machine learning models
    using various feature selection methods.
    """
    
    def __init__(self, method: str = 'auto', threshold: float = 0.05, 
                 max_features: Optional[int] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the feature selector.
        
        Args:
            method: Feature selection method ('auto', 'variance', 'statistical', 'model_based', 'combined').
            threshold: Threshold for feature selection.
            max_features: Maximum number of features to select. If None, will be determined automatically.
            config: Configuration dictionary for the feature selector.
        """
        super().__init__(config)
        
        self.method = method
        self.threshold = threshold
        self.max_features = max_features
        self.selected_features = None
        self.feature_importance = None
    
    def select_features(self, X_train: pd.DataFrame, X_val: pd.DataFrame, y: Union[pd.Series, np.ndarray], 
                       task: str) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
        """
        Select features from the input data.
        
        Args:
            X_train: Training features.
            X_val: Validation features.
            y: Target variable.
            task: Machine learning task type.
            
        Returns:
            Tuple of (X_train_selected, X_val_selected, selected_feature_names).
        """
        # Choose feature selection method
        if self.method == 'auto':
            # Choose method based on data characteristics
            n_samples, n_features = X_train.shape
            
            if n_features > 100:
                # For high-dimensional data, use combined approach
                return self._combined_selection(X_train, X_val, y, task)
            elif n_features > 20:
                # For medium-dimensional data, use model-based selection
                return self._model_based_selection(X_train, X_val, y, task)
            else:
                # For low-dimensional data, use all features
                self.selected_features = X_train.columns.tolist()
                return X_train, X_val, self.selected_features
        
        elif self.method == 'variance':
            return self._variance_selection(X_train, X_val)
        
        elif self.method == 'statistical':
            return self._statistical_selection(X_train, X_val, y, task)
        
        elif self.method == 'model_based':
            return self._model_based_selection(X_train, X_val, y, task)
        
        elif self.method == 'combined':
            return self._combined_selection(X_train, X_val, y, task)
        
        else:
            raise FeatureSelectionError(f"Unknown feature selection method: {self.method}")
    
    def _variance_selection(self, X_train: pd.DataFrame, X_val: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
        """
        Select features based on variance.
        
        Args:
            X_train: Training features.
            X_val: Validation features.
            
        Returns:
            Tuple of (X_train_selected, X_val_selected, selected_feature_names).
        """
        # Remove features with low variance
        selector = VarianceThreshold(threshold=self.threshold)
        X_train_array = selector.fit_transform(X_train)
        X_val_array = selector.transform(X_val)
        
        # Get selected feature names
        selected_indices = selector.get_support(indices=True)
        selected_features = [X_train.columns[i] for i in selected_indices]
        
        # Convert back to DataFrame
        X_train_selected = pd.DataFrame(X_train_array, columns=selected_features, index=X_train.index)
        X_val_selected = pd.DataFrame(X_val_array, columns=selected_features, index=X_val.index)
        
        self.selected_features = selected_features
        return X_train_selected, X_val_selected, selected_features
    
    def _statistical_selection(self, X_train: pd.DataFrame, X_val: pd.DataFrame, 
                              y: Union[pd.Series, np.ndarray], task: str) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
        """
        Select features based on statistical tests.
        
        Args:
            X_train: Training features.
            X_val: Validation features.
            y: Target variable.
            task: Machine learning task type.
            
        Returns:
            Tuple of (X_train_selected, X_val_selected, selected_feature_names).
        """
        # Choose statistical test based on task
        if task in ['binary', 'multiclass']:
            score_func = f_classif
        else:
            score_func = f_regression
        
        # Determine number of features to select
        k = self.max_features if self.max_features is not None else max(1, int(X_train.shape[1] * 0.8))
        
        # Select features
        selector = SelectKBest(score_func=score_func, k=k)
        X_train_array = selector.fit_transform(X_train, y)
        X_val_array = selector.transform(X_val)
        
        # Get selected feature names
        selected_indices = selector.get_support(indices=True)
        selected_features = [X_train.columns[i] for i in selected_indices]
        
        # Convert back to DataFrame
        X_train_selected = pd.DataFrame(X_train_array, columns=selected_features, index=X_train.index)
        X_val_selected = pd.DataFrame(X_val_array, columns=selected_features, index=X_val.index)
        
        # Store feature importance
        self.feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': selector.scores_
        }).sort_values('importance', ascending=False)
        
        self.selected_features = selected_features
        return X_train_selected, X_val_selected, selected_features
    
    def _model_based_selection(self, X_train: pd.DataFrame, X_val: pd.DataFrame, 
                              y: Union[pd.Series, np.ndarray], task: str) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
        """
        Select features based on model importance.
        
        Args:
            X_train: Training features.
            X_val: Validation features.
            y: Target variable.
            task: Machine learning task type.
            
        Returns:
            Tuple of (X_train_selected, X_val_selected, selected_feature_names).
        """
        # Choose model based on task
        if task in ['binary', 'multiclass']:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # Fit model
        model.fit(X_train, y)
        
        # Get feature importance
        importance = model.feature_importances_
        
        # Store feature importance
        self.feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        # Select features based on importance threshold or max_features
        if self.max_features is not None:
            # Select top k features
            k = min(self.max_features, X_train.shape[1])
            threshold = sorted(importance, reverse=True)[k-1]
        else:
            # Use importance threshold
            threshold = self.threshold
        
        # Create selector
        selector = SelectFromModel(model, threshold=threshold, prefit=True)
        X_train_array = selector.transform(X_train)
        X_val_array = selector.transform(X_val)
        
        # Get selected feature names
        selected_indices = selector.get_support(indices=True)
        selected_features = [X_train.columns[i] for i in selected_indices]
        
        # Convert back to DataFrame
        X_train_selected = pd.DataFrame(X_train_array, columns=selected_features, index=X_train.index)
        X_val_selected = pd.DataFrame(X_val_array, columns=selected_features, index=X_val.index)
        
        self.selected_features = selected_features
        return X_train_selected, X_val_selected, selected_features
    
    def _combined_selection(self, X_train: pd.DataFrame, X_val: pd.DataFrame, 
                           y: Union[pd.Series, np.ndarray], task: str) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
        """
        Select features using a combination of methods.
        
        Args:
            X_train: Training features.
            X_val: Validation features.
            y: Target variable.
            task: Machine learning task type.
            
        Returns:
            Tuple of (X_train_selected, X_val_selected, selected_feature_names).
        """
        # Step 1: Remove low variance features
        var_selector = VarianceThreshold(threshold=0.01)
        X_train_var = pd.DataFrame(
            var_selector.fit_transform(X_train),
            columns=X_train.columns[var_selector.get_support()],
            index=X_train.index
        )
        X_val_var = pd.DataFrame(
            var_selector.transform(X_val),
            columns=X_train.columns[var_selector.get_support()],
            index=X_val.index
        )
        
        # If too few features remain, return them
        if X_train_var.shape[1] <= 5:
            self.selected_features = X_train_var.columns.tolist()
            return X_train_var, X_val_var, self.selected_features
        
        # Step 2: Apply statistical selection
        if task in ['binary', 'multiclass']:
            score_func = f_classif
        else:
            score_func = f_regression
        
        # Select a larger subset of features with statistical test
        k_stat = max(5, int(X_train_var.shape[1] * 0.5))
        stat_selector = SelectKBest(score_func=score_func, k=k_stat)
        X_train_stat = pd.DataFrame(
            stat_selector.fit_transform(X_train_var, y),
            columns=X_train_var.columns[stat_selector.get_support()],
            index=X_train_var.index
        )
        X_val_stat = pd.DataFrame(
            stat_selector.transform(X_val_var),
            columns=X_train_var.columns[stat_selector.get_support()],
            index=X_val_var.index
        )
        
        # If too few features remain, return them
        if X_train_stat.shape[1] <= 5:
            self.selected_features = X_train_stat.columns.tolist()
            return X_train_stat, X_val_stat, self.selected_features
        
        # Step 3: Apply model-based selection
        if task in ['binary', 'multiclass']:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # Fit model
        model.fit(X_train_stat, y)
        
        # Get feature importance
        importance = model.feature_importances_
        
        # Store feature importance
        self.feature_importance = pd.DataFrame({
            'feature': X_train_stat.columns,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        # Determine final number of features
        if self.max_features is not None:
            k_final = min(self.max_features, X_train_stat.shape[1])
        else:
            k_final = max(5, int(X_train_stat.shape[1] * 0.8))
        
        # Select top k features
        threshold = sorted(importance, reverse=True)[min(k_final-1, len(importance)-1)]
        model_selector = SelectFromModel(model, threshold=threshold, prefit=True)
        
        X_train_final = pd.DataFrame(
            model_selector.transform(X_train_stat),
            columns=X_train_stat.columns[model_selector.get_support()],
            index=X_train_stat.index
        )
        X_val_final = pd.DataFrame(
            model_selector.transform(X_val_stat),
            columns=X_train_stat.columns[model_selector.get_support()],
            index=X_val_stat.index
        )
        
        self.selected_features = X_train_final.columns.tolist()
        return X_train_final, X_val_final, self.selected_features
    
    def get_feature_importance(self) -> Optional[pd.DataFrame]:
        """
        Get feature importance.
        
        Returns:
            DataFrame with feature names and importance scores, or None if not available.
        """
        return self.feature_importance
