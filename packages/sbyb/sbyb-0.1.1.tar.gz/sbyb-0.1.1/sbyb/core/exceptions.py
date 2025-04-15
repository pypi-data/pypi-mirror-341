"""
Custom exceptions for SBYB.

This module defines custom exception classes for the SBYB library to provide
clear error messages and handling for various error conditions.
"""

class SBYBError(Exception):
    """Base exception class for all SBYB errors."""
    pass


class ConfigurationError(SBYBError):
    """Exception raised for errors in the configuration."""
    pass


class DataError(SBYBError):
    """Exception raised for errors in the input data."""
    pass


class PreprocessingError(SBYBError):
    """Exception raised for errors during data preprocessing."""
    pass


class ModelError(SBYBError):
    """Exception raised for errors related to models."""
    pass


class TaskDetectionError(SBYBError):
    """Exception raised for errors during task detection."""
    pass


class EvaluationError(SBYBError):
    """Exception raised for errors during model evaluation."""
    pass


class DeploymentError(SBYBError):
    """Exception raised for errors during model deployment."""
    pass


class UIGenerationError(SBYBError):
    """Exception raised for errors during UI generation."""
    pass


class PluginError(SBYBError):
    """Exception raised for errors related to plugins."""
    pass


class TrackingError(SBYBError):
    """Exception raised for errors during experiment tracking."""
    pass


class ResourceError(SBYBError):
    """Exception raised for errors related to system resources."""
    pass


class ValidationError(SBYBError):
    """Exception raised for validation errors."""
    pass


class NotFittedError(SBYBError):
    """Exception raised when trying to use an unfitted component."""
    pass


class IncompatibleDataError(DataError):
    """Exception raised when data is incompatible with a component."""
    pass
