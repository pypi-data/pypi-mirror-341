"""
Model export component for SBYB deployment.

This module provides functionality for exporting machine learning models
to various formats for deployment.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import pickle
import json
import datetime

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import ExportError


class ModelExporter(SBYBComponent):
    """
    Model export component.
    
    This component exports machine learning models to various formats for deployment.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the model exporter.
        
        Args:
            config: Configuration dictionary for the exporter.
        """
        super().__init__(config)
        self.export_history = []
    
    def export_pickle(self, model: BaseEstimator, output_path: str, 
                     include_metadata: bool = True, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Export model to pickle format.
        
        Args:
            model: The model to export.
            output_path: Path to save the exported model.
            include_metadata: Whether to include metadata.
            metadata: Additional metadata to include.
            
        Returns:
            Path to the exported model.
        """
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Prepare export object
        if include_metadata:
            # Create metadata if not provided
            if metadata is None:
                metadata = {}
            
            # Add basic metadata
            metadata.update({
                'export_time': datetime.datetime.now().isoformat(),
                'model_type': type(model).__name__,
                'model_module': type(model).__module__,
                'sbyb_version': '0.1.0',  # TODO: Get actual version
                'parameters': model.get_params()
            })
            
            # Create export object with model and metadata
            export_obj = {
                'model': model,
                'metadata': metadata
            }
        else:
            # Export only the model
            export_obj = model
        
        # Save to pickle
        try:
            with open(output_path, 'wb') as f:
                pickle.dump(export_obj, f)
        except Exception as e:
            raise ExportError(f"Failed to export model to pickle: {str(e)}")
        
        # Record export
        self.export_history.append({
            'format': 'pickle',
            'path': output_path,
            'timestamp': datetime.datetime.now().isoformat(),
            'include_metadata': include_metadata
        })
        
        return output_path
    
    def export_onnx(self, model: BaseEstimator, output_path: str, 
                   input_shape: Tuple[int, ...], input_names: Optional[List[str]] = None,
                   output_names: Optional[List[str]] = None) -> str:
        """
        Export model to ONNX format.
        
        Args:
            model: The model to export.
            output_path: Path to save the exported model.
            input_shape: Shape of the input data.
            input_names: Names of the input features.
            output_names: Names of the outputs.
            
        Returns:
            Path to the exported model.
        """
        try:
            import onnxmltools
            from skl2onnx import convert_sklearn
            from skl2onnx.common.data_types import FloatTensorType
        except ImportError:
            raise ExportError("ONNX export requires onnxmltools and skl2onnx. "
                             "Please install them with 'pip install onnxmltools skl2onnx'.")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Set default input and output names if not provided
        if input_names is None:
            if hasattr(model, 'feature_names_in_'):
                input_names = model.feature_names_in_.tolist()
            else:
                input_names = [f'input_{i}' for i in range(input_shape[1])]
        
        if output_names is None:
            output_names = ['output']
        
        # Define input type
        input_type = [('input', FloatTensorType(input_shape))]
        
        # Convert model to ONNX
        try:
            onnx_model = convert_sklearn(model, initial_types=input_type, 
                                        target_opset=12)
            
            # Save model
            with open(output_path, 'wb') as f:
                f.write(onnx_model.SerializeToString())
        except Exception as e:
            raise ExportError(f"Failed to export model to ONNX: {str(e)}")
        
        # Record export
        self.export_history.append({
            'format': 'onnx',
            'path': output_path,
            'timestamp': datetime.datetime.now().isoformat(),
            'input_shape': input_shape
        })
        
        return output_path
    
    def export_tensorflow_savedmodel(self, model: BaseEstimator, output_dir: str,
                                    input_shape: Tuple[int, ...]) -> str:
        """
        Export model to TensorFlow SavedModel format.
        
        Args:
            model: The model to export.
            output_dir: Directory to save the exported model.
            input_shape: Shape of the input data.
            
        Returns:
            Path to the exported model.
        """
        try:
            import tensorflow as tf
            from tensorflow import keras
        except ImportError:
            raise ExportError("TensorFlow export requires tensorflow. "
                             "Please install it with 'pip install tensorflow'.")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create a TensorFlow wrapper for the scikit-learn model
        class SklearnModelWrapper(keras.Model):
            def __init__(self, sklearn_model):
                super().__init__()
                self.sklearn_model = sklearn_model
            
            def call(self, inputs):
                # Convert TensorFlow tensor to numpy array
                inputs_np = inputs.numpy()
                # Make predictions with scikit-learn model
                outputs_np = self.sklearn_model.predict(inputs_np)
                # Convert back to TensorFlow tensor
                return tf.convert_to_tensor(outputs_np, dtype=tf.float32)
        
        # Create wrapper model
        tf_model = SklearnModelWrapper(model)
        
        # Create a concrete function for the model
        @tf.function(input_signature=[tf.TensorSpec(shape=input_shape, dtype=tf.float32)])
        def serving_fn(inputs):
            return tf_model(inputs)
        
        # Save the model
        try:
            tf.saved_model.save(
                tf_model,
                output_dir,
                signatures={'serving_default': serving_fn}
            )
        except Exception as e:
            raise ExportError(f"Failed to export model to TensorFlow SavedModel: {str(e)}")
        
        # Record export
        self.export_history.append({
            'format': 'tensorflow_savedmodel',
            'path': output_dir,
            'timestamp': datetime.datetime.now().isoformat(),
            'input_shape': input_shape
        })
        
        return output_dir
    
    def export_pyfunc(self, model: BaseEstimator, output_path: str,
                     conda_env: Optional[Dict[str, Any]] = None,
                     code_paths: Optional[List[str]] = None) -> str:
        """
        Export model as a Python function using MLflow.
        
        Args:
            model: The model to export.
            output_path: Path to save the exported model.
            conda_env: Conda environment specification.
            code_paths: Paths to additional code dependencies.
            
        Returns:
            Path to the exported model.
        """
        try:
            import mlflow
        except ImportError:
            raise ExportError("MLflow export requires mlflow. "
                             "Please install it with 'pip install mlflow'.")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Create default conda environment if not provided
        if conda_env is None:
            conda_env = {
                'name': 'sbyb_env',
                'channels': ['defaults'],
                'dependencies': [
                    'python=3.8',
                    'scikit-learn',
                    'pandas',
                    'numpy',
                    {'pip': ['mlflow']}
                ]
            }
        
        # Create a wrapper class for the model
        class SBYBModelWrapper(mlflow.pyfunc.PythonModel):
            def __init__(self, model):
                self.model = model
            
            def predict(self, context, model_input):
                # Convert to pandas DataFrame if it's not already
                if not isinstance(model_input, pd.DataFrame):
                    model_input = pd.DataFrame(model_input)
                
                # Make predictions
                return self.model.predict(model_input)
        
        # Create wrapper
        wrapped_model = SBYBModelWrapper(model)
        
        # Save the model
        try:
            mlflow.pyfunc.save_model(
                path=output_path,
                python_model=wrapped_model,
                conda_env=conda_env,
                code_path=code_paths
            )
        except Exception as e:
            raise ExportError(f"Failed to export model as Python function: {str(e)}")
        
        # Record export
        self.export_history.append({
            'format': 'pyfunc',
            'path': output_path,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        return output_path
    
    def export_with_pipeline(self, pipeline: Any, output_path: str,
                            include_metadata: bool = True, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Export a complete pipeline (preprocessing + model) to pickle format.
        
        Args:
            pipeline: The pipeline to export.
            output_path: Path to save the exported pipeline.
            include_metadata: Whether to include metadata.
            metadata: Additional metadata to include.
            
        Returns:
            Path to the exported pipeline.
        """
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Prepare export object
        if include_metadata:
            # Create metadata if not provided
            if metadata is None:
                metadata = {}
            
            # Add basic metadata
            metadata.update({
                'export_time': datetime.datetime.now().isoformat(),
                'pipeline_type': type(pipeline).__name__,
                'pipeline_module': type(pipeline).__module__,
                'sbyb_version': '0.1.0',  # TODO: Get actual version
                'parameters': pipeline.get_params() if hasattr(pipeline, 'get_params') else {}
            })
            
            # Create export object with pipeline and metadata
            export_obj = {
                'pipeline': pipeline,
                'metadata': metadata
            }
        else:
            # Export only the pipeline
            export_obj = pipeline
        
        # Save to pickle
        try:
            with open(output_path, 'wb') as f:
                pickle.dump(export_obj, f)
        except Exception as e:
            raise ExportError(f"Failed to export pipeline to pickle: {str(e)}")
        
        # Record export
        self.export_history.append({
            'format': 'pickle_pipeline',
            'path': output_path,
            'timestamp': datetime.datetime.now().isoformat(),
            'include_metadata': include_metadata
        })
        
        return output_path
    
    def get_export_history(self) -> List[Dict[str, Any]]:
        """
        Get the export history.
        
        Returns:
            List of export records.
        """
        return self.export_history
