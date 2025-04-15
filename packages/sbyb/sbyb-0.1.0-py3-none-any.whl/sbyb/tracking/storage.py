"""
Storage class for SBYB tracking.

This module provides storage backends for experiment tracking data,
with a focus on local storage without requiring external services.
"""

from typing import Any, Dict, List, Optional, Union
import os
import json
import glob
import shutil
from pathlib import Path
import datetime

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import TrackingError
from sbyb.tracking.experiment import Experiment
from sbyb.tracking.run import Run


class LocalStorage(SBYBComponent):
    """
    Local storage backend for experiment tracking.
    
    This component provides functionality for storing and retrieving
    experiments and runs from the local filesystem.
    """
    
    def __init__(self, root_dir: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the local storage backend.
        
        Args:
            root_dir: Root directory for storing tracking data. Defaults to ~/.sbyb/tracking.
            config: Optional configuration dictionary.
        """
        super().__init__(config)
        
        self.root_dir = root_dir or os.path.expanduser("~/.sbyb/tracking")
        self.experiments_dir = os.path.join(self.root_dir, "experiments")
        self.runs_dir = os.path.join(self.root_dir, "runs")
        self.artifacts_dir = os.path.join(self.root_dir, "artifacts")
        
        # Create directories if they don't exist
        os.makedirs(self.experiments_dir, exist_ok=True)
        os.makedirs(self.runs_dir, exist_ok=True)
        os.makedirs(self.artifacts_dir, exist_ok=True)
    
    def save_experiment(self, experiment: Experiment) -> str:
        """
        Save an experiment to storage.
        
        Args:
            experiment: Experiment object to save.
            
        Returns:
            Path to the saved experiment file.
        """
        experiment_dir = os.path.join(self.experiments_dir, experiment.experiment_id)
        os.makedirs(experiment_dir, exist_ok=True)
        
        # Save experiment metadata
        file_path = os.path.join(experiment_dir, "experiment.json")
        
        with open(file_path, "w") as f:
            json.dump(experiment.to_dict(), f, indent=2)
        
        # Save runs
        for run in experiment.runs:
            self.save_run(run)
        
        return file_path
    
    def load_experiment(self, experiment_id: str) -> Experiment:
        """
        Load an experiment from storage.
        
        Args:
            experiment_id: ID of the experiment to load.
            
        Returns:
            Loaded Experiment object.
            
        Raises:
            TrackingError: If the experiment is not found.
        """
        experiment_dir = os.path.join(self.experiments_dir, experiment_id)
        file_path = os.path.join(experiment_dir, "experiment.json")
        
        if not os.path.exists(file_path):
            raise TrackingError(f"Experiment not found: {experiment_id}")
        
        with open(file_path, "r") as f:
            data = json.load(f)
        
        return Experiment.from_dict(data)
    
    def delete_experiment(self, experiment_id: str) -> bool:
        """
        Delete an experiment from storage.
        
        Args:
            experiment_id: ID of the experiment to delete.
            
        Returns:
            True if the experiment was deleted, False otherwise.
        """
        experiment_dir = os.path.join(self.experiments_dir, experiment_id)
        
        if not os.path.exists(experiment_dir):
            return False
        
        # Load experiment to get run IDs
        try:
            experiment = self.load_experiment(experiment_id)
            
            # Delete runs
            for run in experiment.runs:
                self.delete_run(run.run_id)
        except Exception:
            # Continue with deletion even if loading fails
            pass
        
        # Delete experiment directory
        shutil.rmtree(experiment_dir)
        
        return True
    
    def list_experiments(self) -> List[Dict[str, Any]]:
        """
        List all experiments in storage.
        
        Returns:
            List of experiment metadata dictionaries.
        """
        experiments = []
        
        for experiment_dir in glob.glob(os.path.join(self.experiments_dir, "*")):
            if os.path.isdir(experiment_dir):
                experiment_id = os.path.basename(experiment_dir)
                file_path = os.path.join(experiment_dir, "experiment.json")
                
                if os.path.exists(file_path):
                    try:
                        with open(file_path, "r") as f:
                            data = json.load(f)
                        
                        experiments.append({
                            "experiment_id": data["experiment_id"],
                            "name": data["name"],
                            "description": data.get("description", ""),
                            "tags": data.get("tags", []),
                            "created_at": data["created_at"],
                            "run_count": len(data.get("runs", [])),
                            "metadata": data.get("metadata", {})
                        })
                    except Exception as e:
                        # Skip invalid experiment files
                        continue
        
        return experiments
    
    def save_run(self, run: Run) -> str:
        """
        Save a run to storage.
        
        Args:
            run: Run object to save.
            
        Returns:
            Path to the saved run file.
        """
        run_dir = os.path.join(self.runs_dir, run.run_id)
        os.makedirs(run_dir, exist_ok=True)
        
        # Create artifacts directory for this run
        artifacts_dir = os.path.join(self.artifacts_dir, run.run_id)
        os.makedirs(artifacts_dir, exist_ok=True)
        
        # Process artifacts to ensure they're properly saved
        for key, artifact_info in list(run.artifacts.items()):
            if artifact_info["location"] == "memory" and "value" in artifact_info:
                # Save in-memory artifact to file
                artifact_path = os.path.join(artifacts_dir, f"{key}.pkl")
                
                import pickle
                with open(artifact_path, "wb") as f:
                    pickle.dump(artifact_info["value"], f)
                
                # Update artifact info
                run.artifacts[key] = {
                    "type": artifact_info["type"],
                    "location": artifact_path
                }
        
        # Save run metadata
        file_path = os.path.join(run_dir, "run.json")
        
        with open(file_path, "w") as f:
            json.dump(run.to_dict(), f, indent=2)
        
        return file_path
    
    def load_run(self, run_id: str) -> Run:
        """
        Load a run from storage.
        
        Args:
            run_id: ID of the run to load.
            
        Returns:
            Loaded Run object.
            
        Raises:
            TrackingError: If the run is not found.
        """
        run_dir = os.path.join(self.runs_dir, run_id)
        file_path = os.path.join(run_dir, "run.json")
        
        if not os.path.exists(file_path):
            raise TrackingError(f"Run not found: {run_id}")
        
        with open(file_path, "r") as f:
            data = json.load(f)
        
        return Run.from_dict(data)
    
    def delete_run(self, run_id: str) -> bool:
        """
        Delete a run from storage.
        
        Args:
            run_id: ID of the run to delete.
            
        Returns:
            True if the run was deleted, False otherwise.
        """
        run_dir = os.path.join(self.runs_dir, run_id)
        artifacts_dir = os.path.join(self.artifacts_dir, run_id)
        
        if not os.path.exists(run_dir):
            return False
        
        # Delete run directory
        shutil.rmtree(run_dir)
        
        # Delete artifacts directory if it exists
        if os.path.exists(artifacts_dir):
            shutil.rmtree(artifacts_dir)
        
        return True
    
    def list_runs(self, experiment_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all runs in storage, optionally filtered by experiment ID.
        
        Args:
            experiment_id: Optional experiment ID to filter by.
            
        Returns:
            List of run metadata dictionaries.
        """
        runs = []
        
        for run_dir in glob.glob(os.path.join(self.runs_dir, "*")):
            if os.path.isdir(run_dir):
                run_id = os.path.basename(run_dir)
                file_path = os.path.join(run_dir, "run.json")
                
                if os.path.exists(file_path):
                    try:
                        with open(file_path, "r") as f:
                            data = json.load(f)
                        
                        if experiment_id is None or data.get("experiment_id") == experiment_id:
                            runs.append({
                                "run_id": data["run_id"],
                                "experiment_id": data.get("experiment_id"),
                                "name": data["name"],
                                "status": data.get("status", "unknown"),
                                "created_at": data["created_at"],
                                "started_at": data.get("started_at"),
                                "ended_at": data.get("ended_at"),
                                "metrics": data.get("metrics", {}),
                                "parameters": data.get("parameters", {})
                            })
                    except Exception as e:
                        # Skip invalid run files
                        continue
        
        return runs
    
    def get_artifact_path(self, run_id: str, artifact_name: str) -> str:
        """
        Get the path to an artifact.
        
        Args:
            run_id: ID of the run.
            artifact_name: Name of the artifact.
            
        Returns:
            Path to the artifact.
            
        Raises:
            TrackingError: If the run or artifact is not found.
        """
        run = self.load_run(run_id)
        
        if artifact_name not in run.artifacts:
            raise TrackingError(f"Artifact not found: {artifact_name}")
        
        artifact_info = run.artifacts[artifact_name]
        
        if artifact_info["location"] == "memory":
            raise TrackingError(f"Artifact is stored in memory, not on disk: {artifact_name}")
        
        return artifact_info["location"]
    
    def backup(self, backup_dir: str) -> str:
        """
        Backup all tracking data to a directory.
        
        Args:
            backup_dir: Directory to backup to.
            
        Returns:
            Path to the backup directory.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"sbyb_tracking_backup_{timestamp}")
        
        os.makedirs(backup_path, exist_ok=True)
        
        # Copy all data
        shutil.copytree(self.experiments_dir, os.path.join(backup_path, "experiments"))
        shutil.copytree(self.runs_dir, os.path.join(backup_path, "runs"))
        shutil.copytree(self.artifacts_dir, os.path.join(backup_path, "artifacts"))
        
        return backup_path
    
    def restore(self, backup_path: str) -> bool:
        """
        Restore tracking data from a backup.
        
        Args:
            backup_path: Path to the backup directory.
            
        Returns:
            True if the restore was successful, False otherwise.
        """
        if not os.path.exists(backup_path):
            return False
        
        experiments_backup = os.path.join(backup_path, "experiments")
        runs_backup = os.path.join(backup_path, "runs")
        artifacts_backup = os.path.join(backup_path, "artifacts")
        
        if not all(os.path.exists(p) for p in [experiments_backup, runs_backup, artifacts_backup]):
            return False
        
        # Clear existing data
        shutil.rmtree(self.experiments_dir)
        shutil.rmtree(self.runs_dir)
        shutil.rmtree(self.artifacts_dir)
        
        # Restore from backup
        shutil.copytree(experiments_backup, self.experiments_dir)
        shutil.copytree(runs_backup, self.runs_dir)
        shutil.copytree(artifacts_backup, self.artifacts_dir)
        
        return True
