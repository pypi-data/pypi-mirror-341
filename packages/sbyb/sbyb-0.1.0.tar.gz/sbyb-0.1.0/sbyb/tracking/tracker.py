"""
Experiment tracker for SBYB.

This module provides the ExperimentTracker class, which is the main interface
for tracking machine learning experiments locally without requiring external services.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import datetime
import uuid
from pathlib import Path
import logging

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import TrackingError
from sbyb.tracking.experiment import Experiment
from sbyb.tracking.run import Run
from sbyb.tracking.storage import LocalStorage


class ExperimentTracker(SBYBComponent):
    """
    Main interface for tracking machine learning experiments.
    
    This component provides a unified interface for creating and managing
    experiments and runs, logging metrics, parameters, and artifacts,
    and querying tracking data.
    """
    
    def __init__(self, tracking_dir: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the experiment tracker.
        
        Args:
            tracking_dir: Directory for storing tracking data. Defaults to ~/.sbyb/tracking.
            config: Optional configuration dictionary.
        """
        super().__init__(config)
        
        # Set up logging
        self.logger = logging.getLogger("sbyb.tracking")
        
        # Initialize storage
        self.storage = LocalStorage(root_dir=tracking_dir, config=config)
        
        # Current experiment and run
        self.current_experiment = None
        self.current_run = None
    
    def create_experiment(self, name: str, description: Optional[str] = None,
                         tags: Optional[List[str]] = None) -> Experiment:
        """
        Create a new experiment.
        
        Args:
            name: Name of the experiment.
            description: Optional description of the experiment.
            tags: Optional list of tags for categorizing the experiment.
            
        Returns:
            Created Experiment object.
        """
        experiment = Experiment(name=name, description=description, tags=tags)
        self.current_experiment = experiment
        self.storage.save_experiment(experiment)
        
        self.logger.info(f"Created experiment: {name} (ID: {experiment.experiment_id})")
        return experiment
    
    def get_experiment(self, experiment_id: str) -> Experiment:
        """
        Get an experiment by ID.
        
        Args:
            experiment_id: ID of the experiment to retrieve.
            
        Returns:
            Retrieved Experiment object.
            
        Raises:
            TrackingError: If the experiment is not found.
        """
        return self.storage.load_experiment(experiment_id)
    
    def set_experiment(self, experiment_id: str) -> Experiment:
        """
        Set the current experiment.
        
        Args:
            experiment_id: ID of the experiment to set as current.
            
        Returns:
            Set Experiment object.
            
        Raises:
            TrackingError: If the experiment is not found.
        """
        experiment = self.storage.load_experiment(experiment_id)
        self.current_experiment = experiment
        
        self.logger.info(f"Set current experiment: {experiment.name} (ID: {experiment.experiment_id})")
        return experiment
    
    def list_experiments(self) -> List[Dict[str, Any]]:
        """
        List all experiments.
        
        Returns:
            List of experiment metadata dictionaries.
        """
        return self.storage.list_experiments()
    
    def delete_experiment(self, experiment_id: str) -> bool:
        """
        Delete an experiment.
        
        Args:
            experiment_id: ID of the experiment to delete.
            
        Returns:
            True if the experiment was deleted, False otherwise.
        """
        if self.current_experiment and self.current_experiment.experiment_id == experiment_id:
            self.current_experiment = None
        
        return self.storage.delete_experiment(experiment_id)
    
    def create_run(self, name: Optional[str] = None, description: Optional[str] = None,
                  tags: Optional[List[str]] = None) -> Run:
        """
        Create a new run.
        
        Args:
            name: Optional name of the run.
            description: Optional description of the run.
            tags: Optional list of tags for categorizing the run.
            
        Returns:
            Created Run object.
            
        Raises:
            TrackingError: If no current experiment is set.
        """
        if not self.current_experiment:
            raise TrackingError("No current experiment set. Call create_experiment() or set_experiment() first.")
        
        run = Run(name=name, description=description, tags=tags)
        run.experiment_id = self.current_experiment.experiment_id
        
        self.current_experiment.add_run(run)
        self.current_run = run
        
        # Save both the run and the updated experiment
        self.storage.save_run(run)
        self.storage.save_experiment(self.current_experiment)
        
        self.logger.info(f"Created run: {run.name} (ID: {run.run_id})")
        return run
    
    def get_run(self, run_id: str) -> Run:
        """
        Get a run by ID.
        
        Args:
            run_id: ID of the run to retrieve.
            
        Returns:
            Retrieved Run object.
            
        Raises:
            TrackingError: If the run is not found.
        """
        return self.storage.load_run(run_id)
    
    def set_run(self, run_id: str) -> Run:
        """
        Set the current run.
        
        Args:
            run_id: ID of the run to set as current.
            
        Returns:
            Set Run object.
            
        Raises:
            TrackingError: If the run is not found.
        """
        run = self.storage.load_run(run_id)
        
        # If the run belongs to a different experiment, load and set that experiment
        if run.experiment_id and (not self.current_experiment or 
                                 run.experiment_id != self.current_experiment.experiment_id):
            try:
                self.current_experiment = self.storage.load_experiment(run.experiment_id)
            except TrackingError:
                # If the experiment doesn't exist, just set the run
                pass
        
        self.current_run = run
        
        self.logger.info(f"Set current run: {run.name} (ID: {run.run_id})")
        return run
    
    def list_runs(self, experiment_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all runs, optionally filtered by experiment ID.
        
        Args:
            experiment_id: Optional experiment ID to filter by.
            
        Returns:
            List of run metadata dictionaries.
        """
        if experiment_id is None and self.current_experiment:
            experiment_id = self.current_experiment.experiment_id
        
        return self.storage.list_runs(experiment_id)
    
    def delete_run(self, run_id: str) -> bool:
        """
        Delete a run.
        
        Args:
            run_id: ID of the run to delete.
            
        Returns:
            True if the run was deleted, False otherwise.
        """
        if self.current_run and self.current_run.run_id == run_id:
            self.current_run = None
        
        # If the run is part of the current experiment, remove it from there too
        if self.current_experiment:
            run = self.current_experiment.get_run(run_id)
            if run:
                self.current_experiment.runs.remove(run)
                self.storage.save_experiment(self.current_experiment)
        
        return self.storage.delete_run(run_id)
    
    def start_run(self) -> Run:
        """
        Start the current run.
        
        Returns:
            Started Run object.
            
        Raises:
            TrackingError: If no current run is set.
        """
        if not self.current_run:
            raise TrackingError("No current run set. Call create_run() or set_run() first.")
        
        self.current_run.start()
        self.storage.save_run(self.current_run)
        
        self.logger.info(f"Started run: {self.current_run.name} (ID: {self.current_run.run_id})")
        return self.current_run
    
    def end_run(self, status: str = "completed", error_message: Optional[str] = None) -> Run:
        """
        End the current run.
        
        Args:
            status: Status of the run. Either "completed" or "failed".
            error_message: Optional error message if the run failed.
            
        Returns:
            Ended Run object.
            
        Raises:
            TrackingError: If no current run is set.
        """
        if not self.current_run:
            raise TrackingError("No current run set. Call create_run() or set_run() first.")
        
        if status == "completed":
            self.current_run.complete()
        elif status == "failed":
            self.current_run.fail(error_message or "Run failed")
        else:
            raise TrackingError(f"Invalid run status: {status}. Must be 'completed' or 'failed'.")
        
        self.storage.save_run(self.current_run)
        
        self.logger.info(f"Ended run: {self.current_run.name} (ID: {self.current_run.run_id}) with status {status}")
        return self.current_run
    
    def log_parameter(self, key: str, value: Any) -> None:
        """
        Log a parameter for the current run.
        
        Args:
            key: Parameter name.
            value: Parameter value.
            
        Raises:
            TrackingError: If no current run is set.
        """
        if not self.current_run:
            raise TrackingError("No current run set. Call create_run() or set_run() first.")
        
        self.current_run.log_parameter(key, value)
        self.storage.save_run(self.current_run)
    
    def log_parameters(self, params: Dict[str, Any]) -> None:
        """
        Log multiple parameters for the current run.
        
        Args:
            params: Dictionary of parameter names and values.
            
        Raises:
            TrackingError: If no current run is set.
        """
        if not self.current_run:
            raise TrackingError("No current run set. Call create_run() or set_run() first.")
        
        self.current_run.log_parameters(params)
        self.storage.save_run(self.current_run)
    
    def log_metric(self, key: str, value: Union[int, float]) -> None:
        """
        Log a metric for the current run.
        
        Args:
            key: Metric name.
            value: Metric value.
            
        Raises:
            TrackingError: If no current run is set or the value is not a number.
        """
        if not self.current_run:
            raise TrackingError("No current run set. Call create_run() or set_run() first.")
        
        self.current_run.log_metric(key, value)
        self.storage.save_run(self.current_run)
    
    def log_metrics(self, metrics: Dict[str, Union[int, float]]) -> None:
        """
        Log multiple metrics for the current run.
        
        Args:
            metrics: Dictionary of metric names and values.
            
        Raises:
            TrackingError: If no current run is set.
        """
        if not self.current_run:
            raise TrackingError("No current run set. Call create_run() or set_run() first.")
        
        self.current_run.log_metrics(metrics)
        self.storage.save_run(self.current_run)
    
    def log_metric_step(self, key: str, value: Union[int, float], step: int) -> None:
        """
        Log a metric with a step for the current run.
        
        Args:
            key: Metric name.
            value: Metric value.
            step: Step number.
            
        Raises:
            TrackingError: If no current run is set or the value is not a number.
        """
        if not self.current_run:
            raise TrackingError("No current run set. Call create_run() or set_run() first.")
        
        self.current_run.log_metric_step(key, value, step)
        self.storage.save_run(self.current_run)
    
    def log_artifact(self, key: str, artifact: Any, artifact_path: Optional[str] = None) -> str:
        """
        Log an artifact for the current run.
        
        Args:
            key: Artifact name.
            artifact: Artifact object.
            artifact_path: Optional path to save the artifact. If None, a path is generated.
            
        Returns:
            Path to the saved artifact.
            
        Raises:
            TrackingError: If no current run is set.
        """
        if not self.current_run:
            raise TrackingError("No current run set. Call create_run() or set_run() first.")
        
        if artifact_path is None:
            # Generate a path in the artifacts directory
            artifacts_dir = os.path.join(self.storage.artifacts_dir, self.current_run.run_id)
            os.makedirs(artifacts_dir, exist_ok=True)
            
            artifact_path = os.path.join(artifacts_dir, f"{key}")
            
            # Add appropriate extension based on artifact type
            if hasattr(artifact, "savefig"):  # matplotlib figure
                artifact_path += ".png"
            elif isinstance(artifact, (dict, list)):
                artifact_path += ".json"
            else:
                artifact_path += ".pkl"
        
        location = self.current_run.log_artifact(key, artifact, artifact_path)
        self.storage.save_run(self.current_run)
        
        return location
    
    def log_model(self, model: Any, model_path: Optional[str] = None) -> str:
        """
        Log a model for the current run.
        
        Args:
            model: Model object.
            model_path: Optional path to save the model. If None, a path is generated.
            
        Returns:
            Path to the saved model.
            
        Raises:
            TrackingError: If no current run is set.
        """
        if not self.current_run:
            raise TrackingError("No current run set. Call create_run() or set_run() first.")
        
        if model_path is None:
            # Generate a path in the artifacts directory
            artifacts_dir = os.path.join(self.storage.artifacts_dir, self.current_run.run_id)
            os.makedirs(artifacts_dir, exist_ok=True)
            
            model_path = os.path.join(artifacts_dir, "model.pkl")
        
        location = self.current_run.log_model(model, model_path)
        self.storage.save_run(self.current_run)
        
        return location
    
    def log_message(self, message: str) -> None:
        """
        Log a message for the current run.
        
        Args:
            message: Message to log.
            
        Raises:
            TrackingError: If no current run is set.
        """
        if not self.current_run:
            raise TrackingError("No current run set. Call create_run() or set_run() first.")
        
        self.current_run.log_message(message)
        self.storage.save_run(self.current_run)
    
    def add_metadata(self, key: str, value: Any, target: str = "run") -> None:
        """
        Add metadata to the current run or experiment.
        
        Args:
            key: Metadata key.
            value: Metadata value.
            target: Target for the metadata. Either "run" or "experiment".
            
        Raises:
            TrackingError: If no current run or experiment is set.
        """
        if target == "run":
            if not self.current_run:
                raise TrackingError("No current run set. Call create_run() or set_run() first.")
            
            self.current_run.add_metadata(key, value)
            self.storage.save_run(self.current_run)
        elif target == "experiment":
            if not self.current_experiment:
                raise TrackingError("No current experiment set. Call create_experiment() or set_experiment() first.")
            
            self.current_experiment.add_metadata(key, value)
            self.storage.save_experiment(self.current_experiment)
        else:
            raise TrackingError(f"Invalid target: {target}. Must be 'run' or 'experiment'.")
    
    def get_metadata(self, key: str, target: str = "run") -> Any:
        """
        Get metadata from the current run or experiment.
        
        Args:
            key: Metadata key.
            target: Target for the metadata. Either "run" or "experiment".
            
        Returns:
            Metadata value if found, None otherwise.
            
        Raises:
            TrackingError: If no current run or experiment is set.
        """
        if target == "run":
            if not self.current_run:
                raise TrackingError("No current run set. Call create_run() or set_run() first.")
            
            return self.current_run.get_metadata(key)
        elif target == "experiment":
            if not self.current_experiment:
                raise TrackingError("No current experiment set. Call create_experiment() or set_experiment() first.")
            
            return self.current_experiment.get_metadata(key)
        else:
            raise TrackingError(f"Invalid target: {target}. Must be 'run' or 'experiment'.")
    
    def get_best_run(self, metric: str, higher_is_better: bool = True):
        """
        Get the best run in the current experiment based on a metric.
        
        Args:
            metric: Name of the metric to use for comparison.
            higher_is_better: Whether higher values of the metric are better.
            
        Returns:
            Best Run object if found, None otherwise.
            
        Raises:
            TrackingError: If no current experiment is set or no runs have the specified metric.
        """
        if not self.current_experiment:
            raise TrackingError("No current experiment set. Call create_experiment() or set_experiment() first.")
        
        return self.current_experiment.get_best_run(metric, higher_is_better)
    
    def compare_runs(self, run_ids: List[str], metrics: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Compare runs based on specified metrics.
        
        Args:
            run_ids: List of run IDs to compare.
            metrics: List of metric names to compare.
            
        Returns:
            Dictionary mapping run IDs to dictionaries of metric values.
            
        Raises:
            TrackingError: If any of the runs are not found.
        """
        result = {}
        
        for run_id in run_ids:
            run = self.storage.load_run(run_id)
            
            run_metrics = {}
            for metric in metrics:
                if metric in run.metrics:
                    run_metrics[metric] = run.metrics[metric]
                else:
                    run_metrics[metric] = None
            
            result[run_id] = {
                "metrics": run_metrics,
                "parameters": run.parameters,
                "name": run.name,
                "status": run.status
            }
        
        return result
    
    def backup(self, backup_dir: Optional[str] = None) -> str:
        """
        Backup all tracking data to a directory.
        
        Args:
            backup_dir: Directory to backup to. If None, a directory in the current
                       working directory is created.
            
        Returns:
            Path to the backup directory.
        """
        if backup_dir is None:
            backup_dir = os.path.join(os.getcwd(), "sbyb_backups")
            os.makedirs(backup_dir, exist_ok=True)
        
        return self.storage.backup(backup_dir)
    
    def restore(self, backup_path: str) -> bool:
        """
        Restore tracking data from a backup.
        
        Args:
            backup_path: Path to the backup directory.
            
        Returns:
            True if the restore was successful, False otherwise.
        """
        success = self.storage.restore(backup_path)
        
        if success:
            # Reset current experiment and run
            self.current_experiment = None
            self.current_run = None
        
        return success
    
    def __enter__(self):
        """
        Enter context manager.
        
        Returns:
            Self.
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context manager.
        
        Args:
            exc_type: Exception type.
            exc_val: Exception value.
            exc_tb: Exception traceback.
        """
        if self.current_run and self.current_run.status == "running":
            if exc_type:
                # An exception occurred, mark the run as failed
                self.end_run(status="failed", error_message=str(exc_val))
            else:
                # No exception, mark the run as completed
                self.end_run(status="completed")
