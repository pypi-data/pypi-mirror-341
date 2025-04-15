"""
API generator component for SBYB deployment.

This module provides functionality for automatically generating APIs
for machine learning models.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import shutil
import subprocess
import tempfile

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import APIGenerationError


class APIGenerator(SBYBComponent):
    """
    API generator component.
    
    This component generates APIs for machine learning models.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the API generator.
        
        Args:
            config: Configuration dictionary for the generator.
        """
        super().__init__(config)
    
    def generate_fastapi(self, model_path: str, output_dir: str, 
                        api_name: str = "model_api",
                        host: str = "0.0.0.0", 
                        port: int = 8000,
                        include_docs: bool = True,
                        include_preprocessing: bool = False,
                        preprocessor_path: Optional[str] = None) -> str:
        """
        Generate a FastAPI application for serving a model.
        
        Args:
            model_path: Path to the model file.
            output_dir: Directory to save the generated API.
            api_name: Name of the API.
            host: Host address to bind the server.
            port: Port to bind the server.
            include_docs: Whether to include API documentation.
            include_preprocessing: Whether to include preprocessing.
            preprocessor_path: Path to the preprocessor file.
            
        Returns:
            Path to the generated API.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create main.py
        main_py_content = self._generate_fastapi_main(
            model_path=model_path,
            api_name=api_name,
            host=host,
            port=port,
            include_docs=include_docs,
            include_preprocessing=include_preprocessing,
            preprocessor_path=preprocessor_path
        )
        
        with open(os.path.join(output_dir, "main.py"), "w") as f:
            f.write(main_py_content)
        
        # Create requirements.txt
        requirements_txt_content = self._generate_fastapi_requirements()
        
        with open(os.path.join(output_dir, "requirements.txt"), "w") as f:
            f.write(requirements_txt_content)
        
        # Create README.md
        readme_md_content = self._generate_fastapi_readme(
            api_name=api_name,
            host=host,
            port=port
        )
        
        with open(os.path.join(output_dir, "README.md"), "w") as f:
            f.write(readme_md_content)
        
        # Create Dockerfile
        dockerfile_content = self._generate_fastapi_dockerfile()
        
        with open(os.path.join(output_dir, "Dockerfile"), "w") as f:
            f.write(dockerfile_content)
        
        # Create .dockerignore
        dockerignore_content = self._generate_dockerignore()
        
        with open(os.path.join(output_dir, ".dockerignore"), "w") as f:
            f.write(dockerignore_content)
        
        # Copy model file to output directory
        model_filename = os.path.basename(model_path)
        shutil.copy(model_path, os.path.join(output_dir, model_filename))
        
        # Copy preprocessor file to output directory if provided
        if include_preprocessing and preprocessor_path is not None:
            preprocessor_filename = os.path.basename(preprocessor_path)
            shutil.copy(preprocessor_path, os.path.join(output_dir, preprocessor_filename))
        
        return output_dir
    
    def generate_flask(self, model_path: str, output_dir: str, 
                      api_name: str = "model_api",
                      host: str = "0.0.0.0", 
                      port: int = 5000,
                      include_preprocessing: bool = False,
                      preprocessor_path: Optional[str] = None) -> str:
        """
        Generate a Flask application for serving a model.
        
        Args:
            model_path: Path to the model file.
            output_dir: Directory to save the generated API.
            api_name: Name of the API.
            host: Host address to bind the server.
            port: Port to bind the server.
            include_preprocessing: Whether to include preprocessing.
            preprocessor_path: Path to the preprocessor file.
            
        Returns:
            Path to the generated API.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create app.py
        app_py_content = self._generate_flask_app(
            model_path=model_path,
            api_name=api_name,
            host=host,
            port=port,
            include_preprocessing=include_preprocessing,
            preprocessor_path=preprocessor_path
        )
        
        with open(os.path.join(output_dir, "app.py"), "w") as f:
            f.write(app_py_content)
        
        # Create requirements.txt
        requirements_txt_content = self._generate_flask_requirements()
        
        with open(os.path.join(output_dir, "requirements.txt"), "w") as f:
            f.write(requirements_txt_content)
        
        # Create README.md
        readme_md_content = self._generate_flask_readme(
            api_name=api_name,
            host=host,
            port=port
        )
        
        with open(os.path.join(output_dir, "README.md"), "w") as f:
            f.write(readme_md_content)
        
        # Create Dockerfile
        dockerfile_content = self._generate_flask_dockerfile()
        
        with open(os.path.join(output_dir, "Dockerfile"), "w") as f:
            f.write(dockerfile_content)
        
        # Create .dockerignore
        dockerignore_content = self._generate_dockerignore()
        
        with open(os.path.join(output_dir, ".dockerignore"), "w") as f:
            f.write(dockerignore_content)
        
        # Copy model file to output directory
        model_filename = os.path.basename(model_path)
        shutil.copy(model_path, os.path.join(output_dir, model_filename))
        
        # Copy preprocessor file to output directory if provided
        if include_preprocessing and preprocessor_path is not None:
            preprocessor_filename = os.path.basename(preprocessor_path)
            shutil.copy(preprocessor_path, os.path.join(output_dir, preprocessor_filename))
        
        return output_dir
    
    def generate_streamlit(self, model_path: str, output_dir: str, 
                          app_name: str = "Model Demo",
                          port: int = 8501,
                          include_preprocessing: bool = False,
                          preprocessor_path: Optional[str] = None,
                          include_visualization: bool = True) -> str:
        """
        Generate a Streamlit application for demonstrating a model.
        
        Args:
            model_path: Path to the model file.
            output_dir: Directory to save the generated application.
            app_name: Name of the application.
            port: Port to bind the server.
            include_preprocessing: Whether to include preprocessing.
            preprocessor_path: Path to the preprocessor file.
            include_visualization: Whether to include visualization.
            
        Returns:
            Path to the generated application.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create app.py
        app_py_content = self._generate_streamlit_app(
            model_path=model_path,
            app_name=app_name,
            include_preprocessing=include_preprocessing,
            preprocessor_path=preprocessor_path,
            include_visualization=include_visualization
        )
        
        with open(os.path.join(output_dir, "app.py"), "w") as f:
            f.write(app_py_content)
        
        # Create requirements.txt
        requirements_txt_content = self._generate_streamlit_requirements()
        
        with open(os.path.join(output_dir, "requirements.txt"), "w") as f:
            f.write(requirements_txt_content)
        
        # Create README.md
        readme_md_content = self._generate_streamlit_readme(
            app_name=app_name,
            port=port
        )
        
        with open(os.path.join(output_dir, "README.md"), "w") as f:
            f.write(readme_md_content)
        
        # Create Dockerfile
        dockerfile_content = self._generate_streamlit_dockerfile()
        
        with open(os.path.join(output_dir, "Dockerfile"), "w") as f:
            f.write(dockerfile_content)
        
        # Create .dockerignore
        dockerignore_content = self._generate_dockerignore()
        
        with open(os.path.join(output_dir, ".dockerignore"), "w") as f:
            f.write(dockerignore_content)
        
        # Copy model file to output directory
        model_filename = os.path.basename(model_path)
        shutil.copy(model_path, os.path.join(output_dir, model_filename))
        
        # Copy preprocessor file to output directory if provided
        if include_preprocessing and preprocessor_path is not None:
            preprocessor_filename = os.path.basename(preprocessor_path)
            shutil.copy(preprocessor_path, os.path.join(output_dir, preprocessor_filename))
        
        return output_dir
    
    def _generate_fastapi_main(self, model_path: str, api_name: str, host: str, port: int,
                              include_docs: bool, include_preprocessing: bool,
                              preprocessor_path: Optional[str]) -> str:
        """
        Generate FastAPI main.py content.
        
        Args:
            model_path: Path to the model file.
            api_name: Name of the API.
            host: Host address to bind the server.
            port: Port to bind the server.
            include_docs: Whether to include API documentation.
            include_preprocessing: Whether to include preprocessing.
            preprocessor_path: Path to the preprocessor file.
            
        Returns:
            Content of main.py.
        """
        model_filename = os.path.basename(model_path)
        preprocessor_filename = os.path.basename(preprocessor_path) if preprocessor_path else None
        
        content = f"""
import os
import pickle
import json
from typing import List, Dict, Any, Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="{api_name}",
    description="API for serving machine learning model",
    version="1.0.0",
    {"openapi_url=None" if not include_docs else ""}
)

# Load model
try:
    with open("{model_filename}", "rb") as f:
        loaded_obj = pickle.load(f)
    
    # Check if the loaded object is a dictionary with model and metadata
    if isinstance(loaded_obj, dict) and 'model' in loaded_obj:
        model = loaded_obj['model']
        metadata = loaded_obj.get('metadata', {{}})
    else:
        # Assume the loaded object is the model itself
        model = loaded_obj
        metadata = {{}}
    
    print(f"Model loaded from {model_filename}")
except Exception as e:
    print(f"Error loading model: {{e}}")
    raise
"""
        
        if include_preprocessing and preprocessor_path:
            content += f"""
# Load preprocessor
try:
    with open("{preprocessor_filename}", "rb") as f:
        loaded_obj = pickle.load(f)
    
    # Check if the loaded object is a dictionary with preprocessor and metadata
    if isinstance(loaded_obj, dict) and 'preprocessor' in loaded_obj:
        preprocessor = loaded_obj['preprocessor']
    else:
        # Assume the loaded object is the preprocessor itself
        preprocessor = loaded_obj
    
    print(f"Preprocessor loaded from {preprocessor_filename}")
except Exception as e:
    print(f"Error loading preprocessor: {{e}}")
    preprocessor = None
"""
        else:
            content += """
# No preprocessor
preprocessor = None
"""
        
        content += """
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
        # Convert input data to DataFrame
        data = pd.DataFrame(request.data)
        
        # Apply preprocessor if available
        if preprocessor is not None:
            try:
                data = preprocessor.transform(data)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error applying preprocessor: {str(e)}")
        
        # Make predictions
        predictions = model.predict(data)
        
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
        # Check if model supports probability predictions
        if not hasattr(model, 'predict_proba'):
            raise HTTPException(status_code=400, detail="Model does not support probability predictions")
        
        # Convert input data to DataFrame
        data = pd.DataFrame(request.data)
        
        # Apply preprocessor if available
        if preprocessor is not None:
            try:
                data = preprocessor.transform(data)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error applying preprocessor: {str(e)}")
        
        # Make probability predictions
        probabilities = model.predict_proba(data)
        
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
async def get_metadata():
    # Convert numpy arrays and other non-serializable objects to strings
    metadata_dict = {}
    for key, value in metadata.items():
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="{host}", port={port}, reload=False)
"""
        
        return content
    
    def _generate_fastapi_requirements(self) -> str:
        """
        Generate FastAPI requirements.txt content.
        
        Returns:
            Content of requirements.txt.
        """
        return """
fastapi>=0.68.0
uvicorn>=0.15.0
pandas>=1.3.0
numpy>=1.20.0
scikit-learn>=0.24.0
pydantic>=1.8.0
python-multipart>=0.0.5
"""
    
    def _generate_fastapi_readme(self, api_name: str, host: str, port: int) -> str:
        """
        Generate FastAPI README.md content.
        
        Args:
            api_name: Name of the API.
            host: Host address to bind the server.
            port: Port to bind the server.
            
        Returns:
            Content of README.md.
        """
        return f"""
# {api_name}

This is a FastAPI application for serving a machine learning model.

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the API

```
python main.py
```

The API will be available at http://{host}:{port}

### API Endpoints

- `POST /predict`: Make predictions
  - Request body: `{{"data": [{{"feature1": value1, "feature2": value2, ...}}, ...]}}`
  - Response: `{{"predictions": [prediction1, prediction2, ...]}}`

- `POST /predict_proba`: Make probability predictions (if supported by the model)
  - Request body: `{{"data": [{{"feature1": value1, "feature2": value2, ...}}, ...]}}`
  - Response: `{{"probabilities": [[prob1_class1, prob1_class2, ...], [prob2_class1, prob2_class2, ...], ...]}}`

- `GET /health`: Health check
  - Response: `{{"status": "healthy"}}`

- `GET /metadata`: Get model metadata
  - Response: Model metadata

### API Documentation

API documentation is available at http://{host}:{port}/docs

## Docker

You can also run the API using Docker:

```
docker build -t {api_name.lower().replace(" ", "-")} .
docker run -p {port}:{port} {api_name.lower().replace(" ", "-")}
```
"""
    
    def _generate_fastapi_dockerfile(self) -> str:
        """
        Generate FastAPI Dockerfile content.
        
        Returns:
            Content of Dockerfile.
        """
        return """
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
"""
    
    def _generate_flask_app(self, model_path: str, api_name: str, host: str, port: int,
                           include_preprocessing: bool, preprocessor_path: Optional[str]) -> str:
        """
        Generate Flask app.py content.
        
        Args:
            model_path: Path to the model file.
            api_name: Name of the API.
            host: Host address to bind the server.
            port: Port to bind the server.
            include_preprocessing: Whether to include preprocessing.
            preprocessor_path: Path to the preprocessor file.
            
        Returns:
            Content of app.py.
        """
        model_filename = os.path.basename(model_path)
        preprocessor_filename = os.path.basename(preprocessor_path) if preprocessor_path else None
        
        content = f"""
import os
import pickle
import json

import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

# Create Flask app
app = Flask("{api_name}")

# Load model
try:
    with open("{model_filename}", "rb") as f:
        loaded_obj = pickle.load(f)
    
    # Check if the loaded object is a dictionary with model and metadata
    if isinstance(loaded_obj, dict) and 'model' in loaded_obj:
        model = loaded_obj['model']
        metadata = loaded_obj.get('metadata', {{}})
    else:
        # Assume the loaded object is the model itself
        model = loaded_obj
        metadata = {{}}
    
    print(f"Model loaded from {model_filename}")
except Exception as e:
    print(f"Error loading model: {{e}}")
    raise
"""
        
        if include_preprocessing and preprocessor_path:
            content += f"""
# Load preprocessor
try:
    with open("{preprocessor_filename}", "rb") as f:
        loaded_obj = pickle.load(f)
    
    # Check if the loaded object is a dictionary with preprocessor and metadata
    if isinstance(loaded_obj, dict) and 'preprocessor' in loaded_obj:
        preprocessor = loaded_obj['preprocessor']
    else:
        # Assume the loaded object is the preprocessor itself
        preprocessor = loaded_obj
    
    print(f"Preprocessor loaded from {preprocessor_filename}")
except Exception as e:
    print(f"Error loading preprocessor: {{e}}")
    preprocessor = None
"""
        else:
            content += """
# No preprocessor
preprocessor = None
"""
        
        content += """
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.json
        
        # Convert to DataFrame if it's a list of dictionaries
        if isinstance(data, list):
            data = pd.DataFrame(data)
        
        # Apply preprocessor if available
        if preprocessor is not None:
            try:
                data = preprocessor.transform(data)
            except Exception as e:
                return jsonify({'error': f"Error applying preprocessor: {str(e)}"}), 400
        
        # Make predictions
        predictions = model.predict(data)
        
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
        # Check if model supports probability predictions
        if not hasattr(model, 'predict_proba'):
            return jsonify({'error': 'Model does not support probability predictions'}), 400
        
        # Get data from request
        data = request.json
        
        # Convert to DataFrame if it's a list of dictionaries
        if isinstance(data, list):
            data = pd.DataFrame(data)
        
        # Apply preprocessor if available
        if preprocessor is not None:
            try:
                data = preprocessor.transform(data)
            except Exception as e:
                return jsonify({'error': f"Error applying preprocessor: {str(e)}"}), 400
        
        # Make probability predictions
        probabilities = model.predict_proba(data)
        
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
def get_metadata():
    # Convert numpy arrays and other non-serializable objects to strings
    metadata_dict = {}
    for key, value in metadata.items():
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

if __name__ == '__main__':
    app.run(host='{host}', port={port})
"""
        
        return content
    
    def _generate_flask_requirements(self) -> str:
        """
        Generate Flask requirements.txt content.
        
        Returns:
            Content of requirements.txt.
        """
        return """
flask>=2.0.0
pandas>=1.3.0
numpy>=1.20.0
scikit-learn>=0.24.0
"""
    
    def _generate_flask_readme(self, api_name: str, host: str, port: int) -> str:
        """
        Generate Flask README.md content.
        
        Args:
            api_name: Name of the API.
            host: Host address to bind the server.
            port: Port to bind the server.
            
        Returns:
            Content of README.md.
        """
        return f"""
# {api_name}

This is a Flask application for serving a machine learning model.

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the API

```
python app.py
```

The API will be available at http://{host}:{port}

### API Endpoints

- `POST /predict`: Make predictions
  - Request body: `[{{"feature1": value1, "feature2": value2, ...}}, ...]`
  - Response: `{{"predictions": [prediction1, prediction2, ...]}}`

- `POST /predict_proba`: Make probability predictions (if supported by the model)
  - Request body: `[{{"feature1": value1, "feature2": value2, ...}}, ...]`
  - Response: `{{"probabilities": [[prob1_class1, prob1_class2, ...], [prob2_class1, prob2_class2, ...], ...]}}`

- `GET /health`: Health check
  - Response: `{{"status": "healthy"}}`

- `GET /metadata`: Get model metadata
  - Response: Model metadata

## Docker

You can also run the API using Docker:

```
docker build -t {api_name.lower().replace(" ", "-")} .
docker run -p {port}:{port} {api_name.lower().replace(" ", "-")}
```
"""
    
    def _generate_flask_dockerfile(self) -> str:
        """
        Generate Flask Dockerfile content.
        
        Returns:
            Content of Dockerfile.
        """
        return """
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
"""
    
    def _generate_streamlit_app(self, model_path: str, app_name: str,
                               include_preprocessing: bool, preprocessor_path: Optional[str],
                               include_visualization: bool) -> str:
        """
        Generate Streamlit app.py content.
        
        Args:
            model_path: Path to the model file.
            app_name: Name of the application.
            include_preprocessing: Whether to include preprocessing.
            preprocessor_path: Path to the preprocessor file.
            include_visualization: Whether to include visualization.
            
        Returns:
            Content of app.py.
        """
        model_filename = os.path.basename(model_path)
        preprocessor_filename = os.path.basename(preprocessor_path) if preprocessor_path else None
        
        content = f"""
import os
import pickle
import json

import numpy as np
import pandas as pd
import streamlit as st
"""
        
        if include_visualization:
            content += """
import matplotlib.pyplot as plt
import seaborn as sns
"""
        
        content += f"""
# Set page title
st.set_page_config(page_title="{app_name}", layout="wide")

# App title
st.title("{app_name}")

# Load model
@st.cache_resource
def load_model():
    try:
        with open("{model_filename}", "rb") as f:
            loaded_obj = pickle.load(f)
        
        # Check if the loaded object is a dictionary with model and metadata
        if isinstance(loaded_obj, dict) and 'model' in loaded_obj:
            model = loaded_obj['model']
            metadata = loaded_obj.get('metadata', {{}})
        else:
            # Assume the loaded object is the model itself
            model = loaded_obj
            metadata = {{}}
        
        return model, metadata
    except Exception as e:
        st.error(f"Error loading model: {{e}}")
        return None, {{}}

model, metadata = load_model()
"""
        
        if include_preprocessing and preprocessor_path:
            content += f"""
# Load preprocessor
@st.cache_resource
def load_preprocessor():
    try:
        with open("{preprocessor_filename}", "rb") as f:
            loaded_obj = pickle.load(f)
        
        # Check if the loaded object is a dictionary with preprocessor and metadata
        if isinstance(loaded_obj, dict) and 'preprocessor' in loaded_obj:
            preprocessor = loaded_obj['preprocessor']
        else:
            # Assume the loaded object is the preprocessor itself
            preprocessor = loaded_obj
        
        return preprocessor
    except Exception as e:
        st.error(f"Error loading preprocessor: {{e}}")
        return None

preprocessor = load_preprocessor()
"""
        else:
            content += """
# No preprocessor
preprocessor = None
"""
        
        content += """
# Sidebar
st.sidebar.header("Model Information")

# Display model type
model_type = type(model).__name__
st.sidebar.write(f"**Model Type:** {model_type}")

# Display model parameters
st.sidebar.write("**Model Parameters:**")
if hasattr(model, 'get_params'):
    params = model.get_params()
    for param, value in params.items():
        st.sidebar.write(f"- {param}: {value}")

# Display metadata
if metadata:
    st.sidebar.write("**Model Metadata:**")
    for key, value in metadata.items():
        if not isinstance(value, (dict, list, np.ndarray, pd.DataFrame, pd.Series)):
            st.sidebar.write(f"- {key}: {value}")

# Main content
st.header("Make Predictions")

# Input method selection
input_method = st.radio("Select input method:", ["Manual Input", "Upload CSV"])

if input_method == "Manual Input":
    # Get feature names
    if hasattr(model, 'feature_names_in_'):
        feature_names = model.feature_names_in_
    elif 'feature_names' in metadata:
        feature_names = metadata['feature_names']
    else:
        # Ask user for feature names
        feature_names_input = st.text_input("Enter feature names (comma-separated):")
        feature_names = [name.strip() for name in feature_names_input.split(',')] if feature_names_input else []
    
    # Create input fields for each feature
    input_data = {}
    
    if feature_names:
        st.subheader("Enter feature values:")
        cols = st.columns(2)
        for i, feature in enumerate(feature_names):
            input_data[feature] = cols[i % 2].number_input(f"{feature}", value=0.0, key=f"feature_{i}")
    else:
        st.warning("No feature names available. Please upload a CSV file instead.")
    
    # Make prediction button
    if feature_names and st.button("Predict"):
        # Create DataFrame from input
        input_df = pd.DataFrame([input_data])
        
        # Apply preprocessor if available
        if preprocessor is not None:
            try:
                input_df = preprocessor.transform(input_df)
            except Exception as e:
                st.error(f"Error applying preprocessor: {e}")
        
        # Make prediction
        try:
            prediction = model.predict(input_df)
            st.success(f"Prediction: {prediction[0]}")
            
            # Show probability if available
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(input_df)
                st.write("Prediction probabilities:")
                
                # Get class names if available
                if hasattr(model, 'classes_'):
                    class_names = model.classes_
                    prob_df = pd.DataFrame([probabilities[0]], columns=class_names)
                else:
                    prob_df = pd.DataFrame([probabilities[0]], columns=[f"Class {i}" for i in range(probabilities.shape[1])])
                
                st.dataframe(prob_df)
"""
        
        if include_visualization:
            content += """
                # Visualize probabilities
                if hasattr(model, 'predict_proba'):
                    fig, ax = plt.subplots(figsize=(10, 4))
                    
                    # Get class names if available
                    if hasattr(model, 'classes_'):
                        class_names = model.classes_
                    else:
                        class_names = [f"Class {i}" for i in range(probabilities.shape[1])]
                    
                    # Plot probabilities
                    sns.barplot(x=class_names, y=probabilities[0], ax=ax)
                    ax.set_title("Prediction Probabilities")
                    ax.set_ylabel("Probability")
                    ax.set_xlabel("Class")
                    
                    # Rotate x-axis labels if there are many classes
                    if len(class_names) > 3:
                        plt.xticks(rotation=45, ha='right')
                    
                    st.pyplot(fig)
"""
        
        content += """
        except Exception as e:
            st.error(f"Error making prediction: {e}")

elif input_method == "Upload CSV":
    # File uploader
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read CSV
        try:
            input_df = pd.read_csv(uploaded_file)
            st.write("Preview of uploaded data:")
            st.dataframe(input_df.head())
            
            # Make prediction button
            if st.button("Predict"):
                # Apply preprocessor if available
                if preprocessor is not None:
                    try:
                        processed_df = preprocessor.transform(input_df)
                    except Exception as e:
                        st.error(f"Error applying preprocessor: {e}")
                        processed_df = input_df
                else:
                    processed_df = input_df
                
                # Make predictions
                try:
                    predictions = model.predict(processed_df)
                    
                    # Create results DataFrame
                    results_df = input_df.copy()
                    results_df['prediction'] = predictions
                    
                    # Add probabilities if available
                    if hasattr(model, 'predict_proba'):
                        probabilities = model.predict_proba(processed_df)
                        
                        # Get class names if available
                        if hasattr(model, 'classes_'):
                            class_names = model.classes_
                            for i, class_name in enumerate(class_names):
                                results_df[f"probability_{class_name}"] = probabilities[:, i]
                        else:
                            for i in range(probabilities.shape[1]):
                                results_df[f"probability_class_{i}"] = probabilities[:, i]
                    
                    st.success("Predictions completed!")
                    st.write("Results:")
                    st.dataframe(results_df)
                    
                    # Download button
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="Download results as CSV",
                        data=csv,
                        file_name="predictions.csv",
                        mime="text/csv"
                    )
"""
        
        if include_visualization:
            content += """
                    # Visualize predictions
                    st.subheader("Visualization")
                    
                    # Check if it's a classification problem
                    if hasattr(model, 'classes_'):
                        # Plot prediction distribution
                        fig, ax = plt.subplots(figsize=(10, 6))
                        prediction_counts = results_df['prediction'].value_counts().sort_index()
                        sns.barplot(x=prediction_counts.index, y=prediction_counts.values, ax=ax)
                        ax.set_title("Prediction Distribution")
                        ax.set_ylabel("Count")
                        ax.set_xlabel("Predicted Class")
                        
                        # Rotate x-axis labels if there are many classes
                        if len(prediction_counts) > 3:
                            plt.xticks(rotation=45, ha='right')
                        
                        st.pyplot(fig)
                    else:
                        # Regression problem
                        fig, ax = plt.subplots(figsize=(10, 6))
                        sns.histplot(predictions, kde=True, ax=ax)
                        ax.set_title("Prediction Distribution")
                        ax.set_xlabel("Predicted Value")
                        ax.set_ylabel("Count")
                        st.pyplot(fig)
"""
        
        content += """
                except Exception as e:
                    st.error(f"Error making predictions: {e}")
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")

# About section
st.sidebar.header("About")
st.sidebar.info(
    f"This is a Streamlit app for demonstrating the {app_name} model. "
    "It allows you to make predictions using the model either by manual input or by uploading a CSV file."
)
"""
        
        return content
    
    def _generate_streamlit_requirements(self) -> str:
        """
        Generate Streamlit requirements.txt content.
        
        Returns:
            Content of requirements.txt.
        """
        return """
streamlit>=1.10.0
pandas>=1.3.0
numpy>=1.20.0
scikit-learn>=0.24.0
matplotlib>=3.4.0
seaborn>=0.11.0
"""
    
    def _generate_streamlit_readme(self, app_name: str, port: int) -> str:
        """
        Generate Streamlit README.md content.
        
        Args:
            app_name: Name of the application.
            port: Port to bind the server.
            
        Returns:
            Content of README.md.
        """
        return f"""
# {app_name}

This is a Streamlit application for demonstrating a machine learning model.

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```
streamlit run app.py
```

The application will be available at http://localhost:{port}

### Features

- Make predictions using manual input or by uploading a CSV file
- View model information and parameters
- Visualize prediction results
- Download prediction results as CSV

## Docker

You can also run the application using Docker:

```
docker build -t {app_name.lower().replace(" ", "-")} .
docker run -p {port}:{port} {app_name.lower().replace(" ", "-")}
```
"""
    
    def _generate_streamlit_dockerfile(self) -> str:
        """
        Generate Streamlit Dockerfile content.
        
        Returns:
            Content of Dockerfile.
        """
        return """
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
"""
    
    def _generate_dockerignore(self) -> str:
        """
        Generate .dockerignore content.
        
        Returns:
            Content of .dockerignore.
        """
        return """
__pycache__/
*.py[cod]
*$py.class
.env
.venv
env/
venv/
ENV/
.git
.gitignore
.idea
.vscode
"""
