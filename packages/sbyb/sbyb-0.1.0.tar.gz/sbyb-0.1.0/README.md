# SBYB - Step-By-Your-Byte

A comprehensive machine learning library that unifies the entire ML pipeline.

## Overview

SBYB (Step-By-Your-Byte) is a Python library designed to provide a unified, offline-capable machine learning toolkit that outperforms existing solutions like TensorFlow and Keras. It integrates the entire ML pipeline from data preprocessing to model deployment in a single, cohesive package.

## Key Features

- **Unified Data Preprocessing**: Automatic handling of missing values, outliers, encoding, and scaling
- **Task Type & Data Type Auto-detection**: Intelligent identification of ML tasks and data characteristics
- **AutoML Engine**: Automated model selection, hyperparameter tuning, and ensemble creation
- **Evaluation & Explainability**: Comprehensive metrics and model interpretation tools
- **Deployment & Serving**: Easy model export and deployment options
- **Zero-code UI Generation**: Automatic creation of user interfaces for models
- **Project Scaffolding**: Quick setup of new ML projects with best practices
- **EDA Tools**: Powerful data profiling and visualization capabilities
- **Plugin System**: Extensible architecture for custom components
- **Local Experiment Tracking**: Track, compare, and visualize ML experiments
- **CLI & Programmatic API**: Multiple interfaces for different workflows

## Installation

```bash
pip install sbyb
```

## Quick Start

### Using the CLI

```bash
# Create a new project
sbyb project create --name my_project --template classification

# Run AutoML on a dataset
sbyb automl run --data data.csv --target target_column

# Generate a UI for a model
sbyb ui generate --model model.pkl --output ui_app
```

### Using the API

```python
from sbyb.api import SBYB

# Initialize SBYB
sbyb = SBYB()

# Preprocess data
import pandas as pd
data = pd.read_csv("data.csv")
preprocessed_data = sbyb.preprocess_data(data)

# Run AutoML
result = sbyb.run_automl(
    data=preprocessed_data,
    target="target_column",
    output_dir="output"
)

# Generate UI
sbyb.generate_ui(
    model=result.model,
    output_dir="ui_app",
    ui_type="dashboard",
    framework="streamlit"
)
```

## Documentation

For detailed documentation, visit [https://sbyb.readthedocs.io/](https://sbyb.readthedocs.io/)

## License

MIT License
