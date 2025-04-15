"""
Evaluation module for SBYB.

This module provides components for evaluating machine learning models
and generating performance metrics.
"""

from sbyb.evaluation.metrics import MetricsCalculator
from sbyb.evaluation.visualizer import ModelVisualizer
from sbyb.evaluation.explainer import ModelExplainer
from sbyb.evaluation.validator import ModelValidator
from sbyb.evaluation.report import ModelReportGenerator

__all__ = [
    'MetricsCalculator',
    'ModelVisualizer',
    'ModelExplainer',
    'ModelValidator',
    'ModelReportGenerator',
]
