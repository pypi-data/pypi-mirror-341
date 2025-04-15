import unittest
import pandas as pd
import numpy as np
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from sbyb.api import SBYB
from sbyb.preprocessing import PreprocessingPipeline
from sbyb.task_detection import TaskDetector
from sbyb.automl import AutoMLEngine
from sbyb.evaluation import Evaluator, Explainer
from sbyb.deployment import ModelExporter, ModelServer
from sbyb.ui_generator import DashboardGenerator, FormGenerator
from sbyb.scaffolding import ProjectGenerator
from sbyb.eda import DataProfiler, Visualizer, DataAnalyzer
from sbyb.plugins import PluginManager
from sbyb.tracking import ExperimentTracker


class TestPreprocessing(unittest.TestCase):
    """Test cases for the preprocessing module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a sample DataFrame for testing
        self.data = pd.DataFrame({
            'numeric_col': [1, 2, 3, 4, 5, np.nan],
            'categorical_col': ['A', 'B', 'C', 'A', np.nan, 'B'],
            'binary_col': [0, 1, 0, 1, 0, np.nan],
            'date_col': pd.date_range(start='2023-01-01', periods=6)
        })
        
        # Initialize preprocessing pipeline
        self.pipeline = PreprocessingPipeline()
    
    def test_missing_value_imputation(self):
        """Test missing value imputation."""
        # Configure pipeline for imputation
        self.pipeline.add_step('imputer', strategy='mean', columns=['numeric_col'])
        self.pipeline.add_step('imputer', strategy='most_frequent', columns=['categorical_col', 'binary_col'])
        
        # Apply pipeline
        result = self.pipeline.fit_transform(self.data)
        
        # Check that there are no missing values
        self.assertEqual(result.isna().sum().sum(), 0)
        
        # Check that numeric imputation used mean
        self.assertAlmostEqual(result['numeric_col'].iloc[5], 3.0)
        
        # Check that categorical imputation used most frequent
        self.assertEqual(result['categorical_col'].iloc[4], 'A')
        
        # Check that binary imputation used most frequent
        self.assertEqual(result['binary_col'].iloc[5], 0)
    
    def test_categorical_encoding(self):
        """Test categorical encoding."""
        # Configure pipeline for encoding
        self.pipeline.add_step('encoder', method='one_hot', columns=['categorical_col'])
        
        # Apply pipeline
        result = self.pipeline.fit_transform(self.data)
        
        # Check that one-hot encoding created new columns
        self.assertIn('categorical_col_A', result.columns)
        self.assertIn('categorical_col_B', result.columns)
        self.assertIn('categorical_col_C', result.columns)
        
        # Check that original column was dropped
        self.assertNotIn('categorical_col', result.columns)
        
        # Check encoding values
        self.assertEqual(result['categorical_col_A'].iloc[0], 1)
        self.assertEqual(result['categorical_col_B'].iloc[0], 0)
        self.assertEqual(result['categorical_col_C'].iloc[0], 0)
    
    def test_scaling(self):
        """Test feature scaling."""
        # Configure pipeline for scaling
        self.pipeline.add_step('scaler', method='standard', columns=['numeric_col'])
        
        # Apply pipeline
        result = self.pipeline.fit_transform(self.data)
        
        # Check that scaling was applied
        self.assertAlmostEqual(result['numeric_col'].mean(), 0.0, places=10)
        self.assertAlmostEqual(result['numeric_col'].std(), 1.0, places=10)
    
    def test_pipeline_save_load(self):
        """Test saving and loading pipeline."""
        # Configure pipeline
        self.pipeline.add_step('imputer', strategy='mean', columns=['numeric_col'])
        self.pipeline.add_step('encoder', method='one_hot', columns=['categorical_col'])
        self.pipeline.add_step('scaler', method='standard', columns=['numeric_col'])
        
        # Fit pipeline
        self.pipeline.fit(self.data)
        
        # Save pipeline to temporary file
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as tmp:
            pipeline_file = tmp.name
        
        self.pipeline.save(pipeline_file)
        
        # Load pipeline
        loaded_pipeline = PreprocessingPipeline.load(pipeline_file)
        
        # Apply both pipelines
        result1 = self.pipeline.transform(self.data)
        result2 = loaded_pipeline.transform(self.data)
        
        # Check that results are identical
        pd.testing.assert_frame_equal(result1, result2)
        
        # Clean up
        os.unlink(pipeline_file)


class TestTaskDetection(unittest.TestCase):
    """Test cases for the task detection module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize task detector
        self.detector = TaskDetector()
        
        # Create sample datasets for different tasks
        
        # Classification dataset
        self.X_clf = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100)
        })
        self.y_clf = pd.Series(np.random.randint(0, 3, 100))
        
        # Binary classification dataset
        self.X_bin = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100)
        })
        self.y_bin = pd.Series(np.random.randint(0, 2, 100))
        
        # Regression dataset
        self.X_reg = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100)
        })
        self.y_reg = pd.Series(np.random.randn(100))
    
    def test_classification_detection(self):
        """Test classification task detection."""
        task = self.detector.detect(self.X_clf, self.y_clf)
        self.assertEqual(task, 'classification')
    
    def test_binary_classification_detection(self):
        """Test binary classification task detection."""
        task = self.detector.detect(self.X_bin, self.y_bin)
        self.assertEqual(task, 'binary_classification')
    
    def test_regression_detection(self):
        """Test regression task detection."""
        task = self.detector.detect(self.X_reg, self.y_reg)
        self.assertEqual(task, 'regression')


class TestAutoML(unittest.TestCase):
    """Test cases for the AutoML module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize AutoML engine
        self.automl = AutoMLEngine()
        
        # Create a simple classification dataset
        self.X = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100)
        })
        self.y = pd.Series(np.random.randint(0, 2, 100))
    
    @patch('sbyb.automl.engine.AutoMLEngine._train_models')
    def test_automl_fit(self, mock_train):
        """Test AutoML fit method."""
        # Mock the _train_models method to avoid actual training
        mock_result = MagicMock()
        mock_result.best_model_name = 'RandomForest'
        mock_result.model = MagicMock()
        mock_result.metrics = {'accuracy': 0.95, 'f1': 0.94}
        mock_result.leaderboard = pd.DataFrame({
            'model': ['RandomForest', 'LogisticRegression'],
            'accuracy': [0.95, 0.90]
        })
        mock_result.predictions = pd.DataFrame({
            'actual': self.y,
            'predicted': self.y
        })
        mock_train.return_value = mock_result
        
        # Set task type
        self.automl.set_task('classification')
        
        # Run AutoML
        result = self.automl.fit(self.X, self.y)
        
        # Check that _train_models was called
        mock_train.assert_called_once()
        
        # Check result attributes
        self.assertEqual(result.best_model_name, 'RandomForest')
        self.assertEqual(result.metrics['accuracy'], 0.95)
        self.assertEqual(len(result.leaderboard), 2)
    
    def test_automl_config(self):
        """Test AutoML configuration."""
        # Set configuration
        config = {
            'time_limit': 60,
            'models': ['RandomForest', 'LogisticRegression'],
            'metric': 'accuracy'
        }
        self.automl.update_config(config)
        
        # Check that configuration was updated
        self.assertEqual(self.automl.config['time_limit'], 60)
        self.assertEqual(self.automl.config['models'], ['RandomForest', 'LogisticRegression'])
        self.assertEqual(self.automl.config['metric'], 'accuracy')


class TestEvaluation(unittest.TestCase):
    """Test cases for the evaluation module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize evaluator
        self.evaluator = Evaluator()
        
        # Create a simple classification dataset
        self.X = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100)
        })
        self.y = pd.Series(np.random.randint(0, 2, 100))
        
        # Create a mock model
        self.model = MagicMock()
        self.model.predict.return_value = self.y
        self.model.predict_proba.return_value = np.random.rand(100, 2)
    
    def test_classification_metrics(self):
        """Test classification metrics calculation."""
        # Evaluate model
        evaluation = self.evaluator.evaluate(self.model, self.X, self.y)
        
        # Check that metrics were calculated
        self.assertIn('accuracy', evaluation.metrics)
        self.assertIn('precision', evaluation.metrics)
        self.assertIn('recall', evaluation.metrics)
        self.assertIn('f1', evaluation.metrics)
        
        # Check that confusion matrix was created
        self.assertIsNotNone(evaluation.confusion_matrix)
    
    def test_custom_metrics(self):
        """Test custom metrics calculation."""
        # Evaluate model with custom metrics
        evaluation = self.evaluator.evaluate(self.model, self.X, self.y, metrics=['accuracy', 'f1'])
        
        # Check that only specified metrics were calculated
        self.assertIn('accuracy', evaluation.metrics)
        self.assertIn('f1', evaluation.metrics)
        self.assertNotIn('precision', evaluation.metrics)
        self.assertNotIn('recall', evaluation.metrics)


class TestExplainability(unittest.TestCase):
    """Test cases for the explainability module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize explainer
        self.explainer = Explainer()
        
        # Create a simple classification dataset
        self.X = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100)
        })
        
        # Create a mock model
        self.model = MagicMock()
        self.model.predict.return_value = np.random.randint(0, 2, 100)
        self.model.predict_proba.return_value = np.random.rand(100, 2)
        self.model.feature_importances_ = np.array([0.7, 0.3])
    
    @patch('sbyb.evaluation.explainer.shap.Explainer')
    def test_shap_explanation(self, mock_shap):
        """Test SHAP explanation."""
        # Mock SHAP explainer
        mock_shap_explainer = MagicMock()
        mock_shap_explainer.shap_values.return_value = np.random.randn(100, 2)
        mock_shap.return_value = mock_shap_explainer
        
        # Generate explanation
        explanation = self.explainer.explain(self.model, self.X, method='shap')
        
        # Check that SHAP values were calculated
        self.assertIsNotNone(explanation.shap_values)
        
        # Check that feature importance was calculated
        self.assertIsNotNone(explanation.feature_importance)


class TestDeployment(unittest.TestCase):
    """Test cases for the deployment module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize model exporter
        self.exporter = ModelExporter()
        
        # Create a mock model
        self.model = MagicMock()
        self.model.predict.return_value = np.random.randint(0, 2, 10)
    
    def test_pickle_export(self):
        """Test pickle export."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as tmp:
            output_file = tmp.name
        
        # Export model
        path = self.exporter.to_pickle(self.model, output_file)
        
        # Check that file was created
        self.assertTrue(os.path.exists(path))
        
        # Clean up
        os.unlink(path)
    
    @patch('sbyb.deployment.model_export.onnx')
    def test_onnx_export(self, mock_onnx):
        """Test ONNX export."""
        # Mock ONNX conversion
        mock_onnx.convert_sklearn.return_value = MagicMock()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.onnx', delete=False) as tmp:
            output_file = tmp.name
        
        # Export model
        path = self.exporter.to_onnx(self.model, output_file)
        
        # Check that file was created
        self.assertTrue(os.path.exists(path))
        
        # Clean up
        os.unlink(path)


class TestUIGenerator(unittest.TestCase):
    """Test cases for the UI generator module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize UI generators
        self.dashboard_generator = DashboardGenerator()
        self.form_generator = FormGenerator()
        
        # Create a mock model
        self.model = MagicMock()
        self.model.predict.return_value = np.random.randint(0, 2, 10)
        self.model.feature_names_in_ = ['feature1', 'feature2']
    
    def test_dashboard_generation(self):
        """Test dashboard generation."""
        # Create temporary directory
        output_dir = tempfile.mkdtemp()
        
        # Generate dashboard
        path = self.dashboard_generator.generate(self.model, output_dir=output_dir)
        
        # Check that files were created
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.exists(os.path.join(path, 'app.py')))
        
        # Clean up
        shutil.rmtree(output_dir)
    
    def test_form_generation(self):
        """Test form generation."""
        # Create temporary directory
        output_dir = tempfile.mkdtemp()
        
        # Generate form
        path = self.form_generator.generate(self.model, output_dir=output_dir)
        
        # Check that files were created
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.exists(os.path.join(path, 'app.py')))
        
        # Clean up
        shutil.rmtree(output_dir)


class TestScaffolding(unittest.TestCase):
    """Test cases for the scaffolding module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize project generator
        self.project_generator = ProjectGenerator()
    
    def test_project_creation(self):
        """Test project creation."""
        # Create temporary directory
        output_dir = tempfile.mkdtemp()
        
        # Generate project
        project_name = 'test_project'
        path = self.project_generator.create_project(
            name=project_name,
            template='basic',
            output_dir=output_dir
        )
        
        # Check that project directory was created
        self.assertTrue(os.path.exists(path))
        
        # Check that key files were created
        self.assertTrue(os.path.exists(os.path.join(path, 'setup.py')))
        self.assertTrue(os.path.exists(os.path.join(path, 'README.md')))
        self.assertTrue(os.path.exists(os.path.join(path, project_name)))
        
        # Clean up
        shutil.rmtree(output_dir)


class TestEDA(unittest.TestCase):
    """Test cases for the EDA module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize EDA components
        self.profiler = DataProfiler()
        self.visualizer = Visualizer()
        self.analyzer = DataAnalyzer()
        
        # Create a sample DataFrame for testing
        self.data = pd.DataFrame({
            'numeric_col1': np.random.randn(100),
            'numeric_col2': np.random.randn(100),
            'categorical_col': np.random.choice(['A', 'B', 'C'], 100)
        })
    
    def test_profile_generation(self):
        """Test profile generation."""
        # Generate profile
        profile = self.profiler.generate_profile(self.data)
        
        # Check that profile was created
        self.assertIsNotNone(profile)
        
        # Check that profile contains basic statistics
        self.assertIn('row_count', profile.summary)
        self.assertIn('column_count', profile.summary)
        self.assertIn('missing_values', profile.summary)
    
    def test_visualization(self):
        """Test visualization generation."""
        # Generate histogram
        fig = self.visualizer.plot_histogram(self.data, 'numeric_col1')
        
        # Check that figure was created
        self.assertIsNotNone(fig)
        
        # Generate correlation matrix
        fig = self.visualizer.plot_correlation_matrix(self.data)
        
        # Check that figure was created
        self.assertIsNotNone(fig)
    
    def test_analysis(self):
        """Test data analysis."""
        # Analyze data
        analysis = self.analyzer.analyze(self.data)
        
        # Check that analysis was created
        self.assertIsNotNone(analysis)
        
        # Check that analysis contains insights
        self.assertIn('insights', analysis)
        self.assertIn('recommendations', analysis)


class TestPlugins(unittest.TestCase):
    """Test cases for the plugin system."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize plugin manager
        self.plugin_manager = PluginManager()
    
    @patch('sbyb.plugins.manager.PluginManager._load_plugin')
    def test_plugin_installation(self, mock_load):
        """Test plugin installation."""
        # Mock plugin loading
        mock_load.return_value = True
        
        # Install plugin
        success = self.plugin_manager.install_plugin('test-plugin')
        
        # Check that installation was successful
        self.assertTrue(success)
        
        # Check that _load_plugin was called
        mock_load.assert_called_once()
    
    @patch('sbyb.plugins.manager.PluginManager._create_plugin_files')
    def test_plugin_template_creation(self, mock_create):
        """Test plugin template creation."""
        # Mock file creation
        mock_create.return_value = True
        
        # Create plugin template
        success = self.plugin_manager.create_plugin_template(
            output_dir='.',
            name='test-plugin',
            category='custom'
        )
        
        # Check that template creation was successful
        self.assertTrue(success)
        
        # Check that _create_plugin_files was called
        mock_create.assert_called_once()


class TestTracking(unittest.TestCase):
    """Test cases for the experiment tracking module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize experiment tracker
        self.tracker = ExperimentTracker()
        
        # Create temporary directory for tracking data
        self.temp_dir = tempfile.mkdtemp()
        self.tracker.storage.base_dir = self.temp_dir
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_experiment_creation(self):
        """Test experiment creation."""
        # Create experiment
        experiment = self.tracker.create_experiment(
            name='Test Experiment',
            description='Test description',
            tags=['tag1', 'tag2']
        )
        
        # Check that experiment was created
        self.assertIsNotNone(experiment)
        self.assertEqual(experiment.name, 'Test Experiment')
        self.assertEqual(experiment.description, 'Test description')
        self.assertEqual(experiment.tags, ['tag1', 'tag2'])
        
        # Check that experiment was saved
        experiments = self.tracker.list_experiments()
        self.assertEqual(len(experiments), 1)
        self.assertEqual(experiments[0]['name'], 'Test Experiment')
    
    def test_run_creation(self):
        """Test run creation."""
        # Create experiment
        experiment = self.tracker.create_experiment(name='Test Experiment')
        
        # Set experiment
        self.tracker.set_experiment(experiment.experiment_id)
        
        # Create run
        run = self.tracker.create_run(
            name='Test Run',
            description='Test description',
            tags=['tag1', 'tag2']
        )
        
        # Check that run was created
        self.assertIsNotNone(run)
        self.assertEqual(run.name, 'Test Run')
        self.assertEqual(run.description, 'Test description')
        self.assertEqual(run.tags, ['tag1', 'tag2'])
        
        # Check that run was saved
        runs = self.tracker.list_runs(experiment.experiment_id)
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]['name'], 'Test Run')
    
    def test_metric_logging(self):
        """Test metric logging."""
        # Create experiment and run
        experiment = self.tracker.create_experiment(name='Test Experiment')
        self.tracker.set_experiment(experiment.experiment_id)
        run = self.tracker.create_run(name='Test Run')
        self.tracker.start_run()
        
        # Log metric
        self.tracker.log_metric('accuracy', 0.95)
        
        # End run
        self.tracker.end_run()
        
        # Check that metric was saved
        runs = self.tracker.list_runs(experiment.experiment_id)
        self.assertEqual(len(runs), 1)
        self.assertIn('metrics', runs[0])
        self.assertIn('accuracy', runs[0]['metrics'])
        self.assertEqual(runs[0]['metrics']['accuracy'], 0.95)


class TestAPI(unittest.TestCase):
    """Test cases for the API interface."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize SBYB API
        self.sbyb = SBYB()
        
        # Create a sample DataFrame for testing
        self.data = pd.DataFrame({
            'numeric_col': np.random.randn(100),
            'categorical_col': np.random.choice(['A', 'B', 'C'], 100),
            'target': np.random.randint(0, 2, 100)
        })
    
    @patch('sbyb.preprocessing.PreprocessingPipeline.fit_transform')
    def test_preprocess_data(self, mock_fit_transform):
        """Test preprocess_data method."""
        # Mock fit_transform
        mock_fit_transform.return_value = self.data
        
        # Preprocess data
        result = self.sbyb.preprocess_data(self.data)
        
        # Check that fit_transform was called
        mock_fit_transform.assert_called_once()
        
        # Check that result is correct
        self.assertIs(result, self.data)
    
    @patch('sbyb.task_detection.TaskDetector.detect')
    @patch('sbyb.automl.AutoMLEngine.fit')
    def test_run_automl(self, mock_fit, mock_detect):
        """Test run_automl method."""
        # Mock detect and fit
        mock_detect.return_value = 'classification'
        mock_result = MagicMock()
        mock_fit.return_value = mock_result
        
        # Run AutoML
        result = self.sbyb.run_automl(
            data=self.data,
            target='target'
        )
        
        # Check that detect and fit were called
        mock_detect.assert_called_once()
        mock_fit.assert_called_once()
        
        # Check that result is correct
        self.assertIs(result, mock_result)
    
    @patch('sbyb.evaluation.Evaluator.evaluate')
    def test_evaluate_model(self, mock_evaluate):
        """Test evaluate_model method."""
        # Mock evaluate
        mock_result = MagicMock()
        mock_evaluate.return_value = mock_result
        
        # Create mock model
        model = MagicMock()
        
        # Evaluate model
        result = self.sbyb.evaluate_model(
            model=model,
            data=self.data,
            target='target'
        )
        
        # Check that evaluate was called
        mock_evaluate.assert_called_once()
        
        # Check that result is correct
        self.assertIs(result, mock_result)


if __name__ == '__main__':
    unittest.main()
