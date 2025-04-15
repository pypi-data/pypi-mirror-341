"""
Model serving component for SBYB deployment.

This module provides functionality for serving machine learning models
through various interfaces.
"""

from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import os
import pickle
import json
import threading
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import io

import numpy as np
import pandas as pd

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import ServingError


class ModelServer(SBYBComponent):
    """
    Model serving component.
    
    This component serves machine learning models through various interfaces.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the model server.
        
        Args:
            config: Configuration dictionary for the server.
        """
        super().__init__(config)
        self.model = None
        self.preprocessor = None
        self.server = None
        self.server_thread = None
        self.logger = logging.getLogger("sbyb.deployment.serving")
    
    def load_model(self, model_path: str) -> None:
        """
        Load a model from a file.
        
        Args:
            model_path: Path to the model file.
        """
        try:
            with open(model_path, 'rb') as f:
                loaded_obj = pickle.load(f)
            
            # Check if the loaded object is a dictionary with model and metadata
            if isinstance(loaded_obj, dict) and 'model' in loaded_obj:
                self.model = loaded_obj['model']
                self.metadata = loaded_obj.get('metadata', {})
            else:
                # Assume the loaded object is the model itself
                self.model = loaded_obj
                self.metadata = {}
            
            self.logger.info(f"Model loaded from {model_path}")
        except Exception as e:
            raise ServingError(f"Failed to load model from {model_path}: {str(e)}")
    
    def load_preprocessor(self, preprocessor_path: str) -> None:
        """
        Load a preprocessor from a file.
        
        Args:
            preprocessor_path: Path to the preprocessor file.
        """
        try:
            with open(preprocessor_path, 'rb') as f:
                loaded_obj = pickle.load(f)
            
            # Check if the loaded object is a dictionary with preprocessor and metadata
            if isinstance(loaded_obj, dict) and 'preprocessor' in loaded_obj:
                self.preprocessor = loaded_obj['preprocessor']
            else:
                # Assume the loaded object is the preprocessor itself
                self.preprocessor = loaded_obj
            
            self.logger.info(f"Preprocessor loaded from {preprocessor_path}")
        except Exception as e:
            raise ServingError(f"Failed to load preprocessor from {preprocessor_path}: {str(e)}")
    
    def predict(self, data: Union[pd.DataFrame, np.ndarray, Dict[str, Any], List[Dict[str, Any]]]) -> np.ndarray:
        """
        Make predictions with the loaded model.
        
        Args:
            data: Input data for prediction.
            
        Returns:
            Model predictions.
        """
        if self.model is None:
            raise ServingError("No model loaded. Call load_model() first.")
        
        # Convert input data to appropriate format
        if isinstance(data, dict):
            # Single instance as dictionary
            data = pd.DataFrame([data])
        elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # List of dictionaries
            data = pd.DataFrame(data)
        elif isinstance(data, np.ndarray):
            # NumPy array
            pass
        elif not isinstance(data, pd.DataFrame):
            # Unsupported format
            raise ServingError(f"Unsupported data format: {type(data)}")
        
        # Apply preprocessor if available
        if self.preprocessor is not None:
            try:
                data = self.preprocessor.transform(data)
            except Exception as e:
                raise ServingError(f"Error applying preprocessor: {str(e)}")
        
        # Make predictions
        try:
            predictions = self.model.predict(data)
            return predictions
        except Exception as e:
            raise ServingError(f"Error making predictions: {str(e)}")
    
    def predict_proba(self, data: Union[pd.DataFrame, np.ndarray, Dict[str, Any], List[Dict[str, Any]]]) -> np.ndarray:
        """
        Make probability predictions with the loaded model.
        
        Args:
            data: Input data for prediction.
            
        Returns:
            Probability predictions.
        """
        if self.model is None:
            raise ServingError("No model loaded. Call load_model() first.")
        
        if not hasattr(self.model, 'predict_proba'):
            raise ServingError("Model does not support probability predictions.")
        
        # Convert input data to appropriate format
        if isinstance(data, dict):
            # Single instance as dictionary
            data = pd.DataFrame([data])
        elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # List of dictionaries
            data = pd.DataFrame(data)
        elif isinstance(data, np.ndarray):
            # NumPy array
            pass
        elif not isinstance(data, pd.DataFrame):
            # Unsupported format
            raise ServingError(f"Unsupported data format: {type(data)}")
        
        # Apply preprocessor if available
        if self.preprocessor is not None:
            try:
                data = self.preprocessor.transform(data)
            except Exception as e:
                raise ServingError(f"Error applying preprocessor: {str(e)}")
        
        # Make probability predictions
        try:
            probabilities = self.model.predict_proba(data)
            return probabilities
        except Exception as e:
            raise ServingError(f"Error making probability predictions: {str(e)}")
    
    def start_http_server(self, host: str = '0.0.0.0', port: int = 8000) -> None:
        """
        Start an HTTP server for model serving.
        
        Args:
            host: Host address to bind the server.
            port: Port to bind the server.
        """
        if self.model is None:
            raise ServingError("No model loaded. Call load_model() first.")
        
        # Create request handler
        model_server = self
        
        class ModelHTTPHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                if self.path == '/predict':
                    # Get content length
                    content_length = int(self.headers['Content-Length'])
                    # Read request body
                    post_data = self.rfile.read(content_length)
                    
                    try:
                        # Parse JSON data
                        data = json.loads(post_data.decode('utf-8'))
                        
                        # Make predictions
                        predictions = model_server.predict(data)
                        
                        # Convert predictions to list
                        if isinstance(predictions, np.ndarray):
                            predictions = predictions.tolist()
                        
                        # Create response
                        response = {
                            'predictions': predictions
                        }
                        
                        # Send response
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                    except Exception as e:
                        # Send error response
                        self.send_response(400)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                
                elif self.path == '/predict_proba':
                    # Get content length
                    content_length = int(self.headers['Content-Length'])
                    # Read request body
                    post_data = self.rfile.read(content_length)
                    
                    try:
                        # Parse JSON data
                        data = json.loads(post_data.decode('utf-8'))
                        
                        # Make probability predictions
                        probabilities = model_server.predict_proba(data)
                        
                        # Convert predictions to list
                        if isinstance(probabilities, np.ndarray):
                            probabilities = probabilities.tolist()
                        
                        # Create response
                        response = {
                            'probabilities': probabilities
                        }
                        
                        # Send response
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                    except Exception as e:
                        # Send error response
                        self.send_response(400)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                
                else:
                    # Unknown endpoint
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode('utf-8'))
            
            def do_GET(self):
                if self.path == '/health':
                    # Health check endpoint
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'healthy'}).encode('utf-8'))
                
                elif self.path == '/metadata':
                    # Metadata endpoint
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    
                    # Convert numpy arrays and other non-serializable objects to strings
                    metadata = {}
                    for key, value in model_server.metadata.items():
                        if isinstance(value, np.ndarray):
                            metadata[key] = value.tolist()
                        elif isinstance(value, (pd.DataFrame, pd.Series)):
                            metadata[key] = value.to_dict()
                        else:
                            try:
                                # Try to serialize, if it fails, convert to string
                                json.dumps({key: value})
                                metadata[key] = value
                            except (TypeError, OverflowError):
                                metadata[key] = str(value)
                    
                    self.wfile.write(json.dumps(metadata).encode('utf-8'))
                
                else:
                    # Unknown endpoint
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode('utf-8'))
        
        # Create server
        try:
            self.server = HTTPServer((host, port), ModelHTTPHandler)
            
            # Start server in a separate thread
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.logger.info(f"HTTP server started at http://{host}:{port}")
            print(f"HTTP server started at http://{host}:{port}")
            print(f"Available endpoints:")
            print(f"  - POST /predict: Make predictions")
            print(f"  - POST /predict_proba: Make probability predictions")
            print(f"  - GET /health: Health check")
            print(f"  - GET /metadata: Get model metadata")
        except Exception as e:
            raise ServingError(f"Failed to start HTTP server: {str(e)}")
    
    def stop_http_server(self) -> None:
        """
        Stop the HTTP server.
        """
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
            self.server_thread = None
            self.logger.info("HTTP server stopped")
            print("HTTP server stopped")
    
    def start_grpc_server(self, host: str = '0.0.0.0', port: int = 50051) -> None:
        """
        Start a gRPC server for model serving.
        
        Args:
            host: Host address to bind the server.
            port: Port to bind the server.
        """
        try:
            import grpc
            from concurrent import futures
        except ImportError:
            raise ServingError("gRPC server requires grpc. "
                              "Please install it with 'pip install grpcio grpcio-tools'.")
        
        if self.model is None:
            raise ServingError("No model loaded. Call load_model() first.")
        
        # This is a simplified implementation that would need to be expanded
        # with proper protobuf definitions for a real-world application
        self.logger.info(f"gRPC server functionality is a placeholder. "
                        f"For a complete implementation, define protobuf messages and services.")
        print(f"gRPC server functionality is a placeholder. "
             f"For a complete implementation, define protobuf messages and services.")
    
    def serve_flask(self, host: str = '0.0.0.0', port: int = 5000) -> None:
        """
        Serve the model using Flask.
        
        Args:
            host: Host address to bind the server.
            port: Port to bind the server.
        """
        try:
            from flask import Flask, request, jsonify
        except ImportError:
            raise ServingError("Flask server requires flask. "
                              "Please install it with 'pip install flask'.")
        
        if self.model is None:
            raise ServingError("No model loaded. Call load_model() first.")
        
        # Create Flask app
        app = Flask("SBYB Model Server")
        model_server = self
        
        @app.route('/predict', methods=['POST'])
        def predict():
            try:
                # Get data from request
                data = request.json
                
                # Make predictions
                predictions = model_server.predict(data)
                
                # Convert predictions to list
                if isinstance(predictions, np.ndarray):
                    predictions = predictions.tolist()
                
                # Return predictions
                return jsonify({'predictions': predictions})
            except Exception as e:
                return jsonify({'error': str(e)}), 400
        
        @app.route('/predict_proba', methods=['POST'])
        def predict_proba():
            try:
                # Get data from request
                data = request.json
                
                # Make probability predictions
                probabilities = model_server.predict_proba(data)
                
                # Convert predictions to list
                if isinstance(probabilities, np.ndarray):
                    probabilities = probabilities.tolist()
                
                # Return probabilities
                return jsonify({'probabilities': probabilities})
            except Exception as e:
                return jsonify({'error': str(e)}), 400
        
        @app.route('/health', methods=['GET'])
        def health():
            return jsonify({'status': 'healthy'})
        
        @app.route('/metadata', methods=['GET'])
        def metadata():
            # Convert numpy arrays and other non-serializable objects to strings
            metadata_dict = {}
            for key, value in model_server.metadata.items():
                if isinstance(value, np.ndarray):
                    metadata_dict[key] = value.tolist()
                elif isinstance(value, (pd.DataFrame, pd.Series)):
                    metadata_dict[key] = value.to_dict()
                else:
                    try:
                        # Try to serialize, if it fails, convert to string
                        json.dumps({key: value})
                        metadata_dict[key] = value
                    except (TypeError, OverflowError):
                        metadata_dict[key] = str(value)
            
            return jsonify(metadata_dict)
        
        # Start Flask app
        print(f"Starting Flask server at http://{host}:{port}")
        print(f"Available endpoints:")
        print(f"  - POST /predict: Make predictions")
        print(f"  - POST /predict_proba: Make probability predictions")
        print(f"  - GET /health: Health check")
        print(f"  - GET /metadata: Get model metadata")
        
        app.run(host=host, port=port)
    
    def serve_fastapi(self, host: str = '0.0.0.0', port: int = 8000) -> None:
        """
        Serve the model using FastAPI.
        
        Args:
            host: Host address to bind the server.
            port: Port to bind the server.
        """
        try:
            import uvicorn
            from fastapi import FastAPI, HTTPException
            from pydantic import BaseModel
        except ImportError:
            raise ServingError("FastAPI server requires fastapi and uvicorn. "
                              "Please install them with 'pip install fastapi uvicorn'.")
        
        if self.model is None:
            raise ServingError("No model loaded. Call load_model() first.")
        
        # Create FastAPI app
        app = FastAPI(title="SBYB Model Server", description="API for serving machine learning models")
        model_server = self
        
        # Define request and response models
        class PredictionRequest(BaseModel):
            data: List[Dict[str, Any]]
        
        class PredictionResponse(BaseModel):
            predictions: List[Any]
        
        class ProbabilityResponse(BaseModel):
            probabilities: List[List[float]]
        
        @app.post("/predict", response_model=PredictionResponse)
        async def predict(request: PredictionRequest):
            try:
                # Make predictions
                predictions = model_server.predict(request.data)
                
                # Convert predictions to list
                if isinstance(predictions, np.ndarray):
                    predictions = predictions.tolist()
                
                # Return predictions
                return {"predictions": predictions}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        @app.post("/predict_proba", response_model=ProbabilityResponse)
        async def predict_proba(request: PredictionRequest):
            try:
                # Make probability predictions
                probabilities = model_server.predict_proba(request.data)
                
                # Convert predictions to list
                if isinstance(probabilities, np.ndarray):
                    probabilities = probabilities.tolist()
                
                # Return probabilities
                return {"probabilities": probabilities}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        @app.get("/health")
        async def health():
            return {"status": "healthy"}
        
        @app.get("/metadata")
        async def metadata():
            # Convert numpy arrays and other non-serializable objects to strings
            metadata_dict = {}
            for key, value in model_server.metadata.items():
                if isinstance(value, np.ndarray):
                    metadata_dict[key] = value.tolist()
                elif isinstance(value, (pd.DataFrame, pd.Series)):
                    metadata_dict[key] = value.to_dict()
                else:
                    try:
                        # Try to serialize, if it fails, convert to string
                        json.dumps({key: value})
                        metadata_dict[key] = value
                    except (TypeError, OverflowError):
                        metadata_dict[key] = str(value)
            
            return metadata_dict
        
        # Start FastAPI app
        print(f"Starting FastAPI server at http://{host}:{port}")
        print(f"Available endpoints:")
        print(f"  - POST /predict: Make predictions")
        print(f"  - POST /predict_proba: Make probability predictions")
        print(f"  - GET /health: Health check")
        print(f"  - GET /metadata: Get model metadata")
        print(f"  - GET /docs: API documentation")
        
        uvicorn.run(app, host=host, port=port)
