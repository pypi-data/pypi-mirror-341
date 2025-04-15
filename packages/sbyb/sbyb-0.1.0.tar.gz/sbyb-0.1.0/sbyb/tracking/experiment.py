"""
Experiment class for SBYB tracking.

This module provides the Experiment class, which represents a collection of related runs
for a machine learning experiment.
"""

from typing import Any, Dict, List, Optional, Union
import os
import json
import datetime
import uuid
from pathlib import Path

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import TrackingError


class Experiment(SBYBComponent):
    """
    Represents a collection of related runs for a machine learning experiment.
    
    An experiment groups together multiple runs that are part of the same
    machine learning task or investigation. It provides methods for managing
    runs, tracking metadata, and comparing results.
    """
    
    def __init__(self, name: str, description: Optional[str] = None, 
                tags: Optional[List[str]] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a new experiment.
        
        Args:
            name: Name of the experiment.
            description: Optional description of the experiment.
            tags: Optional list of tags for categorizing the experiment.
            config: Optional configuration dictionary.
        """
        super().__init__(config)
        
        self.name = name
        self.description = description or ""
        self.tags = tags or []
        self.experiment_id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now().isoformat()
        self.runs = []
        self.metadata = {}
        
    def add_run(self, run) -> None:
        """
        Add a run to this experiment.
        
        Args:
            run: Run object to add to this experiment.
        """
        run.experiment_id = self.experiment_id
        self.runs.append(run)
    
    def get_run(self, run_id: str):
        """
        Get a run by ID.
        
        Args:
            run_id: ID of the run to retrieve.
            
        Returns:
            Run object if found, None otherwise.
        """
        for run in self.runs:
            if run.run_id == run_id:
                return run
        return None
    
    def get_runs(self) -> List:
        """
        Get all runs in this experiment.
        
        Returns:
            List of Run objects.
        """
        return self.runs
    
    def get_best_run(self, metric: str, higher_is_better: bool = True):
        """
        Get the best run based on a metric.
        
        Args:
            metric: Name of the metric to use for comparison.
            higher_is_better: Whether higher values of the metric are better.
            
        Returns:
            Best Run object if found, None otherwise.
            
        Raises:
            TrackingError: If no runs have the specified metric.
        """
        if not self.runs:
            return None
        
        valid_runs = [run for run in self.runs if metric in run.metrics]
        
        if not valid_runs:
            raise TrackingError(f"No runs have the metric '{metric}'")
        
        if higher_is_better:
            return max(valid_runs, key=lambda run: run.metrics[metric])
        else:
            return min(valid_runs, key=lambda run: run.metrics[metric])
    
    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add metadata to the experiment.
        
        Args:
            key: Metadata key.
            value: Metadata value.
        """
        self.metadata[key] = value
    
    def get_metadata(self, key: str) -> Any:
        """
        Get metadata from the experiment.
        
        Args:
            key: Metadata key.
            
        Returns:
            Metadata value if found, None otherwise.
        """
        return self.metadata.get(key)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the experiment to a dictionary.
        
        Returns:
            Dictionary representation of the experiment.
        """
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "created_at": self.created_at,
            "metadata": self.metadata,
            "runs": [run.to_dict() for run in self.runs]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Create an experiment from a dictionary.
        
        Args:
            data: Dictionary representation of the experiment.
            
        Returns:
            Experiment object.
        """
        from sbyb.tracking.run import Run
        
        experiment = cls(
            name=data["name"],
            description=data.get("description", ""),
            tags=data.get("tags", [])
        )
        
        experiment.experiment_id = data["experiment_id"]
        experiment.created_at = data["created_at"]
        experiment.metadata = data.get("metadata", {})
        
        for run_data in data.get("runs", []):
            run = Run.from_dict(run_data)
            experiment.runs.append(run)
        
        return experiment
    
    def save(self, directory: str) -> str:
        """
        Save the experiment to a file.
        
        Args:
            directory: Directory to save the experiment to.
            
        Returns:
            Path to the saved experiment file.
        """
        os.makedirs(directory, exist_ok=True)
        
        file_path = os.path.join(directory, f"{self.experiment_id}.json")
        
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return file_path
    
    @classmethod
    def load(cls, file_path: str):
        """
        Load an experiment from a file.
        
        Args:
            file_path: Path to the experiment file.
            
        Returns:
            Experiment object.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file is not valid JSON.
        """
        with open(file_path, "r") as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    def compare_runs(self, metrics: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Compare runs based on specified metrics.
        
        Args:
            metrics: List of metric names to compare.
            
        Returns:
            Dictionary mapping run IDs to dictionaries of metric values.
        """
        result = {}
        
        for run in self.runs:
            run_metrics = {}
            for metric in metrics:
                if metric in run.metrics:
                    run_metrics[metric] = run.metrics[metric]
                else:
                    run_metrics[metric] = None
            
            result[run.run_id] = {
                "metrics": run_metrics,
                "parameters": run.parameters,
                "name": run.name,
                "status": run.status
            }
        
        return result
    
    def __repr__(self) -> str:
        """
        Get string representation of the experiment.
        
        Returns:
            String representation.
        """
        return f"Experiment(id={self.experiment_id}, name={self.name}, runs={len(self.runs)})"
