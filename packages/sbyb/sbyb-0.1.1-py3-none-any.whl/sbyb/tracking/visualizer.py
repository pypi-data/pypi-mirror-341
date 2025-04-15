"""
Tracking visualizer for SBYB.

This module provides the TrackingVisualizer class, which generates visualizations
for experiment tracking data to help users understand and compare their experiments.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import datetime
import uuid
from pathlib import Path
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import TrackingError
from sbyb.tracking.experiment import Experiment
from sbyb.tracking.run import Run
from sbyb.tracking.storage import LocalStorage


class TrackingVisualizer(SBYBComponent):
    """
    Visualizer for experiment tracking data.
    
    This component provides functionality for generating visualizations
    of experiment tracking data to help users understand and compare
    their experiments.
    """
    
    def __init__(self, storage: Optional[LocalStorage] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the tracking visualizer.
        
        Args:
            storage: Optional LocalStorage instance. If None, a new instance is created.
            config: Optional configuration dictionary.
        """
        super().__init__(config)
        
        # Set up logging
        self.logger = logging.getLogger("sbyb.tracking.visualizer")
        
        # Initialize storage
        self.storage = storage or LocalStorage(config=config)
        
        # Set default style for matplotlib
        plt.style.use('seaborn-v0_8-whitegrid')
    
    def plot_metric_history(self, run_id: str, metric: str, 
                           figsize: Tuple[int, int] = (10, 6),
                           title: Optional[str] = None,
                           use_plotly: bool = False) -> Union[Figure, go.Figure]:
        """
        Plot the history of a metric for a run.
        
        Args:
            run_id: ID of the run.
            metric: Name of the metric to plot.
            figsize: Figure size (width, height) in inches.
            title: Optional title for the plot.
            use_plotly: Whether to use Plotly instead of Matplotlib.
            
        Returns:
            Matplotlib Figure or Plotly Figure object.
            
        Raises:
            TrackingError: If the run is not found or the metric has no history.
        """
        run = self.storage.load_run(run_id)
        
        if metric not in run.history:
            raise TrackingError(f"Metric {metric} has no history for run {run_id}")
        
        history = run.history[metric]
        steps = [entry["step"] for entry in history]
        values = [entry["value"] for entry in history]
        
        if use_plotly:
            fig = px.line(
                x=steps,
                y=values,
                labels={"x": "Step", "y": metric},
                title=title or f"{metric} History for {run.name}"
            )
            fig.update_layout(
                xaxis_title="Step",
                yaxis_title=metric,
                template="plotly_white"
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=figsize)
            ax.plot(steps, values, marker='o', linestyle='-', markersize=4)
            ax.set_xlabel("Step")
            ax.set_ylabel(metric)
            ax.set_title(title or f"{metric} History for {run.name}")
            ax.grid(True)
            return fig
    
    def plot_metric_comparison(self, run_ids: List[str], metric: str,
                              figsize: Tuple[int, int] = (12, 6),
                              title: Optional[str] = None,
                              use_plotly: bool = False) -> Union[Figure, go.Figure]:
        """
        Compare a metric across multiple runs.
        
        Args:
            run_ids: List of run IDs to compare.
            metric: Name of the metric to compare.
            figsize: Figure size (width, height) in inches.
            title: Optional title for the plot.
            use_plotly: Whether to use Plotly instead of Matplotlib.
            
        Returns:
            Matplotlib Figure or Plotly Figure object.
            
        Raises:
            TrackingError: If any of the runs are not found or the metric is not found.
        """
        runs = []
        for run_id in run_ids:
            try:
                run = self.storage.load_run(run_id)
                runs.append(run)
            except TrackingError:
                self.logger.warning(f"Run not found: {run_id}")
        
        if not runs:
            raise TrackingError("No valid runs found")
        
        # Check if the metric exists in any run
        if not any(metric in run.metrics for run in runs):
            raise TrackingError(f"Metric {metric} not found in any run")
        
        # Create data for plotting
        run_names = []
        metric_values = []
        
        for run in runs:
            run_names.append(run.name)
            metric_values.append(run.metrics.get(metric, np.nan))
        
        if use_plotly:
            fig = px.bar(
                x=run_names,
                y=metric_values,
                labels={"x": "Run", "y": metric},
                title=title or f"{metric} Comparison"
            )
            fig.update_layout(
                xaxis_title="Run",
                yaxis_title=metric,
                template="plotly_white"
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=figsize)
            bars = ax.bar(run_names, metric_values)
            
            # Add value labels on top of bars
            for bar, value in zip(bars, metric_values):
                if not np.isnan(value):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                           f'{value:.4f}', ha='center', va='bottom', rotation=0)
            
            ax.set_xlabel("Run")
            ax.set_ylabel(metric)
            ax.set_title(title or f"{metric} Comparison")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            return fig
    
    def plot_metric_correlation(self, experiment_id: str, metrics: List[str],
                               figsize: Tuple[int, int] = (10, 8),
                               title: Optional[str] = None,
                               use_plotly: bool = False) -> Union[Figure, go.Figure]:
        """
        Plot correlation between metrics across runs in an experiment.
        
        Args:
            experiment_id: ID of the experiment.
            metrics: List of metrics to correlate.
            figsize: Figure size (width, height) in inches.
            title: Optional title for the plot.
            use_plotly: Whether to use Plotly instead of Matplotlib.
            
        Returns:
            Matplotlib Figure or Plotly Figure object.
            
        Raises:
            TrackingError: If the experiment is not found or has no runs.
        """
        experiment = self.storage.load_experiment(experiment_id)
        
        if not experiment.runs:
            raise TrackingError(f"Experiment {experiment_id} has no runs")
        
        # Create a DataFrame with metrics from all runs
        data = []
        for run in experiment.runs:
            run_data = {"run_id": run.run_id, "run_name": run.name}
            for metric in metrics:
                run_data[metric] = run.metrics.get(metric, np.nan)
            data.append(run_data)
        
        df = pd.DataFrame(data)
        
        # Check if we have enough data
        if len(df) < 2:
            raise TrackingError("Need at least 2 runs for correlation analysis")
        
        # Calculate correlation matrix
        corr_matrix = df[metrics].corr()
        
        if use_plotly:
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                title=title or f"Metric Correlation for {experiment.name}"
            )
            fig.update_layout(
                template="plotly_white"
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=figsize)
            mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
            cmap = sns.diverging_palette(230, 20, as_cmap=True)
            
            sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                       square=True, linewidths=.5, annot=True, fmt=".2f", ax=ax)
            
            ax.set_title(title or f"Metric Correlation for {experiment.name}")
            plt.tight_layout()
            return fig
    
    def plot_parameter_importance(self, experiment_id: str, metric: str,
                                 figsize: Tuple[int, int] = (12, 8),
                                 title: Optional[str] = None,
                                 use_plotly: bool = False) -> Union[Figure, go.Figure]:
        """
        Plot parameter importance for a metric across runs in an experiment.
        
        Args:
            experiment_id: ID of the experiment.
            metric: Metric to analyze.
            figsize: Figure size (width, height) in inches.
            title: Optional title for the plot.
            use_plotly: Whether to use Plotly instead of Matplotlib.
            
        Returns:
            Matplotlib Figure or Plotly Figure object.
            
        Raises:
            TrackingError: If the experiment is not found or has no runs.
        """
        experiment = self.storage.load_experiment(experiment_id)
        
        if not experiment.runs:
            raise TrackingError(f"Experiment {experiment_id} has no runs")
        
        # Create a DataFrame with parameters and the metric from all runs
        data = []
        for run in experiment.runs:
            if metric in run.metrics:
                run_data = {"run_id": run.run_id, "run_name": run.name, metric: run.metrics[metric]}
                for param_name, param_value in run.parameters.items():
                    # Only include numeric or boolean parameters
                    if isinstance(param_value, (int, float, bool)):
                        run_data[param_name] = param_value
                data.append(run_data)
        
        df = pd.DataFrame(data)
        
        # Check if we have enough data
        if len(df) < 3:
            raise TrackingError("Need at least 3 runs for parameter importance analysis")
        
        # Get parameter columns
        param_cols = [col for col in df.columns if col not in ["run_id", "run_name", metric]]
        
        if not param_cols:
            raise TrackingError("No numeric parameters found in runs")
        
        # Calculate correlation between parameters and the metric
        correlations = []
        for param in param_cols:
            if df[param].nunique() > 1:  # Only include parameters with variation
                corr = df[[param, metric]].corr().iloc[0, 1]
                correlations.append((param, abs(corr), corr))
        
        if not correlations:
            raise TrackingError("No parameters with variation found")
        
        # Sort by absolute correlation
        correlations.sort(key=lambda x: x[1], reverse=True)
        
        # Extract data for plotting
        params = [c[0] for c in correlations]
        abs_corrs = [c[1] for c in correlations]
        corrs = [c[2] for c in correlations]
        
        if use_plotly:
            fig = px.bar(
                x=params,
                y=abs_corrs,
                color=corrs,
                color_continuous_scale='RdBu_r',
                labels={"x": "Parameter", "y": f"Correlation with {metric} (absolute)"},
                title=title or f"Parameter Importance for {metric}"
            )
            fig.update_layout(
                xaxis_title="Parameter",
                yaxis_title=f"Correlation with {metric} (absolute)",
                template="plotly_white"
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=figsize)
            bars = ax.bar(params, abs_corrs, color=plt.cm.RdBu_r(np.array(corrs) * 0.5 + 0.5))
            
            # Add value labels on top of bars
            for bar, value in zip(bars, corrs):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{value:.2f}', ha='center', va='bottom', rotation=0)
            
            ax.set_xlabel("Parameter")
            ax.set_ylabel(f"Correlation with {metric} (absolute)")
            ax.set_title(title or f"Parameter Importance for {metric}")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            return fig
    
    def plot_parallel_coordinates(self, experiment_id: str, params: List[str], metrics: List[str],
                                 figsize: Tuple[int, int] = (14, 8),
                                 title: Optional[str] = None) -> go.Figure:
        """
        Create a parallel coordinates plot for parameters and metrics.
        
        Args:
            experiment_id: ID of the experiment.
            params: List of parameters to include.
            metrics: List of metrics to include.
            figsize: Figure size (width, height) in inches.
            title: Optional title for the plot.
            
        Returns:
            Plotly Figure object.
            
        Raises:
            TrackingError: If the experiment is not found or has no runs.
        """
        experiment = self.storage.load_experiment(experiment_id)
        
        if not experiment.runs:
            raise TrackingError(f"Experiment {experiment_id} has no runs")
        
        # Create a DataFrame with parameters and metrics from all runs
        data = []
        for run in experiment.runs:
            run_data = {"run_id": run.run_id, "run_name": run.name}
            
            # Add parameters
            for param in params:
                run_data[f"param_{param}"] = run.parameters.get(param, np.nan)
            
            # Add metrics
            for metric in metrics:
                run_data[f"metric_{metric}"] = run.metrics.get(metric, np.nan)
            
            data.append(run_data)
        
        df = pd.DataFrame(data)
        
        # Check if we have enough data
        if len(df) < 2:
            raise TrackingError("Need at least 2 runs for parallel coordinates plot")
        
        # Create dimensions for the plot
        dimensions = []
        
        # Add parameter dimensions
        for param in params:
            col = f"param_{param}"
            if col in df.columns and df[col].nunique() > 1:
                dimensions.append(
                    dict(
                        range=[df[col].min(), df[col].max()],
                        label=param,
                        values=df[col]
                    )
                )
        
        # Add metric dimensions
        for metric in metrics:
            col = f"metric_{metric}"
            if col in df.columns and df[col].nunique() > 1:
                dimensions.append(
                    dict(
                        range=[df[col].min(), df[col].max()],
                        label=metric,
                        values=df[col]
                    )
                )
        
        if not dimensions:
            raise TrackingError("No valid dimensions found for parallel coordinates plot")
        
        # Create the plot
        fig = go.Figure(data=
            go.Parcoords(
                line=dict(color=df.index, colorscale='Viridis', showscale=True),
                dimensions=dimensions
            )
        )
        
        fig.update_layout(
            title=title or f"Parallel Coordinates for {experiment.name}",
            width=figsize[0] * 100,
            height=figsize[1] * 100,
            template="plotly_white"
        )
        
        return fig
    
    def plot_run_status_distribution(self, experiment_id: Optional[str] = None,
                                    figsize: Tuple[int, int] = (10, 6),
                                    title: Optional[str] = None,
                                    use_plotly: bool = False) -> Union[Figure, go.Figure]:
        """
        Plot the distribution of run statuses.
        
        Args:
            experiment_id: Optional ID of the experiment to filter by.
            figsize: Figure size (width, height) in inches.
            title: Optional title for the plot.
            use_plotly: Whether to use Plotly instead of Matplotlib.
            
        Returns:
            Matplotlib Figure or Plotly Figure object.
        """
        # Get run data
        runs = self.storage.list_runs(experiment_id)
        
        if not runs:
            if experiment_id:
                raise TrackingError(f"Experiment {experiment_id} has no runs")
            else:
                raise TrackingError("No runs found")
        
        # Count statuses
        status_counts = {}
        for run in runs:
            status = run.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        statuses = list(status_counts.keys())
        counts = list(status_counts.values())
        
        if use_plotly:
            fig = px.pie(
                names=statuses,
                values=counts,
                title=title or "Run Status Distribution"
            )
            fig.update_layout(
                template="plotly_white"
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=figsize)
            ax.pie(counts, labels=statuses, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            ax.set_title(title or "Run Status Distribution")
            return fig
    
    def plot_metric_distribution(self, experiment_id: str, metric: str,
                               figsize: Tuple[int, int] = (10, 6),
                               title: Optional[str] = None,
                               use_plotly: bool = False) -> Union[Figure, go.Figure]:
        """
        Plot the distribution of a metric across runs in an experiment.
        
        Args:
            experiment_id: ID of the experiment.
            metric: Metric to analyze.
            figsize: Figure size (width, height) in inches.
            title: Optional title for the plot.
            use_plotly: Whether to use Plotly instead of Matplotlib.
            
        Returns:
            Matplotlib Figure or Plotly Figure object.
            
        Raises:
            TrackingError: If the experiment is not found or has no runs.
        """
        experiment = self.storage.load_experiment(experiment_id)
        
        if not experiment.runs:
            raise TrackingError(f"Experiment {experiment_id} has no runs")
        
        # Extract metric values
        values = []
        for run in experiment.runs:
            if metric in run.metrics:
                values.append(run.metrics[metric])
        
        if not values:
            raise TrackingError(f"Metric {metric} not found in any run")
        
        if use_plotly:
            fig = px.histogram(
                x=values,
                nbins=min(20, len(values)),
                labels={"x": metric},
                title=title or f"{metric} Distribution"
            )
            fig.update_layout(
                xaxis_title=metric,
                yaxis_title="Count",
                template="plotly_white"
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=figsize)
            ax.hist(values, bins=min(20, len(values)), alpha=0.7)
            ax.set_xlabel(metric)
            ax.set_ylabel("Count")
            ax.set_title(title or f"{metric} Distribution")
            return fig
    
    def plot_run_duration(self, experiment_id: Optional[str] = None,
                         figsize: Tuple[int, int] = (12, 6),
                         title: Optional[str] = None,
                         use_plotly: bool = False) -> Union[Figure, go.Figure]:
        """
        Plot the duration of runs.
        
        Args:
            experiment_id: Optional ID of the experiment to filter by.
            figsize: Figure size (width, height) in inches.
            title: Optional title for the plot.
            use_plotly: Whether to use Plotly instead of Matplotlib.
            
        Returns:
            Matplotlib Figure or Plotly Figure object.
        """
        # Get run data
        runs = self.storage.list_runs(experiment_id)
        
        if not runs:
            if experiment_id:
                raise TrackingError(f"Experiment {experiment_id} has no runs")
            else:
                raise TrackingError("No runs found")
        
        # Calculate durations
        run_names = []
        durations = []
        
        for run in runs:
            if run.get("started_at") and run.get("ended_at"):
                run_names.append(run.get("name", run.get("run_id")))
                
                started = datetime.datetime.fromisoformat(run["started_at"])
                ended = datetime.datetime.fromisoformat(run["ended_at"])
                duration = (ended - started).total_seconds() / 60.0  # Duration in minutes
                
                durations.append(duration)
        
        if not durations:
            raise TrackingError("No runs with valid duration information found")
        
        # Sort by duration
        sorted_indices = np.argsort(durations)
        sorted_names = [run_names[i] for i in sorted_indices]
        sorted_durations = [durations[i] for i in sorted_indices]
        
        if use_plotly:
            fig = px.bar(
                x=sorted_names,
                y=sorted_durations,
                labels={"x": "Run", "y": "Duration (minutes)"},
                title=title or "Run Duration"
            )
            fig.update_layout(
                xaxis_title="Run",
                yaxis_title="Duration (minutes)",
                template="plotly_white"
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=figsize)
            ax.bar(sorted_names, sorted_durations)
            ax.set_xlabel("Run")
            ax.set_ylabel("Duration (minutes)")
            ax.set_title(title or "Run Duration")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            return fig
    
    def create_experiment_dashboard(self, experiment_id: str, 
                                   metrics: List[str],
                                   params: Optional[List[str]] = None) -> go.Figure:
        """
        Create a comprehensive dashboard for an experiment.
        
        Args:
            experiment_id: ID of the experiment.
            metrics: List of metrics to include.
            params: Optional list of parameters to include.
            
        Returns:
            Plotly Figure object with multiple subplots.
            
        Raises:
            TrackingError: If the experiment is not found or has no runs.
        """
        experiment = self.storage.load_experiment(experiment_id)
        
        if not experiment.runs:
            raise TrackingError(f"Experiment {experiment_id} has no runs")
        
        # Create a subplot grid
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Metric Comparison",
                "Run Status Distribution",
                "Parameter Importance",
                "Run Duration"
            ),
            specs=[
                [{"type": "bar"}, {"type": "pie"}],
                [{"type": "bar"}, {"type": "bar"}]
            ]
        )
        
        # 1. Metric Comparison
        run_names = []
        metric_values = {metric: [] for metric in metrics}
        
        for run in experiment.runs:
            run_names.append(run.name)
            for metric in metrics:
                metric_values[metric].append(run.metrics.get(metric, np.nan))
        
        # Add traces for each metric
        for i, metric in enumerate(metrics):
            fig.add_trace(
                go.Bar(
                    x=run_names,
                    y=metric_values[metric],
                    name=metric
                ),
                row=1, col=1
            )
        
        # 2. Run Status Distribution
        status_counts = {}
        for run in experiment.runs:
            status = run.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        statuses = list(status_counts.keys())
        counts = list(status_counts.values())
        
        fig.add_trace(
            go.Pie(
                labels=statuses,
                values=counts,
                textinfo='percent+label'
            ),
            row=1, col=2
        )
        
        # 3. Parameter Importance (if parameters are provided)
        if params:
            # Get the first metric for parameter importance
            metric = metrics[0]
            
            # Create a DataFrame with parameters and the metric
            data = []
            for run in experiment.runs:
                if metric in run.metrics:
                    run_data = {"run_id": run.run_id, "run_name": run.name, metric: run.metrics[metric]}
                    for param_name in params:
                        param_value = run.parameters.get(param_name)
                        if isinstance(param_value, (int, float, bool)):
                            run_data[param_name] = param_value
                    data.append(run_data)
            
            df = pd.DataFrame(data)
            
            # Calculate correlation between parameters and the metric
            correlations = []
            for param in params:
                if param in df.columns and df[param].nunique() > 1:
                    corr = df[[param, metric]].corr().iloc[0, 1]
                    if not np.isnan(corr):
                        correlations.append((param, abs(corr), corr))
            
            if correlations:
                # Sort by absolute correlation
                correlations.sort(key=lambda x: x[1], reverse=True)
                
                # Extract data for plotting
                params_sorted = [c[0] for c in correlations]
                abs_corrs = [c[1] for c in correlations]
                
                fig.add_trace(
                    go.Bar(
                        x=params_sorted,
                        y=abs_corrs,
                        name="Parameter Importance"
                    ),
                    row=2, col=1
                )
        
        # 4. Run Duration
        run_names = []
        durations = []
        
        for run in experiment.runs:
            if run.started_at and run.ended_at:
                run_names.append(run.name)
                
                started = datetime.datetime.fromisoformat(run.started_at)
                ended = datetime.datetime.fromisoformat(run.ended_at)
                duration = (ended - started).total_seconds() / 60.0  # Duration in minutes
                
                durations.append(duration)
        
        if durations:
            # Sort by duration
            sorted_indices = np.argsort(durations)
            sorted_names = [run_names[i] for i in sorted_indices]
            sorted_durations = [durations[i] for i in sorted_indices]
            
            fig.add_trace(
                go.Bar(
                    x=sorted_names,
                    y=sorted_durations,
                    name="Duration (minutes)"
                ),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title_text=f"Dashboard for {experiment.name}",
            height=800,
            width=1200,
            template="plotly_white",
            showlegend=False
        )
        
        return fig
    
    def export_experiment_report(self, experiment_id: str, output_dir: str,
                               metrics: List[str], params: Optional[List[str]] = None) -> str:
        """
        Export a comprehensive HTML report for an experiment.
        
        Args:
            experiment_id: ID of the experiment.
            output_dir: Directory to save the report to.
            metrics: List of metrics to include.
            params: Optional list of parameters to include.
            
        Returns:
            Path to the generated HTML report.
            
        Raises:
            TrackingError: If the experiment is not found or has no runs.
        """
        experiment = self.storage.load_experiment(experiment_id)
        
        if not experiment.runs:
            raise TrackingError(f"Experiment {experiment_id} has no runs")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate plots
        plots = {}
        
        try:
            # Dashboard
            plots["dashboard"] = self.create_experiment_dashboard(
                experiment_id=experiment_id,
                metrics=metrics,
                params=params
            )
            
            # Metric comparison for each metric
            for metric in metrics:
                try:
                    plots[f"metric_{metric}"] = self.plot_metric_comparison(
                        run_ids=[run.run_id for run in experiment.runs],
                        metric=metric,
                        use_plotly=True
                    )
                except Exception as e:
                    self.logger.warning(f"Error generating metric comparison for {metric}: {str(e)}")
            
            # Parameter importance for each metric
            if params:
                for metric in metrics:
                    try:
                        plots[f"param_importance_{metric}"] = self.plot_parameter_importance(
                            experiment_id=experiment_id,
                            metric=metric,
                            use_plotly=True
                        )
                    except Exception as e:
                        self.logger.warning(f"Error generating parameter importance for {metric}: {str(e)}")
            
            # Parallel coordinates
            if params:
                try:
                    plots["parallel_coords"] = self.plot_parallel_coordinates(
                        experiment_id=experiment_id,
                        params=params,
                        metrics=metrics
                    )
                except Exception as e:
                    self.logger.warning(f"Error generating parallel coordinates plot: {str(e)}")
            
            # Run duration
            try:
                plots["run_duration"] = self.plot_run_duration(
                    experiment_id=experiment_id,
                    use_plotly=True
                )
            except Exception as e:
                self.logger.warning(f"Error generating run duration plot: {str(e)}")
            
            # Run status distribution
            try:
                plots["run_status"] = self.plot_run_status_distribution(
                    experiment_id=experiment_id,
                    use_plotly=True
                )
            except Exception as e:
                self.logger.warning(f"Error generating run status distribution plot: {str(e)}")
            
            # Generate HTML
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Experiment Report: {experiment.name}</title>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 20px;
                        box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    }}
                    h1, h2, h3 {{
                        color: #333;
                    }}
                    .plot {{
                        margin-bottom: 30px;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 20px;
                    }}
                    th, td {{
                        padding: 8px;
                        text-align: left;
                        border-bottom: 1px solid #ddd;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                    tr:hover {{
                        background-color: #f5f5f5;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Experiment Report: {experiment.name}</h1>
                    <p><strong>Description:</strong> {experiment.description}</p>
                    <p><strong>Created:</strong> {experiment.created_at}</p>
                    <p><strong>Tags:</strong> {', '.join(experiment.tags) if experiment.tags else 'None'}</p>
                    <p><strong>Number of Runs:</strong> {len(experiment.runs)}</p>
                    
                    <h2>Dashboard</h2>
                    <div class="plot" id="dashboard"></div>
                    
                    <h2>Metrics</h2>
            """
            
            # Add metric plots
            for metric in metrics:
                plot_id = f"metric_{metric}"
                if plot_id in plots:
                    html_content += f"""
                    <h3>{metric}</h3>
                    <div class="plot" id="{plot_id}"></div>
                    """
            
            # Add parameter importance plots
            if params:
                html_content += "<h2>Parameter Importance</h2>"
                for metric in metrics:
                    plot_id = f"param_importance_{metric}"
                    if plot_id in plots:
                        html_content += f"""
                        <h3>For {metric}</h3>
                        <div class="plot" id="{plot_id}"></div>
                        """
            
            # Add parallel coordinates plot
            if "parallel_coords" in plots:
                html_content += """
                <h2>Parameter-Metric Relationships</h2>
                <div class="plot" id="parallel_coords"></div>
                """
            
            # Add run duration and status plots
            html_content += """
            <h2>Run Information</h2>
            """
            
            if "run_duration" in plots:
                html_content += """
                <h3>Run Duration</h3>
                <div class="plot" id="run_duration"></div>
                """
            
            if "run_status" in plots:
                html_content += """
                <h3>Run Status Distribution</h3>
                <div class="plot" id="run_status"></div>
                """
            
            # Add run table
            html_content += """
            <h2>Run Details</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Duration</th>
            """
            
            for metric in metrics:
                html_content += f"<th>{metric}</th>"
            
            if params:
                for param in params:
                    html_content += f"<th>{param}</th>"
            
            html_content += "</tr>"
            
            for run in experiment.runs:
                duration = ""
                if run.started_at and run.ended_at:
                    started = datetime.datetime.fromisoformat(run.started_at)
                    ended = datetime.datetime.fromisoformat(run.ended_at)
                    duration_mins = (ended - started).total_seconds() / 60.0
                    duration = f"{duration_mins:.2f} min"
                
                html_content += f"""
                <tr>
                    <td>{run.name}</td>
                    <td>{run.status}</td>
                    <td>{run.created_at}</td>
                    <td>{duration}</td>
                """
                
                for metric in metrics:
                    value = run.metrics.get(metric, "")
                    html_content += f"<td>{value}</td>"
                
                if params:
                    for param in params:
                        value = run.parameters.get(param, "")
                        html_content += f"<td>{value}</td>"
                
                html_content += "</tr>"
            
            html_content += """
                </table>
                </div>
            """
            
            # Add plot scripts
            html_content += "<script>"
            for plot_id, plot in plots.items():
                plot_json = plot.to_json()
                html_content += f"""
                Plotly.newPlot('{plot_id}', {plot_json});
                """
            html_content += "</script>"
            
            html_content += """
            </body>
            </html>
            """
            
            # Write HTML to file
            report_path = os.path.join(output_dir, f"experiment_{experiment_id}_report.html")
            with open(report_path, "w") as f:
                f.write(html_content)
            
            return report_path
        
        except Exception as e:
            raise TrackingError(f"Error generating experiment report: {str(e)}")
