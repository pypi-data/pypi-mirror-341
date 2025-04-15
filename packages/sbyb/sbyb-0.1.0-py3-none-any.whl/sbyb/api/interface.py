"""
Main API interface for SBYB.

This module provides the main programmatic interface for the SBYB library,
allowing users to interact with all components through a unified API.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import logging
import pandas as pd
import numpy as np
import datetime

from sbyb.core.config import Config
from sbyb.preprocessing import PreprocessingPipeline
from sbyb.task_detection import TaskDetector
from sbyb.automl import AutoMLEngine
from sbyb.evaluation import Evaluator, Explainer
from sbyb.deployment import ModelExporter, ModelServer
from sbyb.ui_generator import DashboardGenerator, FormGenerator
from sbyb.scaffolding import ProjectGenerator
from sbyb.eda import DataProfiler, Visualizer, DataAnalyzer
from sbyb.plugins import PluginManager
from sbyb.tracking import ExperimentTracker, Run, Experiment, TrackingVisualizer


class SBYB:
    """
    Main interface for the SBYB library.
    
    This class provides a unified API for interacting with all components
    of the SBYB library, making it easy to use the library programmatically.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the SBYB API.
        
        Args:
            config: Optional configuration dictionary.
        """
        self.config = config or {}
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('sbyb.api')
        
        # Initialize components
        self._init_components()
    
    def _init_components(self):
        """
        Initialize all components of the SBYB library.
        """
        # Core components
        self.preprocessing = PreprocessingPipeline(self.config.get('preprocessing'))
        self.task_detector = TaskDetector(self.config.get('task_detection'))
        self.automl = AutoMLEngine(self.config.get('automl'))
        self.evaluator = Evaluator(self.config.get('evaluation'))
        self.explainer = Explainer(self.config.get('explainer'))
        self.model_exporter = ModelExporter(self.config.get('model_exporter'))
        self.model_server = ModelServer(self.config.get('model_server'))
        self.dashboard_generator = DashboardGenerator(self.config.get('dashboard_generator'))
        self.form_generator = FormGenerator(self.config.get('form_generator'))
        self.project_generator = ProjectGenerator(self.config.get('project_generator'))
        self.data_profiler = DataProfiler(self.config.get('data_profiler'))
        self.visualizer = Visualizer(self.config.get('visualizer'))
        self.data_analyzer = DataAnalyzer(self.config.get('data_analyzer'))
        self.plugin_manager = PluginManager(self.config.get('plugin_manager'))
        self.experiment_tracker = ExperimentTracker(self.config.get('experiment_tracker'))
        self.tracking_visualizer = TrackingVisualizer(self.config.get('tracking_visualizer'))
    
    #
    # Project Management
    #
    
    def create_project(self, name: str, template: str = 'basic', output_dir: str = '.',
                      description: Optional[str] = None) -> str:
        """
        Create a new project.
        
        Args:
            name: Project name.
            template: Project template. Options: 'basic', 'classification', 'regression', 'time_series'.
            output_dir: Output directory.
            description: Optional project description.
            
        Returns:
            Path to the created project.
        """
        self.logger.info(f"Creating new project: {name}")
        
        output_dir = os.path.abspath(output_dir)
        project_dir = os.path.join(output_dir, name)
        
        self.project_generator.create_project(
            name=name,
            template=template,
            output_dir=output_dir,
            description=description or f"{name} - A SBYB project"
        )
        
        self.logger.info(f"Project created successfully: {project_dir}")
        return project_dir
    
    #
    # Data Preprocessing
    #
    
    def preprocess_data(self, data: Union[pd.DataFrame, str], config: Optional[Dict[str, Any]] = None,
                       output_file: Optional[str] = None, save_pipeline: Optional[str] = None) -> pd.DataFrame:
        """
        Preprocess data.
        
        Args:
            data: Input data as DataFrame or path to data file.
            config: Optional preprocessing configuration.
            output_file: Optional path to save preprocessed data.
            save_pipeline: Optional path to save preprocessing pipeline.
            
        Returns:
            Preprocessed data as DataFrame.
        """
        self.logger.info("Preprocessing data")
        
        # Load data if it's a file path
        if isinstance(data, str):
            if data.endswith('.csv'):
                data = pd.read_csv(data)
            elif data.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(data)
            elif data.endswith('.parquet'):
                data = pd.read_parquet(data)
            elif data.endswith('.json'):
                data = pd.read_json(data)
            else:
                raise ValueError(f"Unsupported data file format: {data}")
        
        # Update pipeline config if provided
        if config:
            self.preprocessing.update_config(config)
        
        # Preprocess data
        preprocessed_data = self.preprocessing.fit_transform(data)
        
        # Save preprocessed data
        if output_file:
            if output_file.endswith('.csv'):
                preprocessed_data.to_csv(output_file, index=False)
            elif output_file.endswith(('.xls', '.xlsx')):
                preprocessed_data.to_excel(output_file, index=False)
            elif output_file.endswith('.parquet'):
                preprocessed_data.to_parquet(output_file, index=False)
            else:
                preprocessed_data.to_csv(output_file, index=False)
            
            self.logger.info(f"Preprocessed data saved to: {output_file}")
        
        # Save pipeline
        if save_pipeline:
            self.preprocessing.save(save_pipeline)
            self.logger.info(f"Preprocessing pipeline saved to: {save_pipeline}")
        
        self.logger.info("Data preprocessing completed successfully")
        return preprocessed_data
    
    def profile_data(self, data: Union[pd.DataFrame, str], output_dir: Optional[str] = None,
                    format: str = 'html') -> Any:
        """
        Generate a data profile.
        
        Args:
            data: Input data as DataFrame or path to data file.
            output_dir: Optional directory to save profile report.
            format: Output format. Options: 'html', 'json'.
            
        Returns:
            Data profile object.
        """
        self.logger.info("Generating data profile")
        
        # Load data if it's a file path
        if isinstance(data, str):
            if data.endswith('.csv'):
                data = pd.read_csv(data)
            elif data.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(data)
            elif data.endswith('.parquet'):
                data = pd.read_parquet(data)
            elif data.endswith('.json'):
                data = pd.read_json(data)
            else:
                raise ValueError(f"Unsupported data file format: {data}")
        
        # Generate profile
        profile = self.data_profiler.generate_profile(data)
        
        # Save profile
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
            if format == 'html':
                output_file = os.path.join(output_dir, 'data_profile.html')
                profile.to_html(output_file)
            elif format == 'json':
                output_file = os.path.join(output_dir, 'data_profile.json')
                profile.to_json(output_file)
            
            self.logger.info(f"Data profile saved to: {output_file}")
        
        self.logger.info("Data profiling completed successfully")
        return profile
    
    #
    # AutoML
    #
    
    def run_automl(self, data: Union[pd.DataFrame, str], target: str, task: Optional[str] = None,
                  config: Optional[Dict[str, Any]] = None, output_dir: Optional[str] = None,
                  time_limit: Optional[int] = None, track: bool = False,
                  experiment_name: Optional[str] = None) -> Any:
        """
        Run AutoML.
        
        Args:
            data: Input data as DataFrame or path to data file.
            target: Target column name.
            task: Optional ML task type (auto-detected if not specified).
            config: Optional AutoML configuration.
            output_dir: Optional directory to save results.
            time_limit: Optional time limit in seconds.
            track: Whether to track the experiment.
            experiment_name: Optional experiment name for tracking.
            
        Returns:
            AutoML result object.
        """
        self.logger.info("Running AutoML")
        
        # Load data if it's a file path
        if isinstance(data, str):
            if data.endswith('.csv'):
                data = pd.read_csv(data)
            elif data.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(data)
            elif data.endswith('.parquet'):
                data = pd.read_parquet(data)
            elif data.endswith('.json'):
                data = pd.read_json(data)
            else:
                raise ValueError(f"Unsupported data file format: {data}")
        
        # Split features and target
        if target not in data.columns:
            raise ValueError(f"Target column not found: {target}")
        
        X = data.drop(columns=[target])
        y = data[target]
        
        # Update AutoML config if provided
        if config:
            self.automl.update_config(config)
        
        # Set time limit if specified
        if time_limit:
            self.automl.config['time_limit'] = time_limit
        
        # Create experiment tracker if tracking is enabled
        tracker = None
        if track:
            tracker = self.experiment_tracker
            
            # Create or set experiment
            if experiment_name:
                try:
                    # Try to find existing experiment
                    experiments = tracker.list_experiments()
                    experiment_id = None
                    
                    for exp in experiments:
                        if exp['name'] == experiment_name:
                            experiment_id = exp['experiment_id']
                            break
                    
                    if experiment_id:
                        tracker.set_experiment(experiment_id)
                        self.logger.info(f"Using existing experiment: {experiment_name}")
                    else:
                        tracker.create_experiment(name=experiment_name)
                        self.logger.info(f"Created new experiment: {experiment_name}")
                except Exception as e:
                    self.logger.warning(f"Error setting experiment: {str(e)}")
                    tracker.create_experiment(name=f"AutoML Run {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
            else:
                tracker.create_experiment(name=f"AutoML Run {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # Create run
            run = tracker.create_run(name=f"AutoML Run {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
            tracker.start_run()
            
            # Log parameters
            tracker.log_parameters({
                'target_column': target,
                'n_samples': len(data),
                'n_features': len(X.columns),
                'time_limit': time_limit
            })
        
        try:
            # Detect task type if not specified
            task_type = task
            if not task_type:
                self.logger.info("Auto-detecting task type...")
                task_type = self.task_detector.detect(X, y)
                self.logger.info(f"Detected task type: {task_type}")
                
                if tracker:
                    tracker.log_parameter('task_type', task_type)
            
            # Set task type
            self.automl.set_task(task_type)
            
            # Run AutoML
            self.logger.info("Running AutoML...")
            result = self.automl.fit(X, y)
            
            # Log metrics if tracking
            if tracker:
                tracker.log_metrics(result.metrics)
                
                # Log model
                if output_dir:
                    model_path = os.path.join(output_dir, 'model.pkl')
                    os.makedirs(output_dir, exist_ok=True)
                    result.save_model(model_path)
                    tracker.log_model(result.model, model_path)
                
                # End run
                tracker.end_run()
            
            # Save results
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                
                # Save model
                model_path = os.path.join(output_dir, 'model.pkl')
                result.save_model(model_path)
                self.logger.info(f"Model saved to: {model_path}")
                
                # Save leaderboard
                leaderboard_path = os.path.join(output_dir, 'leaderboard.csv')
                result.leaderboard.to_csv(leaderboard_path, index=False)
                self.logger.info(f"Leaderboard saved to: {leaderboard_path}")
                
                # Save feature importance
                if hasattr(result, 'feature_importance') and result.feature_importance is not None:
                    fi_path = os.path.join(output_dir, 'feature_importance.csv')
                    result.feature_importance.to_csv(fi_path, index=False)
                    self.logger.info(f"Feature importance saved to: {fi_path}")
                
                # Save predictions
                preds_path = os.path.join(output_dir, 'predictions.csv')
                result.predictions.to_csv(preds_path, index=False)
                self.logger.info(f"Predictions saved to: {preds_path}")
            
            self.logger.info("AutoML completed successfully")
            return result
        
        except Exception as e:
            self.logger.error(f"Error running AutoML: {str(e)}")
            
            # End run with failure if tracking
            if tracker and tracker.current_run:
                tracker.end_run(status="failed", error_message=str(e))
            
            raise
    
    #
    # Evaluation
    #
    
    def evaluate_model(self, model: Any, data: Union[pd.DataFrame, str], target: str,
                      metrics: Optional[List[str]] = None, output_dir: Optional[str] = None) -> Any:
        """
        Evaluate a model.
        
        Args:
            model: Model object or path to model file.
            data: Test data as DataFrame or path to data file.
            target: Target column name.
            metrics: Optional list of metrics to compute.
            output_dir: Optional directory to save evaluation results.
            
        Returns:
            Evaluation result object.
        """
        self.logger.info("Evaluating model")
        
        # Load model if it's a file path
        if isinstance(model, str):
            import pickle
            with open(model, 'rb') as f:
                model = pickle.load(f)
        
        # Load data if it's a file path
        if isinstance(data, str):
            if data.endswith('.csv'):
                data = pd.read_csv(data)
            elif data.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(data)
            elif data.endswith('.parquet'):
                data = pd.read_parquet(data)
            elif data.endswith('.json'):
                data = pd.read_json(data)
            else:
                raise ValueError(f"Unsupported data file format: {data}")
        
        # Split features and target
        if target not in data.columns:
            raise ValueError(f"Target column not found: {target}")
        
        X = data.drop(columns=[target])
        y = data[target]
        
        # Evaluate model
        evaluation = self.evaluator.evaluate(model, X, y, metrics=metrics)
        
        # Save results
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
            # Save metrics
            metrics_path = os.path.join(output_dir, 'metrics.json')
            import json
            with open(metrics_path, 'w') as f:
                json.dump(evaluation.metrics, f, indent=2)
            self.logger.info(f"Metrics saved to: {metrics_path}")
            
            # Save confusion matrix if available
            if hasattr(evaluation, 'confusion_matrix') and evaluation.confusion_matrix is not None:
                cm_path = os.path.join(output_dir, 'confusion_matrix.csv')
                evaluation.confusion_matrix.to_csv(cm_path, index=False)
                self.logger.info(f"Confusion matrix saved to: {cm_path}")
            
            # Save ROC curve if available
            if hasattr(evaluation, 'roc_curve') and evaluation.roc_curve is not None:
                roc_path = os.path.join(output_dir, 'roc_curve.png')
                evaluation.roc_curve.savefig(roc_path)
                self.logger.info(f"ROC curve saved to: {roc_path}")
            
            # Save predictions
            preds_path = os.path.join(output_dir, 'predictions.csv')
            evaluation.predictions.to_csv(preds_path, index=False)
            self.logger.info(f"Predictions saved to: {preds_path}")
        
        self.logger.info("Evaluation completed successfully")
        return evaluation
    
    def explain_model(self, model: Any, data: Union[pd.DataFrame, str], method: str = 'shap',
                     output_dir: Optional[str] = None) -> Any:
        """
        Explain a model.
        
        Args:
            model: Model object or path to model file.
            data: Data as DataFrame or path to data file.
            method: Explanation method. Options: 'shap', 'lime', 'eli5', 'all'.
            output_dir: Optional directory to save explanation results.
            
        Returns:
            Explanation result object.
        """
        self.logger.info(f"Explaining model using {method}")
        
        # Load model if it's a file path
        if isinstance(model, str):
            import pickle
            with open(model, 'rb') as f:
                model = pickle.load(f)
        
        # Load data if it's a file path
        if isinstance(data, str):
            if data.endswith('.csv'):
                data = pd.read_csv(data)
            elif data.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(data)
            elif data.endswith('.parquet'):
                data = pd.read_parquet(data)
            elif data.endswith('.json'):
                data = pd.read_json(data)
            else:
                raise ValueError(f"Unsupported data file format: {data}")
        
        # Generate explanations
        explanation = self.explainer.explain(model, data, method=method)
        
        # Save results
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
            # Save feature importance
            if hasattr(explanation, 'feature_importance') and explanation.feature_importance is not None:
                fi_path = os.path.join(output_dir, 'feature_importance.csv')
                explanation.feature_importance.to_csv(fi_path, index=False)
                self.logger.info(f"Feature importance saved to: {fi_path}")
            
            # Save SHAP values if available
            if hasattr(explanation, 'shap_values') and explanation.shap_values is not None:
                shap_path = os.path.join(output_dir, 'shap_values.csv')
                pd.DataFrame(explanation.shap_values).to_csv(shap_path, index=False)
                self.logger.info(f"SHAP values saved to: {shap_path}")
            
            # Save SHAP summary plot if available
            if hasattr(explanation, 'shap_summary_plot') and explanation.shap_summary_plot is not None:
                shap_plot_path = os.path.join(output_dir, 'shap_summary.png')
                explanation.shap_summary_plot.savefig(shap_plot_path)
                self.logger.info(f"SHAP summary plot saved to: {shap_plot_path}")
            
            # Save explanation report
            report_path = os.path.join(output_dir, 'explanation_report.html')
            explanation.to_html(report_path)
            self.logger.info(f"Explanation report saved to: {report_path}")
        
        self.logger.info("Explanation completed successfully")
        return explanation
    
    #
    # Deployment
    #
    
    def export_model(self, model: Any, format: str = 'pickle', output: Optional[str] = None) -> str:
        """
        Export a model.
        
        Args:
            model: Model object or path to model file.
            format: Export format. Options: 'pickle', 'onnx', 'tensorflow', 'mlflow'.
            output: Optional output file or directory.
            
        Returns:
            Path to the exported model.
        """
        self.logger.info(f"Exporting model to {format} format")
        
        # Load model if it's a file path
        if isinstance(model, str):
            import pickle
            with open(model, 'rb') as f:
                model = pickle.load(f)
        
        # Export model
        if format == 'pickle':
            output_file = output or 'model_exported.pkl'
            path = self.model_exporter.to_pickle(model, output_file)
        elif format == 'onnx':
            output_file = output or 'model.onnx'
            path = self.model_exporter.to_onnx(model, output_file)
        elif format == 'tensorflow':
            output_dir = output or 'model_tf'
            path = self.model_exporter.to_tensorflow(model, output_dir)
        elif format == 'mlflow':
            output_dir = output or 'model_mlflow'
            path = self.model_exporter.to_mlflow(model, output_dir)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        self.logger.info(f"Model exported to: {path}")
        return path
    
    def serve_model(self, model: Any, host: str = '0.0.0.0', port: int = 8000,
                   server_type: str = 'fastapi') -> Any:
        """
        Serve a model.
        
        Args:
            model: Model object or path to model file.
            host: Host to bind to.
            port: Port to bind to.
            server_type: Server type. Options: 'fastapi', 'flask', 'streamlit'.
            
        Returns:
            Server object.
        """
        self.logger.info(f"Serving model with {server_type} server on {host}:{port}")
        
        # Load model if it's a file path
        if isinstance(model, str):
            import pickle
            with open(model, 'rb') as f:
                model = pickle.load(f)
        
        # Set server type
        self.model_server.set_server_type(server_type)
        
        # Serve model
        server = self.model_server.serve(model, host=host, port=port, start=False)
        
        self.logger.info(f"Model server created. Call start() on the returned object to start the server.")
        return server
    
    #
    # UI Generation
    #
    
    def generate_ui(self, model: Any, output_dir: str, ui_type: str = 'dashboard',
                   framework: str = 'streamlit', theme: Optional[str] = None) -> str:
        """
        Generate a UI.
        
        Args:
            model: Model object or path to model file.
            output_dir: Output directory.
            ui_type: UI type. Options: 'dashboard', 'form', 'app'.
            framework: UI framework. Options: 'streamlit', 'dash', 'flask', 'html'.
            theme: Optional UI theme.
            
        Returns:
            Path to the generated UI.
        """
        self.logger.info(f"Generating {ui_type} UI with {framework} framework")
        
        # Load model if it's a file path
        if isinstance(model, str):
            import pickle
            with open(model, 'rb') as f:
                model = pickle.load(f)
        
        # Create UI generator
        if ui_type == 'dashboard':
            generator = self.dashboard_generator
            generator.set_framework(framework)
        elif ui_type == 'form':
            generator = self.form_generator
            generator.set_framework(framework)
        else:  # app
            if framework == 'streamlit':
                from sbyb.ui_generator import StreamlitAppGenerator
                generator = StreamlitAppGenerator()
            elif framework == 'dash':
                from sbyb.ui_generator import DashAppGenerator
                generator = DashAppGenerator()
            elif framework == 'flask':
                from sbyb.ui_generator import FlaskAppGenerator
                generator = FlaskAppGenerator()
            else:  # html
                from sbyb.ui_generator import HTMLAppGenerator
                generator = HTMLAppGenerator()
        
        # Set theme if specified
        if theme:
            generator.set_theme(theme)
        
        # Generate UI
        ui_path = generator.generate(model, output_dir=output_dir)
        
        self.logger.info(f"UI generated successfully: {ui_path}")
        return ui_path
    
    #
    # Plugin Management
    #
    
    def list_plugins(self, category: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        List installed plugins.
        
        Args:
            category: Optional category to filter by.
            
        Returns:
            Dictionary of plugin categories and their available plugins with metadata.
        """
        self.logger.info("Listing installed plugins")
        return self.plugin_manager.list_plugins(category=category)
    
    def install_plugin(self, source: str, force: bool = False) -> bool:
        """
        Install a plugin.
        
        Args:
            source: Plugin source (local path, git URL, or pip package).
            force: Whether to force installation if the plugin already exists.
            
        Returns:
            True if the plugin was installed successfully, False otherwise.
        """
        self.logger.info(f"Installing plugin from: {source}")
        return self.plugin_manager.install_plugin(source, force=force)
    
    def uninstall_plugin(self, name: str, category: Optional[str] = None) -> bool:
        """
        Uninstall a plugin.
        
        Args:
            name: Plugin name.
            category: Optional plugin category.
            
        Returns:
            True if the plugin was uninstalled successfully, False otherwise.
        """
        self.logger.info(f"Uninstalling plugin: {name}")
        return self.plugin_manager.uninstall_plugin(name, category=category)
    
    def create_plugin_template(self, name: str, output_dir: str = '.', category: str = 'custom',
                              description: Optional[str] = None, author: Optional[str] = None) -> bool:
        """
        Create a plugin template.
        
        Args:
            name: Plugin name.
            output_dir: Output directory.
            category: Plugin category.
            description: Optional plugin description.
            author: Optional plugin author.
            
        Returns:
            True if the template was created successfully, False otherwise.
        """
        self.logger.info(f"Creating plugin template: {name}")
        return self.plugin_manager.create_plugin_template(
            output_dir=output_dir,
            name=name,
            category=category,
            description=description or f"{name} plugin",
            author=author or "SBYB User"
        )
    
    #
    # Experiment Tracking
    #
    
    def create_experiment(self, name: str, description: Optional[str] = None,
                         tags: Optional[List[str]] = None) -> Experiment:
        """
        Create a new experiment.
        
        Args:
            name: Experiment name.
            description: Optional experiment description.
            tags: Optional list of tags.
            
        Returns:
            Created Experiment object.
        """
        self.logger.info(f"Creating experiment: {name}")
        return self.experiment_tracker.create_experiment(
            name=name,
            description=description,
            tags=tags
        )
    
    def get_experiment(self, experiment_id: str) -> Experiment:
        """
        Get an experiment by ID.
        
        Args:
            experiment_id: Experiment ID.
            
        Returns:
            Retrieved Experiment object.
        """
        return self.experiment_tracker.get_experiment(experiment_id)
    
    def list_experiments(self) -> List[Dict[str, Any]]:
        """
        List all experiments.
        
        Returns:
            List of experiment metadata dictionaries.
        """
        self.logger.info("Listing experiments")
        return self.experiment_tracker.list_experiments()
    
    def delete_experiment(self, experiment_id: str) -> bool:
        """
        Delete an experiment.
        
        Args:
            experiment_id: Experiment ID.
            
        Returns:
            True if the experiment was deleted, False otherwise.
        """
        self.logger.info(f"Deleting experiment: {experiment_id}")
        return self.experiment_tracker.delete_experiment(experiment_id)
    
    def create_run(self, experiment_id: str, name: Optional[str] = None,
                  description: Optional[str] = None, tags: Optional[List[str]] = None) -> Run:
        """
        Create a new run.
        
        Args:
            experiment_id: Experiment ID.
            name: Optional run name.
            description: Optional run description.
            tags: Optional list of tags.
            
        Returns:
            Created Run object.
        """
        self.logger.info(f"Creating run for experiment: {experiment_id}")
        
        # Set experiment
        self.experiment_tracker.set_experiment(experiment_id)
        
        return self.experiment_tracker.create_run(
            name=name,
            description=description,
            tags=tags
        )
    
    def start_run(self) -> Run:
        """
        Start the current run.
        
        Returns:
            Started Run object.
        """
        self.logger.info("Starting run")
        return self.experiment_tracker.start_run()
    
    def end_run(self, status: str = "completed", error_message: Optional[str] = None) -> Run:
        """
        End the current run.
        
        Args:
            status: Run status. Options: 'completed', 'failed'.
            error_message: Optional error message if the run failed.
            
        Returns:
            Ended Run object.
        """
        self.logger.info(f"Ending run with status: {status}")
        return self.experiment_tracker.end_run(status=status, error_message=error_message)
    
    def log_metric(self, key: str, value: Union[int, float]) -> None:
        """
        Log a metric for the current run.
        
        Args:
            key: Metric name.
            value: Metric value.
        """
        self.experiment_tracker.log_metric(key, value)
    
    def log_parameter(self, key: str, value: Any) -> None:
        """
        Log a parameter for the current run.
        
        Args:
            key: Parameter name.
            value: Parameter value.
        """
        self.experiment_tracker.log_parameter(key, value)
    
    def log_model(self, model: Any, model_path: Optional[str] = None) -> str:
        """
        Log a model for the current run.
        
        Args:
            model: Model object.
            model_path: Optional path to save the model.
            
        Returns:
            Path to the saved model.
        """
        return self.experiment_tracker.log_model(model, model_path)
    
    def visualize_experiment(self, experiment_id: str, metrics: List[str],
                            params: Optional[List[str]] = None, output_dir: Optional[str] = None,
                            format: str = 'html') -> str:
        """
        Visualize an experiment.
        
        Args:
            experiment_id: Experiment ID.
            metrics: List of metrics to visualize.
            params: Optional list of parameters to visualize.
            output_dir: Optional directory to save visualizations.
            format: Output format. Options: 'html', 'png', 'pdf'.
            
        Returns:
            Path to the visualization report.
        """
        self.logger.info(f"Visualizing experiment: {experiment_id}")
        
        # Create output directory if specified
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Generate visualizations
        if format == 'html':
            # Generate HTML report
            report_path = self.tracking_visualizer.export_experiment_report(
                experiment_id=experiment_id,
                output_dir=output_dir or os.getcwd(),
                metrics=metrics,
                params=params
            )
            
            self.logger.info(f"Visualization report saved to: {report_path}")
            return report_path
        else:
            # Generate individual visualizations
            experiment = self.experiment_tracker.get_experiment(experiment_id)
            
            # Get run IDs
            run_ids = [run.run_id for run in experiment.runs]
            
            # Generate metric comparison plots
            for metric in metrics:
                try:
                    fig = self.tracking_visualizer.plot_metric_comparison(
                        run_ids=run_ids,
                        metric=metric,
                        use_plotly=False
                    )
                    
                    if output_dir:
                        output_file = os.path.join(output_dir, f"metric_{metric}.{format}")
                        fig.savefig(output_file)
                        self.logger.info(f"Metric comparison plot saved to: {output_file}")
                except Exception as e:
                    self.logger.warning(f"Error generating metric comparison for {metric}: {str(e)}")
            
            # Generate parameter importance plots
            if params:
                for metric in metrics:
                    try:
                        fig = self.tracking_visualizer.plot_parameter_importance(
                            experiment_id=experiment_id,
                            metric=metric,
                            use_plotly=False
                        )
                        
                        if output_dir:
                            output_file = os.path.join(output_dir, f"param_importance_{metric}.{format}")
                            fig.savefig(output_file)
                            self.logger.info(f"Parameter importance plot saved to: {output_file}")
                    except Exception as e:
                        self.logger.warning(f"Error generating parameter importance for {metric}: {str(e)}")
            
            # Return output directory
            return output_dir or os.getcwd()
    
    #
    # Context Manager Support
    #
    
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
        # Clean up resources if needed
        pass
