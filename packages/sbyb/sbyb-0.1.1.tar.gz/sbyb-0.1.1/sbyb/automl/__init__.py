"""
AutoML module for SBYB.

This module provides components for automatic machine learning model selection,
hyperparameter optimization, and model ensembling.
"""

from sbyb.automl.engine import AutoMLEngine
from sbyb.automl.model_selection import ModelSelector
from sbyb.automl.hyperparameter import HyperparameterOptimizer
from sbyb.automl.feature_selection import FeatureSelector
from sbyb.automl.stacking import ModelStacker
from sbyb.automl.models import get_models_for_task

__all__ = [
    'AutoMLEngine',
    'ModelSelector',
    'HyperparameterOptimizer',
    'FeatureSelector',
    'ModelStacker',
    'get_models_for_task',
]
