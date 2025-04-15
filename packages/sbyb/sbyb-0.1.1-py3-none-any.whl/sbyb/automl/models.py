"""
Model registry for SBYB AutoML.

This module provides a registry of machine learning models for different tasks,
along with their default hyperparameters and metadata.
"""

from typing import Any, Dict, List, Optional, Tuple, Union, Type

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

# Import model classes
from sklearn.linear_model import (
    LogisticRegression, Ridge, Lasso, ElasticNet, LinearRegression
)
from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor,
    GradientBoostingClassifier, GradientBoostingRegressor,
    AdaBoostClassifier, AdaBoostRegressor,
    ExtraTreesClassifier, ExtraTreesRegressor,
    VotingClassifier, VotingRegressor
)
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVC, SVR
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neural_network import MLPClassifier, MLPRegressor

# Try to import optional models
try:
    from xgboost import XGBClassifier, XGBRegressor
    HAVE_XGBOOST = True
except ImportError:
    HAVE_XGBOOST = False
    XGBClassifier = None
    XGBRegressor = None

try:
    from lightgbm import LGBMClassifier, LGBMRegressor
    HAVE_LIGHTGBM = True
except ImportError:
    HAVE_LIGHTGBM = False
    LGBMClassifier = None
    LGBMRegressor = None

try:
    from catboost import CatBoostClassifier, CatBoostRegressor
    HAVE_CATBOOST = True
except ImportError:
    HAVE_CATBOOST = False
    CatBoostClassifier = None
    CatBoostRegressor = None


def get_models_for_task(task: str) -> Dict[str, Tuple[Type[BaseEstimator], Dict[str, Any], Dict[str, Any]]]:
    """
    Get available models for a specific task.
    
    Args:
        task: Machine learning task type ('binary', 'multiclass', 'regression', etc.).
        
    Returns:
        Dictionary mapping model names to tuples of (model_class, default_params, metadata).
    """
    if task == 'binary':
        return _get_binary_classification_models()
    elif task == 'multiclass':
        return _get_multiclass_classification_models()
    elif task == 'regression':
        return _get_regression_models()
    elif task == 'clustering':
        return _get_clustering_models()
    elif task == 'nlp_classification':
        return _get_nlp_classification_models()
    elif task == 'nlp_regression':
        return _get_nlp_regression_models()
    elif task == 'computer_vision':
        return _get_computer_vision_models()
    elif task == 'time_series_forecasting':
        return _get_time_series_forecasting_models()
    elif task == 'time_series_classification':
        return _get_time_series_classification_models()
    elif task == 'anomaly_detection':
        return _get_anomaly_detection_models()
    else:
        raise ValueError(f"Unknown task type: {task}")


def _get_binary_classification_models() -> Dict[str, Tuple[Type[BaseEstimator], Dict[str, Any], Dict[str, Any]]]:
    """
    Get models for binary classification.
    
    Returns:
        Dictionary mapping model names to tuples of (model_class, default_params, metadata).
    """
    models = {}
    
    # Logistic Regression
    models['logistic_regression'] = (
        LogisticRegression,
        {'C': 1.0, 'penalty': 'l2', 'solver': 'lbfgs', 'max_iter': 1000, 'random_state': 42},
        {'priority': 5, 'min_samples': 10, 'max_features': float('inf')}
    )
    
    # Random Forest
    models['random_forest'] = (
        RandomForestClassifier,
        {'n_estimators': 100, 'max_depth': None, 'min_samples_split': 2, 'random_state': 42},
        {'priority': 9, 'min_samples': 50, 'max_features': float('inf')}
    )
    
    # Gradient Boosting
    models['gradient_boosting'] = (
        GradientBoostingClassifier,
        {'n_estimators': 100, 'learning_rate': 0.1, 'max_depth': 3, 'random_state': 42},
        {'priority': 8, 'min_samples': 50, 'max_features': float('inf')}
    )
    
    # SVM
    models['svm'] = (
        SVC,
        {'C': 1.0, 'kernel': 'rbf', 'probability': True, 'random_state': 42},
        {'priority': 6, 'min_samples': 10, 'max_features': 1000}
    )
    
    # K-Nearest Neighbors
    models['knn'] = (
        KNeighborsClassifier,
        {'n_neighbors': 5, 'weights': 'uniform'},
        {'priority': 4, 'min_samples': 10, 'max_features': 100}
    )
    
    # Decision Tree
    models['decision_tree'] = (
        DecisionTreeClassifier,
        {'max_depth': None, 'min_samples_split': 2, 'random_state': 42},
        {'priority': 3, 'min_samples': 10, 'max_features': float('inf')}
    )
    
    # Naive Bayes
    models['naive_bayes'] = (
        GaussianNB,
        {},
        {'priority': 2, 'min_samples': 10, 'max_features': float('inf')}
    )
    
    # AdaBoost
    models['adaboost'] = (
        AdaBoostClassifier,
        {'n_estimators': 50, 'learning_rate': 1.0, 'random_state': 42},
        {'priority': 7, 'min_samples': 50, 'max_features': float('inf')}
    )
    
    # Extra Trees
    models['extra_trees'] = (
        ExtraTreesClassifier,
        {'n_estimators': 100, 'max_depth': None, 'min_samples_split': 2, 'random_state': 42},
        {'priority': 7, 'min_samples': 50, 'max_features': float('inf')}
    )
    
    # Neural Network
    models['neural_network'] = (
        MLPClassifier,
        {'hidden_layer_sizes': (100,), 'activation': 'relu', 'solver': 'adam', 'alpha': 0.0001,
         'max_iter': 200, 'random_state': 42},
        {'priority': 6, 'min_samples': 100, 'max_features': 1000}
    )
    
    # XGBoost
    if HAVE_XGBOOST:
        models['xgboost'] = (
            XGBClassifier,
            {'n_estimators': 100, 'learning_rate': 0.1, 'max_depth': 3, 'random_state': 42},
            {'priority': 10, 'min_samples': 50, 'max_features': float('inf')}
        )
    
    # LightGBM
    if HAVE_LIGHTGBM:
        models['lightgbm'] = (
            LGBMClassifier,
            {'n_estimators': 100, 'learning_rate': 0.1, 'num_leaves': 31, 'random_state': 42},
            {'priority': 10, 'min_samples': 50, 'max_features': float('inf')}
        )
    
    # CatBoost
    if HAVE_CATBOOST:
        models['catboost'] = (
            CatBoostClassifier,
            {'iterations': 100, 'learning_rate': 0.1, 'depth': 6, 'random_seed': 42, 'verbose': 0},
            {'priority': 9, 'min_samples': 50, 'max_features': float('inf')}
        )
    
    return models


def _get_multiclass_classification_models() -> Dict[str, Tuple[Type[BaseEstimator], Dict[str, Any], Dict[str, Any]]]:
    """
    Get models for multiclass classification.
    
    Returns:
        Dictionary mapping model names to tuples of (model_class, default_params, metadata).
    """
    # Start with binary classification models
    models = _get_binary_classification_models()
    
    # Update SVM for multiclass
    models['svm'] = (
        SVC,
        {'C': 1.0, 'kernel': 'rbf', 'probability': True, 'decision_function_shape': 'ovr', 'random_state': 42},
        {'priority': 6, 'min_samples': 10, 'max_features': 1000}
    )
    
    # Add Multinomial Naive Bayes
    models['multinomial_nb'] = (
        MultinomialNB,
        {'alpha': 1.0},
        {'priority': 2, 'min_samples': 10, 'max_features': float('inf')}
    )
    
    return models


def _get_regression_models() -> Dict[str, Tuple[Type[BaseEstimator], Dict[str, Any], Dict[str, Any]]]:
    """
    Get models for regression.
    
    Returns:
        Dictionary mapping model names to tuples of (model_class, default_params, metadata).
    """
    models = {}
    
    # Linear Regression
    models['linear_regression'] = (
        LinearRegression,
        {'fit_intercept': True, 'n_jobs': -1},
        {'priority': 5, 'min_samples': 10, 'max_features': float('inf')}
    )
    
    # Ridge Regression
    models['ridge'] = (
        Ridge,
        {'alpha': 1.0, 'solver': 'auto', 'random_state': 42},
        {'priority': 6, 'min_samples': 10, 'max_features': float('inf')}
    )
    
    # Lasso Regression
    models['lasso'] = (
        Lasso,
        {'alpha': 1.0, 'random_state': 42},
        {'priority': 5, 'min_samples': 10, 'max_features': float('inf')}
    )
    
    # Elastic Net
    models['elastic_net'] = (
        ElasticNet,
        {'alpha': 1.0, 'l1_ratio': 0.5, 'random_state': 42},
        {'priority': 5, 'min_samples': 10, 'max_features': float('inf')}
    )
    
    # Random Forest
    models['random_forest'] = (
        RandomForestRegressor,
        {'n_estimators': 100, 'max_depth': None, 'min_samples_split': 2, 'random_state': 42},
        {'priority': 9, 'min_samples': 50, 'max_features': float('inf')}
    )
    
    # Gradient Boosting
    models['gradient_boosting'] = (
        GradientBoostingRegressor,
        {'n_estimators': 100, 'learning_rate': 0.1, 'max_depth': 3, 'random_state': 42},
        {'priority': 8, 'min_samples': 50, 'max_features': float('inf')}
    )
    
    # SVR
    models['svr'] = (
        SVR,
        {'C': 1.0, 'kernel': 'rbf', 'epsilon': 0.1},
        {'priority': 6, 'min_samples': 10, 'max_features': 1000}
    )
    
    # K-Nearest Neighbors
    models['knn'] = (
        KNeighborsRegressor,
        {'n_neighbors': 5, 'weights': 'uniform'},
        {'priority': 4, 'min_samples': 10, 'max_features': 100}
    )
    
    # Decision Tree
    models['decision_tree'] = (
        DecisionTreeRegressor,
        {'max_depth': None, 'min_samples_split': 2, 'random_state': 42},
        {'priority': 3, 'min_samples': 10, 'max_features': float('inf')}
    )
    
    # AdaBoost
    models['adaboost'] = (
        AdaBoostRegressor,
        {'n_estimators': 50, 'learning_rate': 1.0, 'random_state': 42},
        {'priority': 7, 'min_samples': 50, 'max_features': float('inf')}
    )
    
    # Extra Trees
    models['extra_trees'] = (
        ExtraTreesRegressor,
        {'n_estimators': 100, 'max_depth': None, 'min_samples_split': 2, 'random_state': 42},
        {'priority': 7, 'min_samples': 50, 'max_features': float('inf')}
    )
    
    # Neural Network
    models['neural_network'] = (
        MLPRegressor,
        {'hidden_layer_sizes': (100,), 'activation': 'relu', 'solver': 'adam', 'alpha': 0.0001,
         'max_iter': 200, 'random_state': 42},
        {'priority': 6, 'min_samples': 100, 'max_features': 1000}
    )
    
    # XGBoost
    if HAVE_XGBOOST:
        models['xgboost'] = (
            XGBRegressor,
            {'n_estimators': 100, 'learning_rate': 0.1, 'max_depth': 3, 'random_state': 42},
            {'priority': 10, 'min_samples': 50, 'max_features': float('inf')}
        )
    
    # LightGBM
    if HAVE_LIGHTGBM:
        models['lightgbm'] = (
            LGBMRegressor,
            {'n_estimators': 100, 'learning_rate': 0.1, 'num_leaves': 31, 'random_state': 42},
            {'priority': 10, 'min_samples': 50, 'max_features': float('inf')}
        )
    
    # CatBoost
    if HAVE_CATBOOST:
        models['catboost'] = (
            CatBoostRegressor,
            {'iterations': 100, 'learning_rate': 0.1, 'depth': 6, 'random_seed': 42, 'verbose': 0},
            {'priority': 9, 'min_samples': 50, 'max_features': float('inf')}
        )
    
    return models


def _get_clustering_models() -> Dict[str, Tuple[Type[BaseEstimator], Dict[str, Any], Dict[str, Any]]]:
    """
    Get models for clustering.
    
    Returns:
        Dictionary mapping model names to tuples of (model_class, default_params, metadata).
    """
    from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, Birch
    from sklearn.mixture import GaussianMixture
    
    models = {}
    
    # K-Means
    models['kmeans'] = (
        KMeans,
        {'n_clusters': 8, 'init': 'k-means++', 'n_init': 10, 'random_state': 42},
        {'priority': 10, 'min_samples': 10, 'max_features': float('inf')}
    )
    
    # DBSCAN
    models['dbscan'] = (
        DBSCAN,
        {'eps': 0.5, 'min_samples': 5, 'metric': 'euclidean'},
        {'priority': 8, 'min_samples': 10, 'max_features': 100}
    )
    
    # Agglomerative Clustering
    models['agglomerative'] = (
        AgglomerativeClustering,
        {'n_clusters': 8, 'linkage': 'ward'},
        {'priority': 7, 'min_samples': 10, 'max_features': 100}
    )
    
    # Gaussian Mixture
    models['gaussian_mixture'] = (
        GaussianMixture,
        {'n_components': 8, 'covariance_type': 'full', 'random_state': 42},
        {'priority': 9, 'min_samples': 10, 'max_features': 100}
    )
    
    # Birch
    models['birch'] = (
        Birch,
        {'n_clusters': 8, 'threshold': 0.5, 'branching_factor': 50},
        {'priority': 6, 'min_samples': 10, 'max_features': float('inf')}
    )
    
    return models


def _get_nlp_classification_models() -> Dict[str, Tuple[Type[BaseEstimator], Dict[str, Any], Dict[str, Any]]]:
    """
    Get models for NLP classification.
    
    Returns:
        Dictionary mapping model names to tuples of (model_class, default_params, metadata).
    """
    # For NLP, we'll use the same models as for multiclass classification
    # In a real implementation, this would include specialized NLP models
    return _get_multiclass_classification_models()


def _get_nlp_regression_models() -> Dict[str, Tuple[Type[BaseEstimator], Dict[str, Any], Dict[str, Any]]]:
    """
    Get models for NLP regression.
    
    Returns:
        Dictionary mapping model names to tuples of (model_class, default_params, metadata).
    """
    # For NLP, we'll use the same models as for regression
    # In a real implementation, this would include specialized NLP models
    return _get_regression_models()


def _get_computer_vision_models() -> Dict[str, Tuple[Type[BaseEstimator], Dict[str, Any], Dict[str, Any]]]:
    """
    Get models for computer vision.
    
    Returns:
        Dictionary mapping model names to tuples of (model_class, default_params, metadata).
    """
    # For computer vision, we would typically use deep learning models
    # In this simplified implementation, we'll return an empty dictionary
    # In a real implementation, this would include CNN models
    return {}


def _get_time_series_forecasting_models() -> Dict[str, Tuple[Type[BaseEstimator], Dict[str, Any], Dict[str, Any]]]:
    """
    Get models for time series forecasting.
    
    Returns:
        Dictionary mapping model names to tuples of (model_class, default_params, metadata).
    """
    # For time series forecasting, we'll use regression models
    # In a real implementation, this would include specialized time series models
    return _get_regression_models()


def _get_time_series_classification_models() -> Dict[str, Tuple[Type[BaseEstimator], Dict[str, Any], Dict[str, Any]]]:
    """
    Get models for time series classification.
    
    Returns:
        Dictionary mapping model names to tuples of (model_class, default_params, metadata).
    """
    # For time series classification, we'll use classification models
    # In a real implementation, this would include specialized time series models
    return _get_multiclass_classification_models()


def _get_anomaly_detection_models() -> Dict[str, Tuple[Type[BaseEstimator], Dict[str, Any], Dict[str, Any]]]:
    """
    Get models for anomaly detection.
    
    Returns:
        Dictionary mapping model names to tuples of (model_class, default_params, metadata).
    """
    from sklearn.ensemble import IsolationForest
    from sklearn.neighbors import LocalOutlierFactor
    from sklearn.svm import OneClassSVM
    
    models = {}
    
    # Isolation Forest
    models['isolation_forest'] = (
        IsolationForest,
        {'n_estimators': 100, 'contamination': 'auto', 'random_state': 42},
        {'priority': 10, 'min_samples': 50, 'max_features': float('inf')}
    )
    
    # Local Outlier Factor
    models['local_outlier_factor'] = (
        LocalOutlierFactor,
        {'n_neighbors': 20, 'contamination': 'auto', 'novelty': True},
        {'priority': 8, 'min_samples': 10, 'max_features': 100}
    )
    
    # One-Class SVM
    models['one_class_svm'] = (
        OneClassSVM,
        {'kernel': 'rbf', 'nu': 0.1, 'gamma': 'scale'},
        {'priority': 7, 'min_samples': 10, 'max_features': 100}
    )
    
    return models
