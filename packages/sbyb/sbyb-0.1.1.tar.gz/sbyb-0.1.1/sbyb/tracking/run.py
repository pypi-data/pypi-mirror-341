"""
Run class for SBYB tracking.

This module provides the Run class, which represents a single execution of a machine
learning workflow with specific parameters, metrics, and artifacts.
"""

from typing import Any, Dict, List, Optional, Union
import os
import json
import datetime
import uuid
from pathlib import Path
import pickle
import matplotlib.pyplot as plt
import numpy as np

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import TrackingError


class Run(SBYBComponent):
    """
    Represents a single execution of a machine learning workflow.
    
    A run tracks parameters, metrics, artifacts, and other metadata for a single
    execution of a machine learning workflow. It provides methods for logging
    metrics, parameters, artifacts, and other information about the run.
    """
    
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None,
                tags: Optional[List[str]] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a new run.
        
        Args:
            name: Optional name of the run.
            description: Optional description of the run.
            tags: Optional list of tags for categorizing the run.
            config: Optional configuration dictionary.
        """
        super().__init__(config)
        
        self.name = name or f"Run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.description = description or ""
        self.tags = tags or []
        self.run_id = str(uuid.uuid4())
        self.experiment_id = None
        self.created_at = datetime.datetime.now().isoformat()
        self.started_at = None
        self.ended_at = None
        self.status = "created"  # created, running, completed, failed
        self.parameters = {}
        self.metrics = {}
        self.artifacts = {}
        self.logs = []
        self.metadata = {}
        self.history = {}
    
    def start(self) -> None:
        """
        Mark the run as started.
        """
        self.started_at = datetime.datetime.now().isoformat()
        self.status = "running"
        self._log_event("Run started")
    
    def complete(self) -> None:
        """
        Mark the run as completed.
        """
        self.ended_at = datetime.datetime.now().isoformat()
        self.status = "completed"
        self._log_event("Run completed")
    
    def fail(self, error_message: str) -> None:
        """
        Mark the run as failed.
        
        Args:
            error_message: Error message describing the failure.
        """
        self.ended_at = datetime.datetime.now().isoformat()
        self.status = "failed"
        self._log_event(f"Run failed: {error_message}")
        self.add_metadata("error_message", error_message)
    
    def log_parameter(self, key: str, value: Any) -> None:
        """
        Log a parameter for this run.
        
        Args:
            key: Parameter name.
            value: Parameter value.
        """
        self.parameters[key] = value
        self._log_event(f"Parameter logged: {key}={value}")
    
    def log_parameters(self, params: Dict[str, Any]) -> None:
        """
        Log multiple parameters for this run.
        
        Args:
            params: Dictionary of parameter names and values.
        """
        for key, value in params.items():
            self.log_parameter(key, value)
    
    def log_metric(self, key: str, value: Union[int, float]) -> None:
        """
        Log a metric for this run.
        
        Args:
            key: Metric name.
            value: Metric value.
            
        Raises:
            TrackingError: If the value is not a number.
        """
        if not isinstance(value, (int, float)):
            raise TrackingError(f"Metric value must be a number, got {type(value)}")
        
        self.metrics[key] = value
        self._log_event(f"Metric logged: {key}={value}")
    
    def log_metrics(self, metrics: Dict[str, Union[int, float]]) -> None:
        """
        Log multiple metrics for this run.
        
        Args:
            metrics: Dictionary of metric names and values.
        """
        for key, value in metrics.items():
            self.log_metric(key, value)
    
    def log_metric_step(self, key: str, value: Union[int, float], step: int) -> None:
        """
        Log a metric with a step for this run.
        
        Args:
            key: Metric name.
            value: Metric value.
            step: Step number.
            
        Raises:
            TrackingError: If the value is not a number.
        """
        if not isinstance(value, (int, float)):
            raise TrackingError(f"Metric value must be a number, got {type(value)}")
        
        if key not in self.history:
            self.history[key] = []
        
        self.history[key].append({"step": step, "value": value})
        self.metrics[key] = value  # Update the latest value
        self._log_event(f"Metric logged: {key}={value} (step {step})")
    
    def log_artifact(self, key: str, artifact: Any, artifact_path: Optional[str] = None) -> str:
        """
        Log an artifact for this run.
        
        Args:
            key: Artifact name.
            artifact: Artifact object.
            artifact_path: Optional path to save the artifact. If None, the artifact is stored in memory.
            
        Returns:
            Path to the saved artifact if artifact_path is provided, otherwise "memory".
        """
        if artifact_path:
            # Save the artifact to a file
            os.makedirs(os.path.dirname(artifact_path), exist_ok=True)
            
            if isinstance(artifact, plt.Figure):
                # Save matplotlib figure
                artifact.savefig(artifact_path)
                location = artifact_path
            elif isinstance(artifact, (np.ndarray, list, dict, str, int, float, bool)):
                # Save simple objects as JSON if possible
                try:
                    with open(artifact_path, "w") as f:
                        json.dump(artifact, f)
                    location = artifact_path
                except (TypeError, OverflowError):
                    # Fall back to pickle for objects that can't be JSON serialized
                    with open(artifact_path, "wb") as f:
                        pickle.dump(artifact, f)
                    location = artifact_path
            else:
                # Use pickle for other objects
                with open(artifact_path, "wb") as f:
                    pickle.dump(artifact, f)
                location = artifact_path
            
            self.artifacts[key] = {"type": type(artifact).__name__, "location": location}
        else:
            # Store the artifact in memory
            self.artifacts[key] = {"type": type(artifact).__name__, "location": "memory", "value": artifact}
            location = "memory"
        
        self._log_event(f"Artifact logged: {key} ({type(artifact).__name__})")
        return location
    
    def get_artifact(self, key: str) -> Any:
        """
        Get an artifact by name.
        
        Args:
            key: Artifact name.
            
        Returns:
            Artifact object if found.
            
        Raises:
            TrackingError: If the artifact is not found or cannot be loaded.
        """
        if key not in self.artifacts:
            raise TrackingError(f"Artifact not found: {key}")
        
        artifact_info = self.artifacts[key]
        
        if artifact_info["location"] == "memory":
            return artifact_info["value"]
        else:
            try:
                location = artifact_info["location"]
                
                if location.endswith((".json", ".txt")):
                    with open(location, "r") as f:
                        return json.load(f)
                else:
                    with open(location, "rb") as f:
                        return pickle.load(f)
            except Exception as e:
                raise TrackingError(f"Error loading artifact {key}: {str(e)}")
    
    def log_model(self, model: Any, model_path: str) -> str:
        """
        Log a model for this run.
        
        Args:
            model: Model object.
            model_path: Path to save the model.
            
        Returns:
            Path to the saved model.
        """
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        
        self.artifacts["model"] = {"type": type(model).__name__, "location": model_path}
        self._log_event(f"Model logged: {type(model).__name__}")
        return model_path
    
    def get_model(self) -> Any:
        """
        Get the model for this run.
        
        Returns:
            Model object if found.
            
        Raises:
            TrackingError: If the model is not found or cannot be loaded.
        """
        return self.get_artifact("model")
    
    def log_message(self, message: str) -> None:
        """
        Log a message for this run.
        
        Args:
            message: Message to log.
        """
        self._log_event(message)
    
    def _log_event(self, message: str) -> None:
        """
        Log an event for this run.
        
        Args:
            message: Event message.
        """
        timestamp = datetime.datetime.now().isoformat()
        self.logs.append({"timestamp": timestamp, "message": message})
    
    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add metadata to the run.
        
        Args:
            key: Metadata key.
            value: Metadata value.
        """
        self.metadata[key] = value
    
    def get_metadata(self, key: str) -> Any:
        """
        Get metadata from the run.
        
        Args:
            key: Metadata key.
            
        Returns:
            Metadata value if found, None otherwise.
        """
        return self.metadata.get(key)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the run to a dictionary.
        
        Returns:
            Dictionary representation of the run.
        """
        # Filter out in-memory artifacts for serialization
        serializable_artifacts = {}
        for key, artifact_info in self.artifacts.items():
            if artifact_info["location"] == "memory":
                serializable_artifacts[key] = {
                    "type": artifact_info["type"],
                    "location": "memory"
                }
            else:
                serializable_artifacts[key] = artifact_info
        
        return {
            "run_id": self.run_id,
            "experiment_id": self.experiment_id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "status": self.status,
            "parameters": self.parameters,
            "metrics": self.metrics,
            "artifacts": serializable_artifacts,
            "logs": self.logs,
            "metadata": self.metadata,
            "history": self.history
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Create a run from a dictionary.
        
        Args:
            data: Dictionary representation of the run.
            
        Returns:
            Run object.
        """
        run = cls(
            name=data["name"],
            description=data.get("description", ""),
            tags=data.get("tags", [])
        )
        
        run.run_id = data["run_id"]
        run.experiment_id = data.get("experiment_id")
        run.created_at = data["created_at"]
        run.started_at = data.get("started_at")
        run.ended_at = data.get("ended_at")
        run.status = data.get("status", "created")
        run.parameters = data.get("parameters", {})
        run.metrics = data.get("metrics", {})
        run.artifacts = data.get("artifacts", {})
        run.logs = data.get("logs", [])
        run.metadata = data.get("metadata", {})
        run.history = data.get("history", {})
        
        return run
    
    def save(self, directory: str) -> str:
        """
        Save the run to a file.
        
        Args:
            directory: Directory to save the run to.
            
        Returns:
            Path to the saved run file.
        """
        os.makedirs(directory, exist_ok=True)
        
        file_path = os.path.join(directory, f"{self.run_id}.json")
        
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return file_path
    
    @classmethod
    def load(cls, file_path: str):
        """
        Load a run from a file.
        
        Args:
            file_path: Path to the run file.
            
        Returns:
            Run object.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file is not valid JSON.
        """
        with open(file_path, "r") as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    def __repr__(self) -> str:
        """
        Get string representation of the run.
        
        Returns:
            String representation.
        """
        return f"Run(id={self.run_id}, name={self.name}, status={self.status})"
