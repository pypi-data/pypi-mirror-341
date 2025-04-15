"""
Task detection module for SBYB.

This module provides components for automatically detecting the machine learning task
type based on the data characteristics.
"""

from sbyb.task_detection.detector import TaskDetector
from sbyb.task_detection.classification import ClassificationDetector
from sbyb.task_detection.regression import RegressionDetector
from sbyb.task_detection.clustering import ClusteringDetector
from sbyb.task_detection.nlp import NLPDetector
from sbyb.task_detection.computer_vision import ComputerVisionDetector
from sbyb.task_detection.time_series import TimeSeriesDetector

__all__ = [
    'TaskDetector',
    'ClassificationDetector',
    'RegressionDetector',
    'ClusteringDetector',
    'NLPDetector',
    'ComputerVisionDetector',
    'TimeSeriesDetector',
]
