"""
CLI commands for SBYB.

This module provides the command-line interface commands for the SBYB library,
allowing users to interact with the library from the command line.
"""

import os
import sys
import argparse
import logging
import json
import yaml
import datetime
from typing import Any, Dict, List, Optional, Union, Tuple
import pandas as pd
import numpy as np

from sbyb.core.config import Config
from sbyb.preprocessing import PreprocessingPipeline
from sbyb.task_detection import TaskDetector
from sbyb.automl import AutoMLEngine
from sbyb.evaluation import Evaluator
from sbyb.deployment import ModelExporter, ModelServer
from sbyb.ui_generator import DashboardGenerator, FormGenerator
from sbyb.scaffolding import ProjectGenerator
from sbyb.eda import DataProfiler, Visualizer, DataAnalyzer
from sbyb.plugins import PluginManager
from sbyb.tracking import ExperimentTracker, Run, Experiment, TrackingVisualizer


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('sbyb.cli')


def setup_parser():
    """
    Set up the command-line argument parser.
    
    Returns:
        ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description='SBYB (Step-By-Your-Byte) - A comprehensive ML library',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new project
  sbyb project create --name my_project --template classification
  
  # Run AutoML on a dataset
  sbyb automl run --data data.csv --target target_column
  
  # Generate a UI for a model
  sbyb ui generate --model model.pkl --output ui_app
  
  # Track an experiment
  sbyb track experiment create --name "My Experiment"
  
  # Get help for a specific command
  sbyb <command> --help
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Project commands
    project_parser = subparsers.add_parser('project', help='Project management commands')
    project_subparsers = project_parser.add_subparsers(dest='subcommand', help='Project subcommand')
    
    # Project create
    project_create_parser = project_subparsers.add_parser('create', help='Create a new project')
    project_create_parser.add_argument('--name', required=True, help='Project name')
    project_create_parser.add_argument('--template', default='basic', 
                                      choices=['basic', 'classification', 'regression', 'time_series'],
                                      help='Project template')
    project_create_parser.add_argument('--output', default='.', help='Output directory')
    project_create_parser.add_argument('--description', help='Project description')
    
    # Data commands
    data_parser = subparsers.add_parser('data', help='Data preprocessing commands')
    data_subparsers = data_parser.add_subparsers(dest='subcommand', help='Data subcommand')
    
    # Data preprocess
    data_preprocess_parser = data_subparsers.add_parser('preprocess', help='Preprocess data')
    data_preprocess_parser.add_argument('--data', required=True, help='Input data file (CSV, Excel, etc.)')
    data_preprocess_parser.add_argument('--config', help='Preprocessing configuration file (JSON or YAML)')
    data_preprocess_parser.add_argument('--output', help='Output file for preprocessed data')
    data_preprocess_parser.add_argument('--save-pipeline', help='Save preprocessing pipeline to file')
    
    # Data profile
    data_profile_parser = data_subparsers.add_parser('profile', help='Generate data profile')
    data_profile_parser.add_argument('--data', required=True, help='Input data file (CSV, Excel, etc.)')
    data_profile_parser.add_argument('--output', help='Output directory for profile report')
    data_profile_parser.add_argument('--format', default='html', choices=['html', 'json'], 
                                    help='Output format')
    
    # AutoML commands
    automl_parser = subparsers.add_parser('automl', help='AutoML commands')
    automl_subparsers = automl_parser.add_subparsers(dest='subcommand', help='AutoML subcommand')
    
    # AutoML run
    automl_run_parser = automl_subparsers.add_parser('run', help='Run AutoML')
    automl_run_parser.add_argument('--data', required=True, help='Input data file (CSV, Excel, etc.)')
    automl_run_parser.add_argument('--target', required=True, help='Target column name')
    automl_run_parser.add_argument('--task', help='ML task type (auto-detected if not specified)')
    automl_run_parser.add_argument('--config', help='AutoML configuration file (JSON or YAML)')
    automl_run_parser.add_argument('--output', help='Output directory for results')
    automl_run_parser.add_argument('--time-limit', type=int, help='Time limit in seconds')
    automl_run_parser.add_argument('--track', action='store_true', help='Track the experiment')
    automl_run_parser.add_argument('--experiment', help='Experiment name for tracking')
    
    # Evaluation commands
    eval_parser = subparsers.add_parser('eval', help='Evaluation commands')
    eval_subparsers = eval_parser.add_subparsers(dest='subcommand', help='Evaluation subcommand')
    
    # Evaluation run
    eval_run_parser = eval_subparsers.add_parser('run', help='Evaluate a model')
    eval_run_parser.add_argument('--model', required=True, help='Model file')
    eval_run_parser.add_argument('--data', required=True, help='Test data file (CSV, Excel, etc.)')
    eval_run_parser.add_argument('--target', required=True, help='Target column name')
    eval_run_parser.add_argument('--output', help='Output directory for evaluation results')
    eval_run_parser.add_argument('--metrics', help='Comma-separated list of metrics to compute')
    
    # Evaluation explain
    eval_explain_parser = eval_subparsers.add_parser('explain', help='Explain a model')
    eval_explain_parser.add_argument('--model', required=True, help='Model file')
    eval_explain_parser.add_argument('--data', required=True, help='Data file (CSV, Excel, etc.)')
    eval_explain_parser.add_argument('--output', help='Output directory for explanation results')
    eval_explain_parser.add_argument('--method', default='shap', 
                                    choices=['shap', 'lime', 'eli5', 'all'],
                                    help='Explanation method')
    
    # Deployment commands
    deploy_parser = subparsers.add_parser('deploy', help='Deployment commands')
    deploy_subparsers = deploy_parser.add_subparsers(dest='subcommand', help='Deployment subcommand')
    
    # Deployment export
    deploy_export_parser = deploy_subparsers.add_parser('export', help='Export a model')
    deploy_export_parser.add_argument('--model', required=True, help='Model file')
    deploy_export_parser.add_argument('--format', required=True, 
                                     choices=['pickle', 'onnx', 'tensorflow', 'mlflow'],
                                     help='Export format')
    deploy_export_parser.add_argument('--output', help='Output file or directory')
    
    # Deployment serve
    deploy_serve_parser = deploy_subparsers.add_parser('serve', help='Serve a model')
    deploy_serve_parser.add_argument('--model', required=True, help='Model file')
    deploy_serve_parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    deploy_serve_parser.add_argument('--port', type=int, default=8000, help='Port to bind to')
    deploy_serve_parser.add_argument('--server', default='fastapi', 
                                    choices=['fastapi', 'flask', 'streamlit'],
                                    help='Server type')
    
    # UI commands
    ui_parser = subparsers.add_parser('ui', help='UI generation commands')
    ui_subparsers = ui_parser.add_subparsers(dest='subcommand', help='UI subcommand')
    
    # UI generate
    ui_generate_parser = ui_subparsers.add_parser('generate', help='Generate a UI')
    ui_generate_parser.add_argument('--model', required=True, help='Model file')
    ui_generate_parser.add_argument('--output', required=True, help='Output directory')
    ui_generate_parser.add_argument('--type', default='dashboard', 
                                   choices=['dashboard', 'form', 'app'],
                                   help='UI type')
    ui_generate_parser.add_argument('--framework', default='streamlit', 
                                   choices=['streamlit', 'dash', 'flask', 'html'],
                                   help='UI framework')
    ui_generate_parser.add_argument('--theme', help='UI theme')
    
    # Plugin commands
    plugin_parser = subparsers.add_parser('plugin', help='Plugin management commands')
    plugin_subparsers = plugin_parser.add_subparsers(dest='subcommand', help='Plugin subcommand')
    
    # Plugin list
    plugin_list_parser = plugin_subparsers.add_parser('list', help='List installed plugins')
    plugin_list_parser.add_argument('--category', help='Filter by category')
    
    # Plugin install
    plugin_install_parser = plugin_subparsers.add_parser('install', help='Install a plugin')
    plugin_install_parser.add_argument('source', help='Plugin source (local path, git URL, or pip package)')
    plugin_install_parser.add_argument('--force', action='store_true', help='Force installation')
    
    # Plugin uninstall
    plugin_uninstall_parser = plugin_subparsers.add_parser('uninstall', help='Uninstall a plugin')
    plugin_uninstall_parser.add_argument('name', help='Plugin name')
    plugin_uninstall_parser.add_argument('--category', help='Plugin category')
    
    # Plugin create
    plugin_create_parser = plugin_subparsers.add_parser('create', help='Create a plugin template')
    plugin_create_parser.add_argument('name', help='Plugin name')
    plugin_create_parser.add_argument('--category', default='custom', help='Plugin category')
    plugin_create_parser.add_argument('--output', default='.', help='Output directory')
    plugin_create_parser.add_argument('--description', help='Plugin description')
    plugin_create_parser.add_argument('--author', help='Plugin author')
    
    # Tracking commands
    track_parser = subparsers.add_parser('track', help='Experiment tracking commands')
    track_subparsers = track_parser.add_subparsers(dest='subcommand', help='Tracking subcommand')
    
    # Tracking experiment commands
    track_exp_parser = track_subparsers.add_parser('experiment', help='Experiment commands')
    track_exp_subparsers = track_exp_parser.add_subparsers(dest='exp_subcommand', help='Experiment subcommand')
    
    # Tracking experiment create
    track_exp_create_parser = track_exp_subparsers.add_parser('create', help='Create an experiment')
    track_exp_create_parser.add_argument('--name', required=True, help='Experiment name')
    track_exp_create_parser.add_argument('--description', help='Experiment description')
    track_exp_create_parser.add_argument('--tags', help='Comma-separated list of tags')
    
    # Tracking experiment list
    track_exp_list_parser = track_exp_subparsers.add_parser('list', help='List experiments')
    
    # Tracking experiment delete
    track_exp_delete_parser = track_exp_subparsers.add_parser('delete', help='Delete an experiment')
    track_exp_delete_parser.add_argument('--id', required=True, help='Experiment ID')
    
    # Tracking run commands
    track_run_parser = track_subparsers.add_parser('run', help='Run commands')
    track_run_subparsers = track_run_parser.add_subparsers(dest='run_subcommand', help='Run subcommand')
    
    # Tracking run create
    track_run_create_parser = track_run_subparsers.add_parser('create', help='Create a run')
    track_run_create_parser.add_argument('--experiment', required=True, help='Experiment ID')
    track_run_create_parser.add_argument('--name', help='Run name')
    track_run_create_parser.add_argument('--description', help='Run description')
    track_run_create_parser.add_argument('--tags', help='Comma-separated list of tags')
    
    # Tracking run list
    track_run_list_parser = track_run_subparsers.add_parser('list', help='List runs')
    track_run_list_parser.add_argument('--experiment', help='Filter by experiment ID')
    
    # Tracking run delete
    track_run_delete_parser = track_run_subparsers.add_parser('delete', help='Delete a run')
    track_run_delete_parser.add_argument('--id', required=True, help='Run ID')
    
    # Tracking visualize
    track_viz_parser = track_subparsers.add_parser('visualize', help='Visualize tracking data')
    track_viz_parser.add_argument('--experiment', required=True, help='Experiment ID')
    track_viz_parser.add_argument('--metrics', required=True, help='Comma-separated list of metrics')
    track_viz_parser.add_argument('--params', help='Comma-separated list of parameters')
    track_viz_parser.add_argument('--output', help='Output directory for visualizations')
    track_viz_parser.add_argument('--format', default='html', choices=['html', 'png', 'pdf'],
                                 help='Output format')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Show version information')
    
    return parser


def load_config(config_file: Optional[str]) -> Dict[str, Any]:
    """
    Load configuration from a file.
    
    Args:
        config_file: Path to configuration file (JSON or YAML).
        
    Returns:
        Configuration dictionary.
    """
    if not config_file:
        return {}
    
    if not os.path.exists(config_file):
        logger.error(f"Configuration file not found: {config_file}")
        sys.exit(1)
    
    try:
        if config_file.endswith('.json'):
            with open(config_file, 'r') as f:
                return json.load(f)
        elif config_file.endswith(('.yaml', '.yml')):
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            logger.error(f"Unsupported configuration file format: {config_file}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading configuration file: {str(e)}")
        sys.exit(1)


def load_data(data_file: str) -> pd.DataFrame:
    """
    Load data from a file.
    
    Args:
        data_file: Path to data file (CSV, Excel, etc.).
        
    Returns:
        Pandas DataFrame.
    """
    if not os.path.exists(data_file):
        logger.error(f"Data file not found: {data_file}")
        sys.exit(1)
    
    try:
        if data_file.endswith('.csv'):
            return pd.read_csv(data_file)
        elif data_file.endswith(('.xls', '.xlsx')):
            return pd.read_excel(data_file)
        elif data_file.endswith('.parquet'):
            return pd.read_parquet(data_file)
        elif data_file.endswith('.json'):
            return pd.read_json(data_file)
        else:
            logger.error(f"Unsupported data file format: {data_file}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading data file: {str(e)}")
        sys.exit(1)


def handle_project_command(args):
    """
    Handle project commands.
    
    Args:
        args: Command-line arguments.
    """
    if args.subcommand == 'create':
        logger.info(f"Creating new project: {args.name}")
        
        try:
            project_generator = ProjectGenerator()
            
            output_dir = os.path.abspath(args.output)
            project_dir = os.path.join(output_dir, args.name)
            
            project_generator.create_project(
                name=args.name,
                template=args.template,
                output_dir=output_dir,
                description=args.description or f"{args.name} - A SBYB project"
            )
            
            logger.info(f"Project created successfully: {project_dir}")
            logger.info(f"To get started, navigate to the project directory:")
            logger.info(f"  cd {project_dir}")
            logger.info(f"  pip install -e .")
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}")
            sys.exit(1)
    else:
        logger.error(f"Unknown project subcommand: {args.subcommand}")
        sys.exit(1)


def handle_data_command(args):
    """
    Handle data commands.
    
    Args:
        args: Command-line arguments.
    """
    if args.subcommand == 'preprocess':
        logger.info(f"Preprocessing data: {args.data}")
        
        try:
            # Load data
            data = load_data(args.data)
            
            # Load configuration
            config = load_config(args.config) if args.config else {}
            
            # Create preprocessing pipeline
            pipeline = PreprocessingPipeline(config)
            
            # Preprocess data
            preprocessed_data = pipeline.fit_transform(data)
            
            # Save preprocessed data
            if args.output:
                output_file = args.output
                
                if output_file.endswith('.csv'):
                    preprocessed_data.to_csv(output_file, index=False)
                elif output_file.endswith(('.xls', '.xlsx')):
                    preprocessed_data.to_excel(output_file, index=False)
                elif output_file.endswith('.parquet'):
                    preprocessed_data.to_parquet(output_file, index=False)
                else:
                    preprocessed_data.to_csv(output_file, index=False)
                
                logger.info(f"Preprocessed data saved to: {output_file}")
            
            # Save pipeline
            if args.save_pipeline:
                pipeline.save(args.save_pipeline)
                logger.info(f"Preprocessing pipeline saved to: {args.save_pipeline}")
            
            logger.info("Data preprocessing completed successfully")
        except Exception as e:
            logger.error(f"Error preprocessing data: {str(e)}")
            sys.exit(1)
    
    elif args.subcommand == 'profile':
        logger.info(f"Generating data profile: {args.data}")
        
        try:
            # Load data
            data = load_data(args.data)
            
            # Create data profiler
            profiler = DataProfiler()
            
            # Generate profile
            profile = profiler.generate_profile(data)
            
            # Save profile
            if args.output:
                os.makedirs(args.output, exist_ok=True)
                
                if args.format == 'html':
                    output_file = os.path.join(args.output, 'data_profile.html')
                    profile.to_html(output_file)
                elif args.format == 'json':
                    output_file = os.path.join(args.output, 'data_profile.json')
                    profile.to_json(output_file)
                
                logger.info(f"Data profile saved to: {output_file}")
            else:
                # Print summary to console
                print(profile.get_summary())
            
            logger.info("Data profiling completed successfully")
        except Exception as e:
            logger.error(f"Error profiling data: {str(e)}")
            sys.exit(1)
    
    else:
        logger.error(f"Unknown data subcommand: {args.subcommand}")
        sys.exit(1)


def handle_automl_command(args):
    """
    Handle AutoML commands.
    
    Args:
        args: Command-line arguments.
    """
    if args.subcommand == 'run':
        logger.info(f"Running AutoML on: {args.data}")
        
        try:
            # Load data
            data = load_data(args.data)
            
            # Split features and target
            if args.target not in data.columns:
                logger.error(f"Target column not found: {args.target}")
                sys.exit(1)
            
            X = data.drop(columns=[args.target])
            y = data[args.target]
            
            # Load configuration
            config = load_config(args.config) if args.config else {}
            
            # Set time limit if specified
            if args.time_limit:
                config['time_limit'] = args.time_limit
            
            # Create experiment tracker if tracking is enabled
            tracker = None
            if args.track:
                tracker = ExperimentTracker()
                
                # Create or set experiment
                if args.experiment:
                    try:
                        # Try to find existing experiment
                        experiments = tracker.list_experiments()
                        experiment_id = None
                        
                        for exp in experiments:
                            if exp['name'] == args.experiment:
                                experiment_id = exp['experiment_id']
                                break
                        
                        if experiment_id:
                            tracker.set_experiment(experiment_id)
                            logger.info(f"Using existing experiment: {args.experiment}")
                        else:
                            tracker.create_experiment(name=args.experiment)
                            logger.info(f"Created new experiment: {args.experiment}")
                    except Exception as e:
                        logger.warning(f"Error setting experiment: {str(e)}")
                        tracker.create_experiment(name=f"AutoML Run {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
                else:
                    tracker.create_experiment(name=f"AutoML Run {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
                
                # Create run
                run = tracker.create_run(name=f"AutoML Run {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
                tracker.start_run()
                
                # Log parameters
                tracker.log_parameters({
                    'data_file': args.data,
                    'target_column': args.target,
                    'n_samples': len(data),
                    'n_features': len(X.columns),
                    'time_limit': args.time_limit
                })
            
            # Detect task type if not specified
            task_type = args.task
            if not task_type:
                logger.info("Auto-detecting task type...")
                detector = TaskDetector()
                task_type = detector.detect(X, y)
                logger.info(f"Detected task type: {task_type}")
                
                if tracker:
                    tracker.log_parameter('task_type', task_type)
            
            # Create AutoML engine
            automl = AutoMLEngine(task_type=task_type, config=config)
            
            # Run AutoML
            logger.info("Running AutoML...")
            result = automl.fit(X, y)
            
            # Log metrics if tracking
            if tracker:
                tracker.log_metrics(result.metrics)
                
                # Log model
                if args.output:
                    model_path = os.path.join(args.output, 'model.pkl')
                    os.makedirs(args.output, exist_ok=True)
                    result.save_model(model_path)
                    tracker.log_model(result.model, model_path)
                
                # End run
                tracker.end_run()
            
            # Save results
            if args.output:
                os.makedirs(args.output, exist_ok=True)
                
                # Save model
                model_path = os.path.join(args.output, 'model.pkl')
                result.save_model(model_path)
                logger.info(f"Model saved to: {model_path}")
                
                # Save leaderboard
                leaderboard_path = os.path.join(args.output, 'leaderboard.csv')
                result.leaderboard.to_csv(leaderboard_path, index=False)
                logger.info(f"Leaderboard saved to: {leaderboard_path}")
                
                # Save feature importance
                if hasattr(result, 'feature_importance') and result.feature_importance is not None:
                    fi_path = os.path.join(args.output, 'feature_importance.csv')
                    result.feature_importance.to_csv(fi_path, index=False)
                    logger.info(f"Feature importance saved to: {fi_path}")
                
                # Save predictions
                preds_path = os.path.join(args.output, 'predictions.csv')
                result.predictions.to_csv(preds_path, index=False)
                logger.info(f"Predictions saved to: {preds_path}")
            
            # Print results
            print("\nAutoML Results:")
            print(f"Best model: {result.best_model_name}")
            print("\nPerformance metrics:")
            for metric, value in result.metrics.items():
                print(f"  {metric}: {value}")
            
            print("\nLeaderboard (top 5):")
            print(result.leaderboard.head(5).to_string(index=False))
            
            logger.info("AutoML completed successfully")
        except Exception as e:
            logger.error(f"Error running AutoML: {str(e)}")
            
            # End run with failure if tracking
            if 'tracker' in locals() and tracker and tracker.current_run:
                tracker.end_run(status="failed", error_message=str(e))
            
            sys.exit(1)
    
    else:
        logger.error(f"Unknown automl subcommand: {args.subcommand}")
        sys.exit(1)


def handle_eval_command(args):
    """
    Handle evaluation commands.
    
    Args:
        args: Command-line arguments.
    """
    if args.subcommand == 'run':
        logger.info(f"Evaluating model: {args.model}")
        
        try:
            # Load model
            import pickle
            with open(args.model, 'rb') as f:
                model = pickle.load(f)
            
            # Load data
            data = load_data(args.data)
            
            # Split features and target
            if args.target not in data.columns:
                logger.error(f"Target column not found: {args.target}")
                sys.exit(1)
            
            X = data.drop(columns=[args.target])
            y = data[args.target]
            
            # Create evaluator
            evaluator = Evaluator()
            
            # Parse metrics
            metrics = None
            if args.metrics:
                metrics = [m.strip() for m in args.metrics.split(',')]
            
            # Evaluate model
            evaluation = evaluator.evaluate(model, X, y, metrics=metrics)
            
            # Save results
            if args.output:
                os.makedirs(args.output, exist_ok=True)
                
                # Save metrics
                metrics_path = os.path.join(args.output, 'metrics.json')
                with open(metrics_path, 'w') as f:
                    json.dump(evaluation.metrics, f, indent=2)
                logger.info(f"Metrics saved to: {metrics_path}")
                
                # Save confusion matrix if available
                if hasattr(evaluation, 'confusion_matrix') and evaluation.confusion_matrix is not None:
                    cm_path = os.path.join(args.output, 'confusion_matrix.csv')
                    evaluation.confusion_matrix.to_csv(cm_path, index=False)
                    logger.info(f"Confusion matrix saved to: {cm_path}")
                
                # Save ROC curve if available
                if hasattr(evaluation, 'roc_curve') and evaluation.roc_curve is not None:
                    roc_path = os.path.join(args.output, 'roc_curve.png')
                    evaluation.roc_curve.savefig(roc_path)
                    logger.info(f"ROC curve saved to: {roc_path}")
                
                # Save predictions
                preds_path = os.path.join(args.output, 'predictions.csv')
                evaluation.predictions.to_csv(preds_path, index=False)
                logger.info(f"Predictions saved to: {preds_path}")
            
            # Print results
            print("\nEvaluation Results:")
            print("\nPerformance metrics:")
            for metric, value in evaluation.metrics.items():
                print(f"  {metric}: {value}")
            
            logger.info("Evaluation completed successfully")
        except Exception as e:
            logger.error(f"Error evaluating model: {str(e)}")
            sys.exit(1)
    
    elif args.subcommand == 'explain':
        logger.info(f"Explaining model: {args.model}")
        
        try:
            # Load model
            import pickle
            with open(args.model, 'rb') as f:
                model = pickle.load(f)
            
            # Load data
            data = load_data(args.data)
            
            # Create explainer
            from sbyb.evaluation import Explainer
            explainer = Explainer()
            
            # Generate explanations
            explanation = explainer.explain(model, data, method=args.method)
            
            # Save results
            if args.output:
                os.makedirs(args.output, exist_ok=True)
                
                # Save feature importance
                if hasattr(explanation, 'feature_importance') and explanation.feature_importance is not None:
                    fi_path = os.path.join(args.output, 'feature_importance.csv')
                    explanation.feature_importance.to_csv(fi_path, index=False)
                    logger.info(f"Feature importance saved to: {fi_path}")
                
                # Save SHAP values if available
                if hasattr(explanation, 'shap_values') and explanation.shap_values is not None:
                    shap_path = os.path.join(args.output, 'shap_values.csv')
                    pd.DataFrame(explanation.shap_values).to_csv(shap_path, index=False)
                    logger.info(f"SHAP values saved to: {shap_path}")
                
                # Save SHAP summary plot if available
                if hasattr(explanation, 'shap_summary_plot') and explanation.shap_summary_plot is not None:
                    shap_plot_path = os.path.join(args.output, 'shap_summary.png')
                    explanation.shap_summary_plot.savefig(shap_plot_path)
                    logger.info(f"SHAP summary plot saved to: {shap_plot_path}")
                
                # Save explanation report
                report_path = os.path.join(args.output, 'explanation_report.html')
                explanation.to_html(report_path)
                logger.info(f"Explanation report saved to: {report_path}")
            
            # Print results
            print("\nExplanation Results:")
            if hasattr(explanation, 'feature_importance') and explanation.feature_importance is not None:
                print("\nTop 10 important features:")
                print(explanation.feature_importance.head(10).to_string(index=False))
            
            logger.info("Explanation completed successfully")
        except Exception as e:
            logger.error(f"Error explaining model: {str(e)}")
            sys.exit(1)
    
    else:
        logger.error(f"Unknown eval subcommand: {args.subcommand}")
        sys.exit(1)


def handle_deploy_command(args):
    """
    Handle deployment commands.
    
    Args:
        args: Command-line arguments.
    """
    if args.subcommand == 'export':
        logger.info(f"Exporting model: {args.model}")
        
        try:
            # Load model
            import pickle
            with open(args.model, 'rb') as f:
                model = pickle.load(f)
            
            # Create model exporter
            exporter = ModelExporter()
            
            # Export model
            if args.format == 'pickle':
                output_file = args.output or f"{os.path.splitext(args.model)[0]}_exported.pkl"
                exporter.to_pickle(model, output_file)
                logger.info(f"Model exported to: {output_file}")
            
            elif args.format == 'onnx':
                output_file = args.output or f"{os.path.splitext(args.model)[0]}.onnx"
                exporter.to_onnx(model, output_file)
                logger.info(f"Model exported to: {output_file}")
            
            elif args.format == 'tensorflow':
                output_dir = args.output or f"{os.path.splitext(args.model)[0]}_tf"
                exporter.to_tensorflow(model, output_dir)
                logger.info(f"Model exported to: {output_dir}")
            
            elif args.format == 'mlflow':
                output_dir = args.output or f"{os.path.splitext(args.model)[0]}_mlflow"
                exporter.to_mlflow(model, output_dir)
                logger.info(f"Model exported to: {output_dir}")
            
            logger.info("Model export completed successfully")
        except Exception as e:
            logger.error(f"Error exporting model: {str(e)}")
            sys.exit(1)
    
    elif args.subcommand == 'serve':
        logger.info(f"Serving model: {args.model}")
        
        try:
            # Load model
            import pickle
            with open(args.model, 'rb') as f:
                model = pickle.load(f)
            
            # Create model server
            server = ModelServer(server_type=args.server)
            
            # Serve model
            logger.info(f"Starting {args.server} server on {args.host}:{args.port}")
            server.serve(model, host=args.host, port=args.port)
            
            # Note: This will block until the server is stopped
        except Exception as e:
            logger.error(f"Error serving model: {str(e)}")
            sys.exit(1)
    
    else:
        logger.error(f"Unknown deploy subcommand: {args.subcommand}")
        sys.exit(1)


def handle_ui_command(args):
    """
    Handle UI commands.
    
    Args:
        args: Command-line arguments.
    """
    if args.subcommand == 'generate':
        logger.info(f"Generating UI for model: {args.model}")
        
        try:
            # Load model
            import pickle
            with open(args.model, 'rb') as f:
                model = pickle.load(f)
            
            # Create UI generator
            if args.type == 'dashboard':
                generator = DashboardGenerator(framework=args.framework)
            elif args.type == 'form':
                generator = FormGenerator(framework=args.framework)
            else:  # app
                if args.framework == 'streamlit':
                    from sbyb.ui_generator import StreamlitAppGenerator
                    generator = StreamlitAppGenerator()
                elif args.framework == 'dash':
                    from sbyb.ui_generator import DashAppGenerator
                    generator = DashAppGenerator()
                elif args.framework == 'flask':
                    from sbyb.ui_generator import FlaskAppGenerator
                    generator = FlaskAppGenerator()
                else:  # html
                    from sbyb.ui_generator import HTMLAppGenerator
                    generator = HTMLAppGenerator()
            
            # Set theme if specified
            if args.theme:
                generator.set_theme(args.theme)
            
            # Generate UI
            ui_path = generator.generate(model, output_dir=args.output)
            
            logger.info(f"UI generated successfully: {ui_path}")
            
            # Print instructions
            if args.framework == 'streamlit':
                logger.info(f"To run the UI, execute: streamlit run {os.path.join(ui_path, 'app.py')}")
            elif args.framework == 'dash':
                logger.info(f"To run the UI, execute: python {os.path.join(ui_path, 'app.py')}")
            elif args.framework == 'flask':
                logger.info(f"To run the UI, execute: python {os.path.join(ui_path, 'app.py')}")
            else:  # html
                logger.info(f"Open {os.path.join(ui_path, 'index.html')} in a web browser")
        except Exception as e:
            logger.error(f"Error generating UI: {str(e)}")
            sys.exit(1)
    
    else:
        logger.error(f"Unknown ui subcommand: {args.subcommand}")
        sys.exit(1)


def handle_plugin_command(args):
    """
    Handle plugin commands.
    
    Args:
        args: Command-line arguments.
    """
    # Create plugin manager
    plugin_manager = PluginManager()
    
    if args.subcommand == 'list':
        logger.info("Listing installed plugins")
        
        try:
            plugins = plugin_manager.list_plugins(category=args.category)
            
            if not plugins:
                print("No plugins installed")
                return
            
            for category, category_plugins in plugins.items():
                if not category_plugins:
                    continue
                
                print(f"\n{category.capitalize()} Plugins:")
                for plugin in category_plugins:
                    print(f"  {plugin['name']} (v{plugin['version']})")
                    if plugin.get('description'):
                        print(f"    {plugin['description']}")
        except Exception as e:
            logger.error(f"Error listing plugins: {str(e)}")
            sys.exit(1)
    
    elif args.subcommand == 'install':
        logger.info(f"Installing plugin from: {args.source}")
        
        try:
            success = plugin_manager.install_plugin(args.source, force=args.force)
            
            if success:
                logger.info("Plugin installed successfully")
            else:
                logger.error("Failed to install plugin")
                sys.exit(1)
        except Exception as e:
            logger.error(f"Error installing plugin: {str(e)}")
            sys.exit(1)
    
    elif args.subcommand == 'uninstall':
        logger.info(f"Uninstalling plugin: {args.name}")
        
        try:
            success = plugin_manager.uninstall_plugin(args.name, category=args.category)
            
            if success:
                logger.info("Plugin uninstalled successfully")
            else:
                logger.error("Failed to uninstall plugin")
                sys.exit(1)
        except Exception as e:
            logger.error(f"Error uninstalling plugin: {str(e)}")
            sys.exit(1)
    
    elif args.subcommand == 'create':
        logger.info(f"Creating plugin template: {args.name}")
        
        try:
            success = plugin_manager.create_plugin_template(
                output_dir=args.output,
                name=args.name,
                category=args.category,
                description=args.description or f"{args.name} plugin",
                author=args.author or "SBYB User"
            )
            
            if success:
                plugin_dir = os.path.join(args.output, args.name)
                logger.info(f"Plugin template created successfully: {plugin_dir}")
            else:
                logger.error("Failed to create plugin template")
                sys.exit(1)
        except Exception as e:
            logger.error(f"Error creating plugin template: {str(e)}")
            sys.exit(1)
    
    else:
        logger.error(f"Unknown plugin subcommand: {args.subcommand}")
        sys.exit(1)


def handle_track_command(args):
    """
    Handle tracking commands.
    
    Args:
        args: Command-line arguments.
    """
    # Create experiment tracker
    tracker = ExperimentTracker()
    
    if args.subcommand == 'experiment':
        if args.exp_subcommand == 'create':
            logger.info(f"Creating experiment: {args.name}")
            
            try:
                tags = args.tags.split(',') if args.tags else []
                
                experiment = tracker.create_experiment(
                    name=args.name,
                    description=args.description,
                    tags=tags
                )
                
                print(f"Experiment created successfully:")
                print(f"  ID: {experiment.experiment_id}")
                print(f"  Name: {experiment.name}")
                print(f"  Description: {experiment.description}")
                print(f"  Tags: {', '.join(experiment.tags) if experiment.tags else 'None'}")
            except Exception as e:
                logger.error(f"Error creating experiment: {str(e)}")
                sys.exit(1)
        
        elif args.exp_subcommand == 'list':
            logger.info("Listing experiments")
            
            try:
                experiments = tracker.list_experiments()
                
                if not experiments:
                    print("No experiments found")
                    return
                
                print(f"Found {len(experiments)} experiments:")
                for exp in experiments:
                    print(f"\nID: {exp['experiment_id']}")
                    print(f"Name: {exp['name']}")
                    print(f"Description: {exp.get('description', '')}")
                    print(f"Tags: {', '.join(exp.get('tags', [])) if exp.get('tags') else 'None'}")
                    print(f"Created: {exp['created_at']}")
                    print(f"Runs: {exp.get('run_count', 0)}")
            except Exception as e:
                logger.error(f"Error listing experiments: {str(e)}")
                sys.exit(1)
        
        elif args.exp_subcommand == 'delete':
            logger.info(f"Deleting experiment: {args.id}")
            
            try:
                success = tracker.delete_experiment(args.id)
                
                if success:
                    logger.info("Experiment deleted successfully")
                else:
                    logger.error("Failed to delete experiment")
                    sys.exit(1)
            except Exception as e:
                logger.error(f"Error deleting experiment: {str(e)}")
                sys.exit(1)
        
        else:
            logger.error(f"Unknown experiment subcommand: {args.exp_subcommand}")
            sys.exit(1)
    
    elif args.subcommand == 'run':
        if args.run_subcommand == 'create':
            logger.info(f"Creating run for experiment: {args.experiment}")
            
            try:
                # Set experiment
                tracker.set_experiment(args.experiment)
                
                tags = args.tags.split(',') if args.tags else []
                
                run = tracker.create_run(
                    name=args.name,
                    description=args.description,
                    tags=tags
                )
                
                print(f"Run created successfully:")
                print(f"  ID: {run.run_id}")
                print(f"  Name: {run.name}")
                print(f"  Description: {run.description}")
                print(f"  Tags: {', '.join(run.tags) if run.tags else 'None'}")
                print(f"  Status: {run.status}")
            except Exception as e:
                logger.error(f"Error creating run: {str(e)}")
                sys.exit(1)
        
        elif args.run_subcommand == 'list':
            logger.info("Listing runs")
            
            try:
                runs = tracker.list_runs(experiment_id=args.experiment)
                
                if not runs:
                    print("No runs found")
                    return
                
                print(f"Found {len(runs)} runs:")
                for run in runs:
                    print(f"\nID: {run['run_id']}")
                    print(f"Name: {run['name']}")
                    print(f"Status: {run['status']}")
                    print(f"Created: {run['created_at']}")
                    
                    if run.get('metrics'):
                        print("Metrics:")
                        for metric, value in run['metrics'].items():
                            print(f"  {metric}: {value}")
            except Exception as e:
                logger.error(f"Error listing runs: {str(e)}")
                sys.exit(1)
        
        elif args.run_subcommand == 'delete':
            logger.info(f"Deleting run: {args.id}")
            
            try:
                success = tracker.delete_run(args.id)
                
                if success:
                    logger.info("Run deleted successfully")
                else:
                    logger.error("Failed to delete run")
                    sys.exit(1)
            except Exception as e:
                logger.error(f"Error deleting run: {str(e)}")
                sys.exit(1)
        
        else:
            logger.error(f"Unknown run subcommand: {args.run_subcommand}")
            sys.exit(1)
    
    elif args.subcommand == 'visualize':
        logger.info(f"Visualizing experiment: {args.experiment}")
        
        try:
            # Create visualizer
            visualizer = TrackingVisualizer()
            
            # Parse metrics and parameters
            metrics = [m.strip() for m in args.metrics.split(',')]
            params = [p.strip() for p in args.params.split(',')] if args.params else None
            
            # Create output directory if specified
            if args.output:
                os.makedirs(args.output, exist_ok=True)
            
            # Generate visualizations
            if args.format == 'html':
                # Generate HTML report
                report_path = visualizer.export_experiment_report(
                    experiment_id=args.experiment,
                    output_dir=args.output or os.getcwd(),
                    metrics=metrics,
                    params=params
                )
                
                logger.info(f"Visualization report saved to: {report_path}")
                print(f"Visualization report saved to: {report_path}")
            else:
                # Generate individual visualizations
                experiment = tracker.get_experiment(args.experiment)
                
                # Get run IDs
                run_ids = [run.run_id for run in experiment.runs]
                
                # Generate metric comparison plots
                for metric in metrics:
                    try:
                        fig = visualizer.plot_metric_comparison(
                            run_ids=run_ids,
                            metric=metric,
                            use_plotly=False
                        )
                        
                        if args.output:
                            output_file = os.path.join(args.output, f"metric_{metric}.{args.format}")
                            fig.savefig(output_file)
                            logger.info(f"Metric comparison plot saved to: {output_file}")
                        else:
                            fig.show()
                    except Exception as e:
                        logger.warning(f"Error generating metric comparison for {metric}: {str(e)}")
                
                # Generate parameter importance plots
                if params:
                    for metric in metrics:
                        try:
                            fig = visualizer.plot_parameter_importance(
                                experiment_id=args.experiment,
                                metric=metric,
                                use_plotly=False
                            )
                            
                            if args.output:
                                output_file = os.path.join(args.output, f"param_importance_{metric}.{args.format}")
                                fig.savefig(output_file)
                                logger.info(f"Parameter importance plot saved to: {output_file}")
                            else:
                                fig.show()
                        except Exception as e:
                            logger.warning(f"Error generating parameter importance for {metric}: {str(e)}")
                
                # Generate run status distribution
                try:
                    fig = visualizer.plot_run_status_distribution(
                        experiment_id=args.experiment,
                        use_plotly=False
                    )
                    
                    if args.output:
                        output_file = os.path.join(args.output, f"run_status.{args.format}")
                        fig.savefig(output_file)
                        logger.info(f"Run status plot saved to: {output_file}")
                    else:
                        fig.show()
                except Exception as e:
                    logger.warning(f"Error generating run status distribution: {str(e)}")
                
                # Generate run duration plot
                try:
                    fig = visualizer.plot_run_duration(
                        experiment_id=args.experiment,
                        use_plotly=False
                    )
                    
                    if args.output:
                        output_file = os.path.join(args.output, f"run_duration.{args.format}")
                        fig.savefig(output_file)
                        logger.info(f"Run duration plot saved to: {output_file}")
                    else:
                        fig.show()
                except Exception as e:
                    logger.warning(f"Error generating run duration plot: {str(e)}")
            
            logger.info("Visualization completed successfully")
        except Exception as e:
            logger.error(f"Error visualizing experiment: {str(e)}")
            sys.exit(1)
    
    else:
        logger.error(f"Unknown track subcommand: {args.subcommand}")
        sys.exit(1)


def handle_version_command(args):
    """
    Handle version command.
    
    Args:
        args: Command-line arguments.
    """
    from sbyb import __version__
    print(f"SBYB (Step-By-Your-Byte) version {__version__}")
    print("A comprehensive ML library that unifies the entire ML pipeline")
    print("https://github.com/sbyb/sbyb")


def main():
    """
    Main entry point for the CLI.
    """
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Handle commands
    if args.command == 'project':
        handle_project_command(args)
    elif args.command == 'data':
        handle_data_command(args)
    elif args.command == 'automl':
        handle_automl_command(args)
    elif args.command == 'eval':
        handle_eval_command(args)
    elif args.command == 'deploy':
        handle_deploy_command(args)
    elif args.command == 'ui':
        handle_ui_command(args)
    elif args.command == 'plugin':
        handle_plugin_command(args)
    elif args.command == 'track':
        handle_track_command(args)
    elif args.command == 'version':
        handle_version_command(args)
    else:
        logger.error(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
