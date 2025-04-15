"""
Project generator for SBYB Scaffolding.

This module provides functionality to generate new ML project structures
with appropriate files, directories, and configurations.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import shutil
import datetime
import pkg_resources

from sbyb.core.base import SBYBComponent
from sbyb.core.config import Config
from sbyb.core.exceptions import ScaffoldingError


class ProjectGenerator(SBYBComponent):
    """
    Project generator for creating new ML project structures.
    
    This component provides functionality to generate new ML project structures
    with appropriate files, directories, and configurations.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the project generator.
        
        Args:
            config: Configuration dictionary for the project generator.
        """
        super().__init__(config)
        self.templates = {}
        self._load_default_templates()
    
    def _load_default_templates(self) -> None:
        """
        Load default project templates.
        """
        # Basic ML project template
        self.register_template(
            "basic",
            "Basic ML Project",
            {
                "description": "A basic machine learning project structure.",
                "directories": [
                    "data/raw",
                    "data/processed",
                    "data/external",
                    "models",
                    "notebooks",
                    "src",
                    "src/data",
                    "src/features",
                    "src/models",
                    "src/visualization",
                    "reports",
                    "reports/figures"
                ],
                "files": {
                    "README.md": """# {{ project_name }}

{{ project_description }}

## Project Organization

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment
    │
    ├── setup.py           <- Makes project pip installable (pip install -e .)
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── config.yaml        <- Configuration file for the project
""",
                    "LICENSE": """MIT License

Copyright (c) {% now 'utc', '%Y' %} {{ author_name }}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
                    "requirements.txt": """# External requirements
sbyb=={{ sbyb_version }}
pandas>=1.3.0
numpy>=1.20.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
jupyter>=1.0.0
pytest>=6.0.0
python-dotenv>=0.19.0
""",
                    "setup.py": """from setuptools import find_packages, setup

setup(
    name='{{ project_name_slug }}',
    packages=find_packages(),
    version='0.1.0',
    description='{{ project_description }}',
    author='{{ author_name }}',
    license='MIT',
)
""",
                    "config.yaml": """# Project Configuration
project:
  name: {{ project_name }}
  description: {{ project_description }}
  author: {{ author_name }}
  created: {% now 'utc', '%Y-%m-%d' %}

paths:
  data_raw: data/raw
  data_processed: data/processed
  data_external: data/external
  models: models
  notebooks: notebooks
  reports: reports
  figures: reports/figures

sbyb:
  preprocessing:
    impute_strategy: auto
    scaling: auto
    encoding: auto
  
  task_detection:
    enabled: true
    
  automl:
    model_selection: auto
    hyperparameter_optimization: true
    feature_selection: true
    stacking: false
    
  evaluation:
    metrics: auto
    visualizations: true
    explainability: true
    
  deployment:
    format: pickle
    api_type: fastapi
""",
                    "src/__init__.py": """# -*- coding: utf-8 -*-
""",
                    "src/data/__init__.py": """# -*- coding: utf-8 -*-
""",
                    "src/data/make_dataset.py": """# -*- coding: utf-8 -*-
import os
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import sbyb


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    
    # Load data
    logger.info(f'Loading data from {input_filepath}')
    
    # Use SBYB preprocessing
    from sbyb.preprocessing import PreprocessingPipeline
    
    pipeline = PreprocessingPipeline()
    # Configure pipeline as needed
    
    # Process data
    processed_data = pipeline.fit_transform(input_data)
    
    # Save processed data
    logger.info(f'Saving processed data to {output_filepath}')
    # Save processed_data to output_filepath


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
""",
                    "src/features/__init__.py": """# -*- coding: utf-8 -*-
""",
                    "src/features/build_features.py": """# -*- coding: utf-8 -*-
import os
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import sbyb


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs feature engineering scripts to turn processed data into
        features ready for modeling.
    """
    logger = logging.getLogger(__name__)
    logger.info('building features from processed data')
    
    # Load processed data
    logger.info(f'Loading processed data from {input_filepath}')
    
    # Use SBYB feature engineering
    from sbyb.preprocessing import FeatureEngineering
    
    feature_engineering = FeatureEngineering()
    # Configure feature engineering as needed
    
    # Build features
    features = feature_engineering.fit_transform(processed_data)
    
    # Save features
    logger.info(f'Saving features to {output_filepath}')
    # Save features to output_filepath


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
""",
                    "src/models/__init__.py": """# -*- coding: utf-8 -*-
""",
                    "src/models/train_model.py": """# -*- coding: utf-8 -*-
import os
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import sbyb


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Trains a model using the features data.
    """
    logger = logging.getLogger(__name__)
    logger.info('training model from features data')
    
    # Load features data
    logger.info(f'Loading features data from {input_filepath}')
    
    # Use SBYB AutoML
    from sbyb.automl import AutoMLEngine
    from sbyb.task_detection import TaskDetector
    
    # Detect task type
    task_detector = TaskDetector()
    task_type = task_detector.detect(features_data)
    logger.info(f'Detected task type: {task_type}')
    
    # Initialize AutoML engine
    automl = AutoMLEngine(task_type=task_type)
    
    # Train model
    model = automl.fit(X_train, y_train)
    
    # Evaluate model
    from sbyb.evaluation import Evaluator
    
    evaluator = Evaluator(task_type=task_type)
    metrics = evaluator.evaluate(model, X_test, y_test)
    logger.info(f'Model evaluation metrics: {metrics}')
    
    # Save model
    logger.info(f'Saving model to {output_filepath}')
    from sbyb.deployment import ModelExporter
    
    exporter = ModelExporter()
    exporter.export(model, output_filepath)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
""",
                    "src/models/predict_model.py": """# -*- coding: utf-8 -*-
import os
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import sbyb


@click.command()
@click.argument('model_filepath', type=click.Path(exists=True))
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(model_filepath, input_filepath, output_filepath):
    """ Uses a trained model to make predictions on new data.
    """
    logger = logging.getLogger(__name__)
    logger.info('making predictions using trained model')
    
    # Load model
    logger.info(f'Loading model from {model_filepath}')
    from sbyb.deployment import ModelExporter
    
    exporter = ModelExporter()
    model = exporter.load(model_filepath)
    
    # Load input data
    logger.info(f'Loading input data from {input_filepath}')
    
    # Make predictions
    predictions = model.predict(input_data)
    
    # Save predictions
    logger.info(f'Saving predictions to {output_filepath}')
    # Save predictions to output_filepath


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
""",
                    "src/visualization/__init__.py": """# -*- coding: utf-8 -*-
""",
                    "src/visualization/visualize.py": """# -*- coding: utf-8 -*-
import os
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import sbyb


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Creates visualizations from processed data and model results.
    """
    logger = logging.getLogger(__name__)
    logger.info('creating visualizations')
    
    # Load data
    logger.info(f'Loading data from {input_filepath}')
    
    # Use SBYB visualization tools
    from sbyb.evaluation import Visualizer
    
    visualizer = Visualizer()
    
    # Create visualizations
    figures = visualizer.create_visualizations(data)
    
    # Save visualizations
    logger.info(f'Saving visualizations to {output_filepath}')
    visualizer.save_visualizations(figures, output_filepath)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
""",
                    "notebooks/0.1-initial-data-exploration.ipynb": """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Initial Data Exploration\n",
    "\n",
    "This notebook contains initial exploration of the dataset for the {{ project_name }} project."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Import libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# SBYB imports\n",
    "import sbyb\n",
    "from sbyb.preprocessing import PreprocessingPipeline\n",
    "from sbyb.task_detection import TaskDetector\n",
    "from sbyb.eda import DataProfiler\n",
    "\n",
    "# Set up plotting\n",
    "%matplotlib inline\n",
    "plt.style.use('seaborn-whitegrid')\n",
    "sns.set_style('whitegrid')\n",
    "plt.rcParams['figure.figsize'] = (12, 8)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Load Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Load data\n",
    "# Replace with your data loading code\n",
    "# data = pd.read_csv('../data/raw/your_data.csv')\n",
    "\n",
    "# Display first few rows\n",
    "# data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Overview"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Basic information\n",
    "# data.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Summary statistics\n",
    "# data.describe()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Use SBYB for Data Profiling"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Create a data profiler\n",
    "# profiler = DataProfiler()\n",
    "\n",
    "# Generate profile\n",
    "# profile = profiler.profile(data)\n",
    "\n",
    "# Display profile\n",
    "# profile"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Task Detection"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Detect task type\n",
    "# detector = TaskDetector()\n",
    "# task_type = detector.detect(data)\n",
    "# print(f\"Detected task type: {task_type}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Preprocessing"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Create preprocessing pipeline\n",
    "# pipeline = PreprocessingPipeline()\n",
    "\n",
    "# Process data\n",
    "# processed_data = pipeline.fit_transform(data)\n",
    "\n",
    "# Display processed data\n",
    "# processed_data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Next Steps\n",
    "\n",
    "Based on the initial exploration, the next steps are:\n",
    "\n",
    "1. ...\n",
    "2. ...\n",
    "3. ..."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
""",
                    "notebooks/0.2-model-development.ipynb": """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Model Development\n",
    "\n",
    "This notebook contains model development for the {{ project_name }} project."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Import libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# SBYB imports\n",
    "import sbyb\n",
    "from sbyb.preprocessing import PreprocessingPipeline\n",
    "from sbyb.automl import AutoMLEngine\n",
    "from sbyb.evaluation import Evaluator, Visualizer, Explainer\n",
    "\n",
    "# Set up plotting\n",
    "%matplotlib inline\n",
    "plt.style.use('seaborn-whitegrid')\n",
    "sns.set_style('whitegrid')\n",
    "plt.rcParams['figure.figsize'] = (12, 8)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Load Processed Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Load processed data\n",
    "# Replace with your data loading code\n",
    "# data = pd.read_csv('../data/processed/processed_data.csv')\n",
    "\n",
    "# Display first few rows\n",
    "# data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Prepare Data for Modeling"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Define features and target\n",
    "# X = data.drop('target_column', axis=1)\n",
    "# y = data['target_column']\n",
    "\n",
    "# Split data into train and test sets\n",
    "# from sklearn.model_selection import train_test_split\n",
    "# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Training with SBYB AutoML"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize AutoML engine\n",
    "# automl = AutoMLEngine()\n",
    "\n",
    "# Train model\n",
    "# model = automl.fit(X_train, y_train)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Evaluation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize evaluator\n",
    "# evaluator = Evaluator()\n",
    "\n",
    "# Evaluate model\n",
    "# metrics = evaluator.evaluate(model, X_test, y_test)\n",
    "\n",
    "# Display metrics\n",
    "# metrics"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Visualization"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize visualizer\n",
    "# visualizer = Visualizer()\n",
    "\n",
    "# Create visualizations\n",
    "# figs = visualizer.visualize_model(model, X_test, y_test)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Explainability"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize explainer\n",
    "# explainer = Explainer()\n",
    "\n",
    "# Generate explanations\n",
    "# explanations = explainer.explain(model, X_test)\n",
    "\n",
    "# Display explanations\n",
    "# explanations"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Save Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Save model\n",
    "# from sbyb.deployment import ModelExporter\n",
    "# exporter = ModelExporter()\n",
    "# exporter.export(model, '../models/model.pkl')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Conclusions\n",
    "\n",
    "Based on the model development, the conclusions are:\n",
    "\n",
    "1. ...\n",
    "2. ...\n",
    "3. ..."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
"""
                }
            }
        )
        
        # Classification project template
        self.register_template(
            "classification",
            "Classification Project",
            {
                "description": "A machine learning project structure for classification tasks.",
                "extends": "basic",
                "files": {
                    "config.yaml": """# Project Configuration
project:
  name: {{ project_name }}
  description: {{ project_description }}
  author: {{ author_name }}
  created: {% now 'utc', '%Y-%m-%d' %}
  task_type: classification

paths:
  data_raw: data/raw
  data_processed: data/processed
  data_external: data/external
  models: models
  notebooks: notebooks
  reports: reports
  figures: reports/figures

sbyb:
  preprocessing:
    impute_strategy: auto
    scaling: auto
    encoding: auto
    outlier_detection: true
  
  task_detection:
    enabled: true
    
  automl:
    model_selection: 
      - LogisticRegression
      - RandomForest
      - XGBoost
      - LightGBM
    hyperparameter_optimization: true
    feature_selection: true
    stacking: true
    
  evaluation:
    metrics:
      - accuracy
      - precision
      - recall
      - f1
      - roc_auc
    visualizations:
      - confusion_matrix
      - roc_curve
      - precision_recall_curve
    explainability: true
    
  deployment:
    format: pickle
    api_type: fastapi
""",
                    "notebooks/0.1-initial-data-exploration.ipynb": """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Initial Data Exploration for Classification\n",
    "\n",
    "This notebook contains initial exploration of the dataset for the {{ project_name }} classification project."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Import libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# SBYB imports\n",
    "import sbyb\n",
    "from sbyb.preprocessing import PreprocessingPipeline\n",
    "from sbyb.task_detection import TaskDetector, ClassificationDetector\n",
    "from sbyb.eda import DataProfiler\n",
    "\n",
    "# Set up plotting\n",
    "%matplotlib inline\n",
    "plt.style.use('seaborn-whitegrid')\n",
    "sns.set_style('whitegrid')\n",
    "plt.rcParams['figure.figsize'] = (12, 8)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Load Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Load data\n",
    "# Replace with your data loading code\n",
    "# data = pd.read_csv('../data/raw/your_data.csv')\n",
    "\n",
    "# Display first few rows\n",
    "# data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Overview"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Basic information\n",
    "# data.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Summary statistics\n",
    "# data.describe()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Target Variable Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Analyze target variable\n",
    "# target_col = 'target_column'  # Replace with your target column name\n",
    "# data[target_col].value_counts()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Visualize target distribution\n",
    "# plt.figure(figsize=(10, 6))\n",
    "# sns.countplot(data[target_col])\n",
    "# plt.title('Target Variable Distribution')\n",
    "# plt.xlabel('Class')\n",
    "# plt.ylabel('Count')\n",
    "# plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Feature Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Analyze correlations\n",
    "# corr = data.corr()\n",
    "# plt.figure(figsize=(12, 10))\n",
    "# sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')\n",
    "# plt.title('Feature Correlations')\n",
    "# plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Analyze feature distributions by class\n",
    "# for col in data.select_dtypes(include=['number']).columns:\n",
    "#     if col != target_col:\n",
    "#         plt.figure(figsize=(12, 6))\n",
    "#         sns.histplot(data=data, x=col, hue=target_col, kde=True, element='step')\n",
    "#         plt.title(f'Distribution of {col} by Class')\n",
    "#         plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Use SBYB for Data Profiling"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Create a data profiler\n",
    "# profiler = DataProfiler()\n",
    "\n",
    "# Generate profile\n",
    "# profile = profiler.profile(data)\n",
    "\n",
    "# Display profile\n",
    "# profile"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Classification Task Detection"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Detect classification task details\n",
    "# detector = ClassificationDetector()\n",
    "# classification_info = detector.detect(data, target_column=target_col)\n",
    "# print(f\"Classification type: {classification_info['type']}\")\n",
    "# print(f\"Number of classes: {classification_info['n_classes']}\")\n",
    "# print(f\"Class balance: {classification_info['class_balance']}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Preprocessing"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Create preprocessing pipeline\n",
    "# pipeline = PreprocessingPipeline()\n",
    "\n",
    "# Process data\n",
    "# processed_data = pipeline.fit_transform(data)\n",
    "\n",
    "# Display processed data\n",
    "# processed_data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Next Steps\n",
    "\n",
    "Based on the initial exploration, the next steps are:\n",
    "\n",
    "1. Handle class imbalance if present\n",
    "2. Feature selection and engineering\n",
    "3. Model selection and training\n",
    "4. Model evaluation and tuning"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
""",
                    "notebooks/0.2-model-development.ipynb": """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Classification Model Development\n",
    "\n",
    "This notebook contains classification model development for the {{ project_name }} project."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Import libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# SBYB imports\n",
    "import sbyb\n",
    "from sbyb.preprocessing import PreprocessingPipeline\n",
    "from sbyb.automl import AutoMLEngine\n",
    "from sbyb.evaluation import Evaluator, Visualizer, Explainer\n",
    "\n",
    "# Set up plotting\n",
    "%matplotlib inline\n",
    "plt.style.use('seaborn-whitegrid')\n",
    "sns.set_style('whitegrid')\n",
    "plt.rcParams['figure.figsize'] = (12, 8)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Load Processed Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Load processed data\n",
    "# Replace with your data loading code\n",
    "# data = pd.read_csv('../data/processed/processed_data.csv')\n",
    "\n",
    "# Display first few rows\n",
    "# data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Prepare Data for Modeling"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Define features and target\n",
    "# target_col = 'target_column'  # Replace with your target column name\n",
    "# X = data.drop(target_col, axis=1)\n",
    "# y = data[target_col]\n",
    "\n",
    "# Split data into train and test sets\n",
    "# from sklearn.model_selection import train_test_split\n",
    "# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Training with SBYB AutoML"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize AutoML engine for classification\n",
    "# automl = AutoMLEngine(task_type='classification')\n",
    "\n",
    "# Train model\n",
    "# model = automl.fit(X_train, y_train)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Evaluation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize evaluator for classification\n",
    "# evaluator = Evaluator(task_type='classification')\n",
    "\n",
    "# Evaluate model\n",
    "# metrics = evaluator.evaluate(model, X_test, y_test)\n",
    "\n",
    "# Display metrics\n",
    "# metrics"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Classification Visualizations"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize visualizer for classification\n",
    "# visualizer = Visualizer(task_type='classification')\n",
    "\n",
    "# Create confusion matrix\n",
    "# cm_fig = visualizer.plot_confusion_matrix(model, X_test, y_test)\n",
    "\n",
    "# Create ROC curve\n",
    "# roc_fig = visualizer.plot_roc_curve(model, X_test, y_test)\n",
    "\n",
    "# Create precision-recall curve\n",
    "# pr_fig = visualizer.plot_precision_recall_curve(model, X_test, y_test)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Explainability"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize explainer\n",
    "# explainer = Explainer()\n",
    "\n",
    "# Generate feature importance\n",
    "# importance = explainer.feature_importance(model, X_test)\n",
    "\n",
    "# Plot feature importance\n",
    "# plt.figure(figsize=(12, 8))\n",
    "# importance.sort_values().plot(kind='barh')\n",
    "# plt.title('Feature Importance')\n",
    "# plt.show()\n",
    "\n",
    "# Generate SHAP values\n",
    "# shap_values = explainer.shap_values(model, X_test)\n",
    "\n",
    "# Plot SHAP summary\n",
    "# explainer.plot_shap_summary(shap_values, X_test)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Save Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Save model\n",
    "# from sbyb.deployment import ModelExporter\n",
    "# exporter = ModelExporter()\n",
    "# exporter.export(model, '../models/classification_model.pkl')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Deploy Model API"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Generate API\n",
    "# from sbyb.deployment import APIGenerator\n",
    "# api_generator = APIGenerator()\n",
    "# api_generator.generate_fastapi('../models/classification_model.pkl', '../deployment/api')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Conclusions\n",
    "\n",
    "Based on the classification model development, the conclusions are:\n",
    "\n",
    "1. ...\n",
    "2. ...\n",
    "3. ..."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
"""
                }
            }
        )
        
        # Regression project template
        self.register_template(
            "regression",
            "Regression Project",
            {
                "description": "A machine learning project structure for regression tasks.",
                "extends": "basic",
                "files": {
                    "config.yaml": """# Project Configuration
project:
  name: {{ project_name }}
  description: {{ project_description }}
  author: {{ author_name }}
  created: {% now 'utc', '%Y-%m-%d' %}
  task_type: regression

paths:
  data_raw: data/raw
  data_processed: data/processed
  data_external: data/external
  models: models
  notebooks: notebooks
  reports: reports
  figures: reports/figures

sbyb:
  preprocessing:
    impute_strategy: auto
    scaling: auto
    encoding: auto
    outlier_detection: true
  
  task_detection:
    enabled: true
    
  automl:
    model_selection: 
      - LinearRegression
      - RandomForestRegressor
      - XGBRegressor
      - LGBMRegressor
    hyperparameter_optimization: true
    feature_selection: true
    stacking: true
    
  evaluation:
    metrics:
      - r2
      - mse
      - rmse
      - mae
      - mape
    visualizations:
      - residuals
      - actual_vs_predicted
      - error_distribution
    explainability: true
    
  deployment:
    format: pickle
    api_type: fastapi
""",
                    "notebooks/0.1-initial-data-exploration.ipynb": """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Initial Data Exploration for Regression\n",
    "\n",
    "This notebook contains initial exploration of the dataset for the {{ project_name }} regression project."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Import libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# SBYB imports\n",
    "import sbyb\n",
    "from sbyb.preprocessing import PreprocessingPipeline\n",
    "from sbyb.task_detection import TaskDetector, RegressionDetector\n",
    "from sbyb.eda import DataProfiler\n",
    "\n",
    "# Set up plotting\n",
    "%matplotlib inline\n",
    "plt.style.use('seaborn-whitegrid')\n",
    "sns.set_style('whitegrid')\n",
    "plt.rcParams['figure.figsize'] = (12, 8)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Load Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Load data\n",
    "# Replace with your data loading code\n",
    "# data = pd.read_csv('../data/raw/your_data.csv')\n",
    "\n",
    "# Display first few rows\n",
    "# data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Overview"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Basic information\n",
    "# data.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Summary statistics\n",
    "# data.describe()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Target Variable Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Analyze target variable\n",
    "# target_col = 'target_column'  # Replace with your target column name\n",
    "# plt.figure(figsize=(10, 6))\n",
    "# sns.histplot(data[target_col], kde=True)\n",
    "# plt.title('Target Variable Distribution')\n",
    "# plt.xlabel(target_col)\n",
    "# plt.ylabel('Frequency')\n",
    "# plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Check for skewness\n",
    "# skewness = data[target_col].skew()\n",
    "# print(f\"Target skewness: {skewness}\")\n",
    "\n",
    "# If skewed, try log transformation\n",
    "# if abs(skewness) > 1:\n",
    "#     plt.figure(figsize=(12, 6))\n",
    "#     plt.subplot(1, 2, 1)\n",
    "#     sns.histplot(data[target_col], kde=True)\n",
    "#     plt.title('Original Target Distribution')\n",
    "#     \n",
    "#     plt.subplot(1, 2, 2)\n",
    "#     sns.histplot(np.log1p(data[target_col]), kde=True)\n",
    "#     plt.title('Log-Transformed Target Distribution')\n",
    "#     plt.tight_layout()\n",
    "#     plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Feature Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Analyze correlations\n",
    "# corr = data.corr()\n",
    "# plt.figure(figsize=(12, 10))\n",
    "# sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')\n",
    "# plt.title('Feature Correlations')\n",
    "# plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Analyze feature relationships with target\n",
    "# for col in data.select_dtypes(include=['number']).columns:\n",
    "#     if col != target_col:\n",
    "#         plt.figure(figsize=(10, 6))\n",
    "#         sns.scatterplot(x=col, y=target_col, data=data)\n",
    "#         plt.title(f'Relationship between {col} and {target_col}')\n",
    "#         plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Use SBYB for Data Profiling"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Create a data profiler\n",
    "# profiler = DataProfiler()\n",
    "\n",
    "# Generate profile\n",
    "# profile = profiler.profile(data)\n",
    "\n",
    "# Display profile\n",
    "# profile"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Regression Task Detection"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Detect regression task details\n",
    "# detector = RegressionDetector()\n",
    "# regression_info = detector.detect(data, target_column=target_col)\n",
    "# print(f\"Target range: {regression_info['range']}\")\n",
    "# print(f\"Target distribution: {regression_info['distribution']}\")\n",
    "# print(f\"Recommended transformations: {regression_info['recommended_transformations']}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Preprocessing"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Create preprocessing pipeline\n",
    "# pipeline = PreprocessingPipeline()\n",
    "\n",
    "# Process data\n",
    "# processed_data = pipeline.fit_transform(data)\n",
    "\n",
    "# Display processed data\n",
    "# processed_data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Next Steps\n",
    "\n",
    "Based on the initial exploration, the next steps are:\n",
    "\n",
    "1. Handle outliers in the target variable\n",
    "2. Apply appropriate transformations to the target\n",
    "3. Feature selection and engineering\n",
    "4. Model selection and training\n",
    "5. Model evaluation and tuning"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
""",
                    "notebooks/0.2-model-development.ipynb": """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Regression Model Development\n",
    "\n",
    "This notebook contains regression model development for the {{ project_name }} project."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Import libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# SBYB imports\n",
    "import sbyb\n",
    "from sbyb.preprocessing import PreprocessingPipeline\n",
    "from sbyb.automl import AutoMLEngine\n",
    "from sbyb.evaluation import Evaluator, Visualizer, Explainer\n",
    "\n",
    "# Set up plotting\n",
    "%matplotlib inline\n",
    "plt.style.use('seaborn-whitegrid')\n",
    "sns.set_style('whitegrid')\n",
    "plt.rcParams['figure.figsize'] = (12, 8)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Load Processed Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Load processed data\n",
    "# Replace with your data loading code\n",
    "# data = pd.read_csv('../data/processed/processed_data.csv')\n",
    "\n",
    "# Display first few rows\n",
    "# data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Prepare Data for Modeling"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Define features and target\n",
    "# target_col = 'target_column'  # Replace with your target column name\n",
    "# X = data.drop(target_col, axis=1)\n",
    "# y = data[target_col]\n",
    "\n",
    "# Split data into train and test sets\n",
    "# from sklearn.model_selection import train_test_split\n",
    "# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Training with SBYB AutoML"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize AutoML engine for regression\n",
    "# automl = AutoMLEngine(task_type='regression')\n",
    "\n",
    "# Train model\n",
    "# model = automl.fit(X_train, y_train)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Evaluation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize evaluator for regression\n",
    "# evaluator = Evaluator(task_type='regression')\n",
    "\n",
    "# Evaluate model\n",
    "# metrics = evaluator.evaluate(model, X_test, y_test)\n",
    "\n",
    "# Display metrics\n",
    "# metrics"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Regression Visualizations"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize visualizer for regression\n",
    "# visualizer = Visualizer(task_type='regression')\n",
    "\n",
    "# Make predictions\n",
    "# y_pred = model.predict(X_test)\n",
    "\n",
    "# Create residual plot\n",
    "# residual_fig = visualizer.plot_residuals(y_test, y_pred)\n",
    "\n",
    "# Create actual vs predicted plot\n",
    "# actual_vs_pred_fig = visualizer.plot_actual_vs_predicted(y_test, y_pred)\n",
    "\n",
    "# Create error distribution plot\n",
    "# error_dist_fig = visualizer.plot_error_distribution(y_test, y_pred)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Explainability"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize explainer\n",
    "# explainer = Explainer()\n",
    "\n",
    "# Generate feature importance\n",
    "# importance = explainer.feature_importance(model, X_test)\n",
    "\n",
    "# Plot feature importance\n",
    "# plt.figure(figsize=(12, 8))\n",
    "# importance.sort_values().plot(kind='barh')\n",
    "# plt.title('Feature Importance')\n",
    "# plt.show()\n",
    "\n",
    "# Generate SHAP values\n",
    "# shap_values = explainer.shap_values(model, X_test)\n",
    "\n",
    "# Plot SHAP summary\n",
    "# explainer.plot_shap_summary(shap_values, X_test)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Save Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Save model\n",
    "# from sbyb.deployment import ModelExporter\n",
    "# exporter = ModelExporter()\n",
    "# exporter.export(model, '../models/regression_model.pkl')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Deploy Model API"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Generate API\n",
    "# from sbyb.deployment import APIGenerator\n",
    "# api_generator = APIGenerator()\n",
    "# api_generator.generate_fastapi('../models/regression_model.pkl', '../deployment/api')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Conclusions\n",
    "\n",
    "Based on the regression model development, the conclusions are:\n",
    "\n",
    "1. ...\n",
    "2. ...\n",
    "3. ..."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
"""
                }
            }
        )
        
        # Time series project template
        self.register_template(
            "time_series",
            "Time Series Project",
            {
                "description": "A machine learning project structure for time series tasks.",
                "extends": "basic",
                "files": {
                    "config.yaml": """# Project Configuration
project:
  name: {{ project_name }}
  description: {{ project_description }}
  author: {{ author_name }}
  created: {% now 'utc', '%Y-%m-%d' %}
  task_type: time_series

paths:
  data_raw: data/raw
  data_processed: data/processed
  data_external: data/external
  models: models
  notebooks: notebooks
  reports: reports
  figures: reports/figures

sbyb:
  preprocessing:
    impute_strategy: auto
    scaling: auto
    encoding: auto
    outlier_detection: true
    time_series_features: true
  
  task_detection:
    enabled: true
    
  automl:
    model_selection: 
      - ARIMA
      - Prophet
      - LSTM
      - XGBRegressor
    hyperparameter_optimization: true
    feature_selection: true
    stacking: false
    
  evaluation:
    metrics:
      - mse
      - rmse
      - mae
      - mape
    visualizations:
      - forecast_vs_actual
      - residuals
      - components
    explainability: true
    
  deployment:
    format: pickle
    api_type: fastapi
""",
                    "notebooks/0.1-initial-data-exploration.ipynb": """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Initial Data Exploration for Time Series\n",
    "\n",
    "This notebook contains initial exploration of the dataset for the {{ project_name }} time series project."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Import libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from statsmodels.tsa.seasonal import seasonal_decompose\n",
    "from statsmodels.graphics.tsaplots import plot_acf, plot_pacf\n",
    "\n",
    "# SBYB imports\n",
    "import sbyb\n",
    "from sbyb.preprocessing import PreprocessingPipeline\n",
    "from sbyb.task_detection import TaskDetector, TimeSeriesDetector\n",
    "from sbyb.eda import DataProfiler\n",
    "\n",
    "# Set up plotting\n",
    "%matplotlib inline\n",
    "plt.style.use('seaborn-whitegrid')\n",
    "sns.set_style('whitegrid')\n",
    "plt.rcParams['figure.figsize'] = (12, 8)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Load Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Load data\n",
    "# Replace with your data loading code\n",
    "# data = pd.read_csv('../data/raw/your_data.csv')\n",
    "\n",
    "# Convert date column to datetime\n",
    "# date_col = 'date_column'  # Replace with your date column name\n",
    "# data[date_col] = pd.to_datetime(data[date_col])\n",
    "\n",
    "# Set date column as index\n",
    "# data = data.set_index(date_col)\n",
    "\n",
    "# Sort by date\n",
    "# data = data.sort_index()\n",
    "\n",
    "# Display first few rows\n",
    "# data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Overview"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Basic information\n",
    "# data.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Summary statistics\n",
    "# data.describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Check for missing values\n",
    "# data.isna().sum()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Time Series Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Plot time series\n",
    "# target_col = 'target_column'  # Replace with your target column name\n",
    "# plt.figure(figsize=(15, 6))\n",
    "# plt.plot(data.index, data[target_col])\n",
    "# plt.title(f'{target_col} Time Series')\n",
    "# plt.xlabel('Date')\n",
    "# plt.ylabel(target_col)\n",
    "# plt.grid(True)\n",
    "# plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Resample to different frequencies\n",
    "# daily = data[target_col].resample('D').mean()\n",
    "# weekly = data[target_col].resample('W').mean()\n",
    "# monthly = data[target_col].resample('M').mean()\n",
    "\n",
    "# plt.figure(figsize=(15, 12))\n",
    "\n",
    "# plt.subplot(3, 1, 1)\n",
    "# plt.plot(daily.index, daily)\n",
    "# plt.title('Daily Resampling')\n",
    "# plt.grid(True)\n",
    "\n",
    "# plt.subplot(3, 1, 2)\n",
    "# plt.plot(weekly.index, weekly)\n",
    "# plt.title('Weekly Resampling')\n",
    "# plt.grid(True)\n",
    "\n",
    "# plt.subplot(3, 1, 3)\n",
    "# plt.plot(monthly.index, monthly)\n",
    "# plt.title('Monthly Resampling')\n",
    "# plt.grid(True)\n",
    "\n",
    "# plt.tight_layout()\n",
    "# plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Seasonal decomposition\n",
    "# decomposition = seasonal_decompose(data[target_col], model='additive', period=30)  # Adjust period as needed\n",
    "# fig = decomposition.plot()\n",
    "# fig.set_size_inches(15, 12)\n",
    "# plt.tight_layout()\n",
    "# plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# ACF and PACF plots\n",
    "# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))\n",
    "# plot_acf(data[target_col], ax=ax1, lags=40)\n",
    "# plot_pacf(data[target_col], ax=ax2, lags=40)\n",
    "# plt.tight_layout()\n",
    "# plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Use SBYB for Time Series Detection"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Detect time series characteristics\n",
    "# detector = TimeSeriesDetector()\n",
    "# ts_info = detector.detect(data, target_column=target_col)\n",
    "# print(f\"Frequency: {ts_info['frequency']}\")\n",
    "# print(f\"Stationarity: {ts_info['stationarity']}\")\n",
    "# print(f\"Seasonality: {ts_info['seasonality']}\")\n",
    "# print(f\"Trend: {ts_info['trend']}\")\n",
    "# print(f\"Recommended models: {ts_info['recommended_models']}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Preprocessing for Time Series"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Create preprocessing pipeline for time series\n",
    "# pipeline = PreprocessingPipeline(time_series=True)\n",
    "\n",
    "# Process data\n",
    "# processed_data = pipeline.fit_transform(data)\n",
    "\n",
    "# Display processed data\n",
    "# processed_data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Feature Engineering for Time Series"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Create time series features\n",
    "# from sbyb.preprocessing import FeatureEngineering\n",
    "# feature_eng = FeatureEngineering(time_series=True)\n",
    "\n",
    "# Add time series features\n",
    "# features = feature_eng.fit_transform(processed_data)\n",
    "\n",
    "# Display features\n",
    "# features.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Next Steps\n",
    "\n",
    "Based on the initial exploration, the next steps are:\n",
    "\n",
    "1. Handle missing values and outliers\n",
    "2. Apply appropriate transformations for stationarity\n",
    "3. Create lag features and other time series features\n",
    "4. Split data into train and test sets (respecting time order)\n",
    "5. Model selection and training\n",
    "6. Model evaluation and tuning"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
""",
                    "notebooks/0.2-model-development.ipynb": """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Time Series Model Development\n",
    "\n",
    "This notebook contains time series model development for the {{ project_name }} project."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Import libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# SBYB imports\n",
    "import sbyb\n",
    "from sbyb.preprocessing import PreprocessingPipeline\n",
    "from sbyb.automl import AutoMLEngine\n",
    "from sbyb.evaluation import Evaluator, Visualizer, Explainer\n",
    "\n",
    "# Set up plotting\n",
    "%matplotlib inline\n",
    "plt.style.use('seaborn-whitegrid')\n",
    "sns.set_style('whitegrid')\n",
    "plt.rcParams['figure.figsize'] = (12, 8)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Load Processed Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Load processed data\n",
    "# Replace with your data loading code\n",
    "# data = pd.read_csv('../data/processed/processed_data.csv')\n",
    "\n",
    "# Convert date column to datetime\n",
    "# date_col = 'date_column'  # Replace with your date column name\n",
    "# data[date_col] = pd.to_datetime(data[date_col])\n",
    "\n",
    "# Set date column as index\n",
    "# data = data.set_index(date_col)\n",
    "\n",
    "# Sort by date\n",
    "# data = data.sort_index()\n",
    "\n",
    "# Display first few rows\n",
    "# data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Prepare Data for Time Series Modeling"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Define target variable\n",
    "# target_col = 'target_column'  # Replace with your target column name\n",
    "\n",
    "# Split data into train and test sets (time-based split)\n",
    "# train_size = int(len(data) * 0.8)\n",
    "# train_data = data.iloc[:train_size]\n",
    "# test_data = data.iloc[train_size:]\n",
    "\n",
    "# print(f\"Training data: {train_data.index.min()} to {train_data.index.max()} ({len(train_data)} records)\")\n",
    "# print(f\"Testing data: {test_data.index.min()} to {test_data.index.max()} ({len(test_data)} records)\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Time Series Model Training with SBYB AutoML"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize AutoML engine for time series\n",
    "# automl = AutoMLEngine(task_type='time_series')\n",
    "\n",
    "# Configure time series parameters\n",
    "# automl.set_params(\n",
    "#     forecast_horizon=30,  # Number of periods to forecast\n",
    "#     frequency='D',       # Frequency of the time series (D=daily, W=weekly, M=monthly, etc.)\n",
    "#     seasonality=True     # Whether to model seasonality\n",
    "# )\n",
    "\n",
    "# Train model\n",
    "# model = automl.fit(train_data, target_column=target_col)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Evaluation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize evaluator for time series\n",
    "# evaluator = Evaluator(task_type='time_series')\n",
    "\n",
    "# Evaluate model\n",
    "# metrics = evaluator.evaluate(model, test_data, target_column=target_col)\n",
    "\n",
    "# Display metrics\n",
    "# metrics"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Time Series Visualizations"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Initialize visualizer for time series\n",
    "# visualizer = Visualizer(task_type='time_series')\n",
    "\n",
    "# Generate forecast\n",
    "# forecast = model.predict(len(test_data))\n",
    "\n",
    "# Plot forecast vs actual\n",
    "# forecast_fig = visualizer.plot_forecast_vs_actual(forecast, test_data[target_col])\n",
    "\n",
    "# Plot components (trend, seasonality, etc.)\n",
    "# components_fig = visualizer.plot_components(model)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Future Forecasting"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Generate future forecast\n",
    "# future_periods = 90  # Number of periods to forecast into the future\n",
    "# future_forecast = model.predict(future_periods)\n",
    "\n",
    "# Plot future forecast\n",
    "# plt.figure(figsize=(15, 6))\n",
    "# plt.plot(data.index, data[target_col], label='Historical Data')\n",
    "# plt.plot(future_forecast.index, future_forecast, label='Future Forecast', color='red')\n",
    "# plt.title('Future Forecast')\n",
    "# plt.xlabel('Date')\n",
    "# plt.ylabel(target_col)\n",
    "# plt.legend()\n",
    "# plt.grid(True)\n",
    "# plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Save Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Save model\n",
    "# from sbyb.deployment import ModelExporter\n",
    "# exporter = ModelExporter()\n",
    "# exporter.export(model, '../models/time_series_model.pkl')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Deploy Model API"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Generate API\n",
    "# from sbyb.deployment import APIGenerator\n",
    "# api_generator = APIGenerator()\n",
    "# api_generator.generate_fastapi('../models/time_series_model.pkl', '../deployment/api')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Conclusions\n",
    "\n",
    "Based on the time series model development, the conclusions are:\n",
    "\n",
    "1. ...\n",
    "2. ...\n",
    "3. ..."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
"""
                }
            }
        )
    
    def register_template(self, template_id: str, template_name: str,
                         config: Dict[str, Any]) -> None:
        """
        Register a project template.
        
        Args:
            template_id: Unique identifier for the template.
            template_name: Display name for the template.
            config: Configuration for the template.
        """
        if template_id in self.templates:
            raise ScaffoldingError(f"Template ID '{template_id}' already exists.")
        
        template = {
            "id": template_id,
            "name": template_name,
            "config": config
        }
        
        self.templates[template_id] = template
    
    def get_template(self, template_id: str) -> Dict[str, Any]:
        """
        Get a template by ID.
        
        Args:
            template_id: ID of the template to get.
            
        Returns:
            Template configuration.
        """
        if template_id not in self.templates:
            raise ScaffoldingError(f"Template ID '{template_id}' does not exist.")
        
        return self.templates[template_id]
    
    def get_all_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all templates.
        
        Returns:
            Dictionary of all templates.
        """
        return self.templates
    
    def generate_project(self, output_dir: str, template_id: str,
                        context: Dict[str, Any]) -> str:
        """
        Generate a new project from a template.
        
        Args:
            output_dir: Directory to output the generated project.
            template_id: ID of the template to use.
            context: Context variables for template rendering.
            
        Returns:
            Path to the output directory.
        """
        import jinja2
        
        template = self.get_template(template_id)
        
        # Check if template extends another template
        if "extends" in template["config"]:
            parent_template_id = template["config"]["extends"]
            parent_template = self.get_template(parent_template_id)
            
            # Merge directories
            directories = parent_template["config"].get("directories", []).copy()
            if "directories" in template["config"]:
                for directory in template["config"]["directories"]:
                    if directory not in directories:
                        directories.append(directory)
            
            # Merge files
            files = parent_template["config"].get("files", {}).copy()
            if "files" in template["config"]:
                files.update(template["config"]["files"])
        else:
            directories = template["config"].get("directories", [])
            files = template["config"].get("files", {})
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create directories
        for directory in directories:
            dir_path = os.path.join(output_dir, directory)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        
        # Create Jinja2 environment
        env = jinja2.Environment()
        
        # Add custom filters
        def now_filter(value, format_string="%Y-%m-%d"):
            return datetime.datetime.now().strftime(format_string)
        
        env.filters["now"] = now_filter
        
        # Process files
        for file_path, file_content in files.items():
            # Create directory for file if it doesn't exist
            file_dir = os.path.dirname(os.path.join(output_dir, file_path))
            if file_dir and not os.path.exists(file_dir):
                os.makedirs(file_dir)
            
            # Render file content
            template_obj = env.from_string(file_content)
            rendered_content = template_obj.render(**context)
            
            # Write file
            with open(os.path.join(output_dir, file_path), "w") as f:
                f.write(rendered_content)
        
        return output_dir
    
    def create_custom_template(self, template_id: str, template_name: str,
                              directories: List[str], files: Dict[str, str],
                              description: str = "", extends: str = None) -> None:
        """
        Create a custom project template.
        
        Args:
            template_id: Unique identifier for the template.
            template_name: Display name for the template.
            directories: List of directories to create.
            files: Dictionary of file paths and contents.
            description: Description of the template.
            extends: ID of the template to extend.
        """
        config = {
            "description": description,
            "directories": directories,
            "files": files
        }
        
        if extends:
            if extends not in self.templates:
                raise ScaffoldingError(f"Template ID '{extends}' does not exist.")
            config["extends"] = extends
        
        self.register_template(template_id, template_name, config)
    
    def export_template(self, template_id: str, output_path: str) -> str:
        """
        Export a template to a JSON file.
        
        Args:
            template_id: ID of the template to export.
            output_path: Path to save the exported template.
            
        Returns:
            Path to the exported template.
        """
        template = self.get_template(template_id)
        
        # Create template export data
        export_data = {
            "id": template["id"],
            "name": template["name"],
            "config": template["config"]
        }
        
        # Save to JSON file
        json_path = output_path if output_path.endswith(".json") else f"{output_path}.json"
        with open(json_path, "w") as f:
            json.dump(export_data, f, indent=2)
        
        return json_path
    
    def import_template(self, json_path: str) -> str:
        """
        Import a template from a JSON file.
        
        Args:
            json_path: Path to the JSON file.
            
        Returns:
            ID of the imported template.
        """
        # Load template from JSON file
        with open(json_path, "r") as f:
            template_data = json.load(f)
        
        # Validate template data
        required_keys = ["id", "name", "config"]
        for key in required_keys:
            if key not in template_data:
                raise ScaffoldingError(f"Missing required key '{key}' in template data.")
        
        # Register template
        self.register_template(
            template_data["id"],
            template_data["name"],
            template_data["config"]
        )
        
        return template_data["id"]
