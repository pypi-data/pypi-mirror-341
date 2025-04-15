"""
Model monitoring component for SBYB deployment.

This module provides functionality for monitoring machine learning models
in production environments.
"""

from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import os
import json
import time
import datetime
import logging
import threading
import queue
import numpy as np
import pandas as pd
from collections import deque

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import MonitoringError


class ModelMonitor(SBYBComponent):
    """
    Model monitoring component.
    
    This component monitors machine learning models in production environments.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the model monitor.
        
        Args:
            config: Configuration dictionary for the monitor.
        """
        super().__init__(config)
        self.logger = logging.getLogger("sbyb.deployment.monitoring")
        self.metrics = {}
        self.alerts = []
        self.predictions_log = deque(maxlen=10000)  # Store last 10,000 predictions
        self.monitoring_thread = None
        self.stop_monitoring = threading.Event()
        self.metrics_queue = queue.Queue()
        self.alert_callbacks = []
    
    def start_monitoring(self, model: Any, check_interval: int = 60) -> None:
        """
        Start monitoring a model.
        
        Args:
            model: The model to monitor.
            check_interval: Interval between checks in seconds.
        """
        if self.monitoring_thread is not None and self.monitoring_thread.is_alive():
            raise MonitoringError("Monitoring is already running.")
        
        # Reset stop flag
        self.stop_monitoring.clear()
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(model, check_interval),
            daemon=True
        )
        self.monitoring_thread.start()
        
        self.logger.info(f"Model monitoring started with check interval of {check_interval} seconds.")
    
    def stop_monitoring(self) -> None:
        """
        Stop monitoring.
        """
        if self.monitoring_thread is None or not self.monitoring_thread.is_alive():
            self.logger.warning("Monitoring is not running.")
            return
        
        # Set stop flag
        self.stop_monitoring.set()
        
        # Wait for thread to terminate
        self.monitoring_thread.join(timeout=5.0)
        
        if self.monitoring_thread.is_alive():
            self.logger.warning("Monitoring thread did not terminate gracefully.")
        else:
            self.logger.info("Model monitoring stopped.")
    
    def log_prediction(self, inputs: Any, prediction: Any, 
                      ground_truth: Optional[Any] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a prediction for monitoring.
        
        Args:
            inputs: Input data for the prediction.
            prediction: Model prediction.
            ground_truth: Actual ground truth (if available).
            metadata: Additional metadata.
        """
        # Create prediction log entry
        timestamp = datetime.datetime.now().isoformat()
        
        log_entry = {
            'timestamp': timestamp,
            'prediction': self._convert_to_serializable(prediction),
            'metadata': metadata or {}
        }
        
        # Add inputs if not too large
        try:
            log_entry['inputs'] = self._convert_to_serializable(inputs)
        except Exception as e:
            log_entry['inputs'] = str(e)
        
        # Add ground truth if available
        if ground_truth is not None:
            log_entry['ground_truth'] = self._convert_to_serializable(ground_truth)
        
        # Add to predictions log
        self.predictions_log.append(log_entry)
        
        # Add to metrics queue for processing
        self.metrics_queue.put(log_entry)
    
    def add_metric(self, name: str, calculator: Callable, 
                  threshold: Optional[float] = None,
                  alert_condition: Optional[str] = None) -> None:
        """
        Add a metric to monitor.
        
        Args:
            name: Name of the metric.
            calculator: Function to calculate the metric.
            threshold: Threshold for alerting.
            alert_condition: Condition for alerting ('above', 'below', 'equal').
        """
        self.metrics[name] = {
            'calculator': calculator,
            'threshold': threshold,
            'alert_condition': alert_condition,
            'values': [],
            'timestamps': []
        }
        
        self.logger.info(f"Added metric '{name}' to monitoring.")
    
    def add_alert_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Add a callback function for alerts.
        
        Args:
            callback: Function to call when an alert is triggered.
        """
        self.alert_callbacks.append(callback)
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get all metrics.
        
        Returns:
            Dictionary of metrics.
        """
        # Create a copy of metrics without the calculator functions
        metrics_copy = {}
        for name, metric in self.metrics.items():
            metrics_copy[name] = {
                'threshold': metric['threshold'],
                'alert_condition': metric['alert_condition'],
                'values': metric['values'],
                'timestamps': metric['timestamps']
            }
        
        return metrics_copy
    
    def get_alerts(self) -> List[Dict[str, Any]]:
        """
        Get all alerts.
        
        Returns:
            List of alerts.
        """
        return self.alerts
    
    def get_predictions_log(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get the predictions log.
        
        Args:
            limit: Maximum number of log entries to return.
            
        Returns:
            List of prediction log entries.
        """
        if limit is None or limit >= len(self.predictions_log):
            return list(self.predictions_log)
        else:
            return list(self.predictions_log)[-limit:]
    
    def export_metrics(self, output_file: str) -> None:
        """
        Export metrics to a file.
        
        Args:
            output_file: Path to the output file.
        """
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        # Get metrics
        metrics = self.get_metrics()
        
        # Add export timestamp
        metrics['export_timestamp'] = datetime.datetime.now().isoformat()
        
        # Write to file
        with open(output_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        self.logger.info(f"Metrics exported to {output_file}")
    
    def export_predictions_log(self, output_file: str) -> None:
        """
        Export predictions log to a file.
        
        Args:
            output_file: Path to the output file.
        """
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        # Get predictions log
        predictions_log = self.get_predictions_log()
        
        # Write to file
        with open(output_file, 'w') as f:
            json.dump(predictions_log, f, indent=2)
        
        self.logger.info(f"Predictions log exported to {output_file}")
    
    def calculate_drift(self, reference_data: pd.DataFrame, current_data: pd.DataFrame,
                       method: str = 'ks_test') -> Dict[str, Any]:
        """
        Calculate data drift between reference and current data.
        
        Args:
            reference_data: Reference data.
            current_data: Current data.
            method: Method for calculating drift.
            
        Returns:
            Dictionary with drift metrics.
        """
        from scipy import stats
        
        if method not in ['ks_test', 'chi2_test', 'js_divergence']:
            raise MonitoringError(f"Unsupported drift detection method: {method}")
        
        # Ensure data has the same columns
        common_columns = set(reference_data.columns) & set(current_data.columns)
        if not common_columns:
            raise MonitoringError("No common columns between reference and current data.")
        
        # Calculate drift for each column
        drift_metrics = {}
        
        for column in common_columns:
            ref_values = reference_data[column].dropna()
            cur_values = current_data[column].dropna()
            
            # Skip if not enough data
            if len(ref_values) < 10 or len(cur_values) < 10:
                drift_metrics[column] = {
                    'status': 'skipped',
                    'reason': 'Not enough data'
                }
                continue
            
            # Calculate drift based on method
            if method == 'ks_test':
                # Kolmogorov-Smirnov test for continuous data
                try:
                    statistic, p_value = stats.ks_2samp(ref_values, cur_values)
                    drift_metrics[column] = {
                        'method': 'ks_test',
                        'statistic': float(statistic),
                        'p_value': float(p_value),
                        'drift_detected': p_value < 0.05
                    }
                except Exception as e:
                    drift_metrics[column] = {
                        'status': 'error',
                        'reason': str(e)
                    }
            
            elif method == 'chi2_test':
                # Chi-squared test for categorical data
                try:
                    # Get unique values
                    all_values = pd.concat([ref_values, cur_values]).unique()
                    
                    # Count occurrences
                    ref_counts = pd.Series(ref_values).value_counts().reindex(all_values).fillna(0)
                    cur_counts = pd.Series(cur_values).value_counts().reindex(all_values).fillna(0)
                    
                    # Chi-squared test
                    statistic, p_value = stats.chisquare(cur_counts, ref_counts)
                    
                    drift_metrics[column] = {
                        'method': 'chi2_test',
                        'statistic': float(statistic),
                        'p_value': float(p_value),
                        'drift_detected': p_value < 0.05
                    }
                except Exception as e:
                    drift_metrics[column] = {
                        'status': 'error',
                        'reason': str(e)
                    }
            
            elif method == 'js_divergence':
                # Jensen-Shannon divergence
                try:
                    # Get unique values
                    all_values = pd.concat([ref_values, cur_values]).unique()
                    
                    # Count occurrences
                    ref_counts = pd.Series(ref_values).value_counts().reindex(all_values).fillna(0)
                    cur_counts = pd.Series(cur_values).value_counts().reindex(all_values).fillna(0)
                    
                    # Convert to probabilities
                    ref_probs = ref_counts / ref_counts.sum()
                    cur_probs = cur_counts / cur_counts.sum()
                    
                    # Calculate JS divergence
                    m = 0.5 * (ref_probs + cur_probs)
                    js_div = 0.5 * (stats.entropy(ref_probs, m) + stats.entropy(cur_probs, m))
                    
                    drift_metrics[column] = {
                        'method': 'js_divergence',
                        'divergence': float(js_div),
                        'drift_detected': js_div > 0.1  # Threshold can be adjusted
                    }
                except Exception as e:
                    drift_metrics[column] = {
                        'status': 'error',
                        'reason': str(e)
                    }
        
        # Overall drift status
        drift_detected = any(
            col_metrics.get('drift_detected', False)
            for col_metrics in drift_metrics.values()
            if isinstance(col_metrics, dict) and 'drift_detected' in col_metrics
        )
        
        return {
            'drift_detected': drift_detected,
            'column_metrics': drift_metrics,
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def calculate_performance_metrics(self, predictions: List[Any], 
                                     ground_truths: List[Any],
                                     task_type: str) -> Dict[str, float]:
        """
        Calculate performance metrics for a model.
        
        Args:
            predictions: List of predictions.
            ground_truths: List of ground truths.
            task_type: Type of task ('classification', 'regression').
            
        Returns:
            Dictionary of performance metrics.
        """
        if task_type == 'classification':
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
            
            try:
                metrics = {
                    'accuracy': float(accuracy_score(ground_truths, predictions)),
                    'precision': float(precision_score(ground_truths, predictions, average='weighted')),
                    'recall': float(recall_score(ground_truths, predictions, average='weighted')),
                    'f1': float(f1_score(ground_truths, predictions, average='weighted'))
                }
            except Exception as e:
                raise MonitoringError(f"Error calculating classification metrics: {str(e)}")
        
        elif task_type == 'regression':
            from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
            
            try:
                mse = mean_squared_error(ground_truths, predictions)
                metrics = {
                    'mse': float(mse),
                    'rmse': float(np.sqrt(mse)),
                    'mae': float(mean_absolute_error(ground_truths, predictions)),
                    'r2': float(r2_score(ground_truths, predictions))
                }
            except Exception as e:
                raise MonitoringError(f"Error calculating regression metrics: {str(e)}")
        
        else:
            raise MonitoringError(f"Unsupported task type: {task_type}")
        
        return metrics
    
    def _monitoring_loop(self, model: Any, check_interval: int) -> None:
        """
        Main monitoring loop.
        
        Args:
            model: The model to monitor.
            check_interval: Interval between checks in seconds.
        """
        while not self.stop_monitoring.is_set():
            try:
                # Process metrics queue
                self._process_metrics_queue()
                
                # Check for alerts
                self._check_alerts()
                
                # Wait for next check
                self.stop_monitoring.wait(check_interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {str(e)}")
    
    def _process_metrics_queue(self) -> None:
        """
        Process metrics queue.
        """
        # Get all items from queue
        items = []
        while not self.metrics_queue.empty():
            try:
                items.append(self.metrics_queue.get_nowait())
                self.metrics_queue.task_done()
            except queue.Empty:
                break
        
        if not items:
            return
        
        # Calculate metrics
        timestamp = datetime.datetime.now().isoformat()
        
        for name, metric in self.metrics.items():
            calculator = metric['calculator']
            
            try:
                # Calculate metric
                value = calculator(items)
                
                # Add to metric values
                metric['values'].append(value)
                metric['timestamps'].append(timestamp)
                
                # Check for alert
                if metric['threshold'] is not None and metric['alert_condition'] is not None:
                    threshold = metric['threshold']
                    condition = metric['alert_condition']
                    
                    alert_triggered = False
                    
                    if condition == 'above' and value > threshold:
                        alert_triggered = True
                    elif condition == 'below' and value < threshold:
                        alert_triggered = True
                    elif condition == 'equal' and value == threshold:
                        alert_triggered = True
                    
                    if alert_triggered:
                        alert = {
                            'timestamp': timestamp,
                            'metric': name,
                            'value': value,
                            'threshold': threshold,
                            'condition': condition
                        }
                        
                        self.alerts.append(alert)
                        self.logger.warning(f"Alert triggered for metric '{name}': {value} {condition} {threshold}")
                        
                        # Call alert callbacks
                        for callback in self.alert_callbacks:
                            try:
                                callback(alert)
                            except Exception as e:
                                self.logger.error(f"Error in alert callback: {str(e)}")
            
            except Exception as e:
                self.logger.error(f"Error calculating metric '{name}': {str(e)}")
    
    def _check_alerts(self) -> None:
        """
        Check for alerts.
        """
        # This method can be extended to implement more complex alert logic
        pass
    
    def _convert_to_serializable(self, obj: Any) -> Any:
        """
        Convert an object to a JSON-serializable format.
        
        Args:
            obj: Object to convert.
            
        Returns:
            JSON-serializable object.
        """
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, (list, tuple)):
            return [self._convert_to_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {str(k): self._convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (pd.DataFrame, pd.Series)):
            return obj.to_dict()
        elif hasattr(obj, 'tolist'):
            return obj.tolist()
        else:
            return str(obj)
