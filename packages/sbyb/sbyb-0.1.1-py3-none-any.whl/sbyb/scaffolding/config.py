"""
Configuration generator for SBYB Scaffolding.

This module provides functionality to generate configuration files
for ML projects, including environment setup, package requirements,
and project settings.
"""

from typing import Any, Dict, List, Optional, Union
import os
import yaml
import json
import toml
import configparser
from pathlib import Path

from sbyb.core.base import SBYBComponent
from sbyb.core.config import Config
from sbyb.core.exceptions import ScaffoldingError


class ConfigGenerator(SBYBComponent):
    """
    Configuration generator for ML projects.
    
    This component provides functionality to generate various configuration files
    for ML projects, including environment setup, package requirements, and project settings.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the configuration generator.
        
        Args:
            config: Configuration dictionary for the configuration generator.
        """
        super().__init__(config)
    
    def generate_sbyb_config(self, output_path: str, project_name: str, 
                            task_type: str = "auto", 
                            preprocessing_config: Optional[Dict[str, Any]] = None,
                            automl_config: Optional[Dict[str, Any]] = None,
                            evaluation_config: Optional[Dict[str, Any]] = None,
                            deployment_config: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate SBYB configuration file.
        
        Args:
            output_path: Path to save the configuration file.
            project_name: Name of the project.
            task_type: Type of ML task (auto, classification, regression, clustering, etc.).
            preprocessing_config: Configuration for preprocessing.
            automl_config: Configuration for AutoML.
            evaluation_config: Configuration for evaluation.
            deployment_config: Configuration for deployment.
            
        Returns:
            Path to the generated configuration file.
        """
        # Default configurations
        default_preprocessing = {
            "impute_strategy": "auto",
            "scaling": "auto",
            "encoding": "auto",
            "outlier_detection": True,
            "feature_engineering": True
        }
        
        default_automl = {
            "model_selection": "auto",
            "hyperparameter_optimization": True,
            "feature_selection": True,
            "stacking": False
        }
        
        default_evaluation = {
            "metrics": "auto",
            "visualizations": True,
            "explainability": True
        }
        
        default_deployment = {
            "format": "pickle",
            "api_type": "fastapi"
        }
        
        # Merge with provided configurations
        preprocessing = {**default_preprocessing, **(preprocessing_config or {})}
        automl = {**default_automl, **(automl_config or {})}
        evaluation = {**default_evaluation, **(evaluation_config or {})}
        deployment = {**default_deployment, **(deployment_config or {})}
        
        # Create configuration
        config = {
            "project": {
                "name": project_name,
                "task_type": task_type
            },
            "sbyb": {
                "preprocessing": preprocessing,
                "task_detection": {
                    "enabled": task_type == "auto"
                },
                "automl": automl,
                "evaluation": evaluation,
                "deployment": deployment
            }
        }
        
        # Save configuration
        with open(output_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
        
        return output_path
    
    def generate_requirements(self, output_path: str, 
                             include_core: bool = True,
                             include_ml: bool = True,
                             include_viz: bool = True,
                             include_deployment: bool = True,
                             include_extras: bool = False,
                             additional_packages: Optional[List[str]] = None) -> str:
        """
        Generate requirements.txt file.
        
        Args:
            output_path: Path to save the requirements file.
            include_core: Whether to include core packages.
            include_ml: Whether to include ML packages.
            include_viz: Whether to include visualization packages.
            include_deployment: Whether to include deployment packages.
            include_extras: Whether to include extra packages.
            additional_packages: Additional packages to include.
            
        Returns:
            Path to the generated requirements file.
        """
        requirements = []
        
        # Core packages
        if include_core:
            requirements.extend([
                "sbyb",
                "numpy>=1.20.0",
                "pandas>=1.3.0",
                "scikit-learn>=1.0.0",
                "python-dotenv>=0.19.0"
            ])
        
        # ML packages
        if include_ml:
            requirements.extend([
                "xgboost>=1.5.0",
                "lightgbm>=3.3.0",
                "catboost>=1.0.0",
                "statsmodels>=0.13.0",
                "scipy>=1.7.0"
            ])
        
        # Visualization packages
        if include_viz:
            requirements.extend([
                "matplotlib>=3.4.0",
                "seaborn>=0.11.0",
                "plotly>=5.3.0",
                "ipywidgets>=7.6.0"
            ])
        
        # Deployment packages
        if include_deployment:
            requirements.extend([
                "fastapi>=0.70.0",
                "uvicorn>=0.15.0",
                "streamlit>=1.0.0",
                "gradio>=2.0.0",
                "flask>=2.0.0"
            ])
        
        # Extra packages
        if include_extras:
            requirements.extend([
                "shap>=0.40.0",
                "lime>=0.2.0",
                "eli5>=0.11.0",
                "mlflow>=1.20.0",
                "optuna>=2.10.0",
                "hyperopt>=0.2.5",
                "pytest>=6.0.0",
                "black>=21.9b0",
                "isort>=5.9.0",
                "flake8>=4.0.0"
            ])
        
        # Add additional packages
        if additional_packages:
            requirements.extend(additional_packages)
        
        # Write requirements file
        with open(output_path, "w") as f:
            f.write("\n".join(requirements))
        
        return output_path
    
    def generate_conda_environment(self, output_path: str, environment_name: str,
                                  python_version: str = "3.9",
                                  include_core: bool = True,
                                  include_ml: bool = True,
                                  include_viz: bool = True,
                                  include_deployment: bool = True,
                                  include_extras: bool = False,
                                  additional_packages: Optional[List[str]] = None,
                                  channels: Optional[List[str]] = None) -> str:
        """
        Generate conda environment.yml file.
        
        Args:
            output_path: Path to save the environment file.
            environment_name: Name of the conda environment.
            python_version: Python version to use.
            include_core: Whether to include core packages.
            include_ml: Whether to include ML packages.
            include_viz: Whether to include visualization packages.
            include_deployment: Whether to include deployment packages.
            include_extras: Whether to include extra packages.
            additional_packages: Additional packages to include.
            channels: Conda channels to use.
            
        Returns:
            Path to the generated environment file.
        """
        # Default channels
        if channels is None:
            channels = ["defaults", "conda-forge"]
        
        # Initialize dependencies
        dependencies = [f"python={python_version}"]
        
        # Core packages
        if include_core:
            dependencies.extend([
                "numpy>=1.20.0",
                "pandas>=1.3.0",
                "scikit-learn>=1.0.0",
                "python-dotenv>=0.19.0"
            ])
        
        # ML packages
        if include_ml:
            dependencies.extend([
                "xgboost>=1.5.0",
                "lightgbm>=3.3.0",
                "catboost>=1.0.0",
                "statsmodels>=0.13.0",
                "scipy>=1.7.0"
            ])
        
        # Visualization packages
        if include_viz:
            dependencies.extend([
                "matplotlib>=3.4.0",
                "seaborn>=0.11.0",
                "plotly>=5.3.0",
                "ipywidgets>=7.6.0"
            ])
        
        # Deployment packages
        if include_deployment:
            dependencies.extend([
                "fastapi>=0.70.0",
                "uvicorn>=0.15.0",
                "streamlit>=1.0.0",
                "flask>=2.0.0"
            ])
        
        # Extra packages
        if include_extras:
            dependencies.extend([
                "shap>=0.40.0",
                "mlflow>=1.20.0",
                "optuna>=2.10.0",
                "pytest>=6.0.0",
                "black>=21.9b0",
                "flake8>=4.0.0"
            ])
        
        # Add additional packages
        if additional_packages:
            dependencies.extend(additional_packages)
        
        # Add pip section for packages not available in conda
        pip_packages = ["sbyb", "gradio>=2.0.0", "lime>=0.2.0", "eli5>=0.11.0"]
        
        # Create environment configuration
        environment = {
            "name": environment_name,
            "channels": channels,
            "dependencies": dependencies + [{"pip": pip_packages}]
        }
        
        # Write environment file
        with open(output_path, "w") as f:
            yaml.dump(environment, f, default_flow_style=False)
        
        return output_path
    
    def generate_setup_py(self, output_path: str, package_name: str,
                         version: str = "0.1.0",
                         description: str = "",
                         author: str = "",
                         author_email: str = "",
                         url: str = "",
                         license_type: str = "MIT",
                         python_requires: str = ">=3.7",
                         install_requires: Optional[List[str]] = None) -> str:
        """
        Generate setup.py file for Python package.
        
        Args:
            output_path: Path to save the setup.py file.
            package_name: Name of the package.
            version: Version of the package.
            description: Description of the package.
            author: Author of the package.
            author_email: Author's email.
            url: URL of the package.
            license_type: License type.
            python_requires: Python version requirements.
            install_requires: Required packages.
            
        Returns:
            Path to the generated setup.py file.
        """
        # Default install_requires
        if install_requires is None:
            install_requires = [
                "sbyb",
                "numpy>=1.20.0",
                "pandas>=1.3.0",
                "scikit-learn>=1.0.0"
            ]
        
        # Create setup.py content
        setup_content = f"""from setuptools import find_packages, setup

setup(
    name="{package_name}",
    version="{version}",
    description="{description}",
    author="{author}",
    author_email="{author_email}",
    url="{url}",
    license="{license_type}",
    packages=find_packages(),
    python_requires="{python_requires}",
    install_requires={install_requires},
)
"""
        
        # Write setup.py file
        with open(output_path, "w") as f:
            f.write(setup_content)
        
        return output_path
    
    def generate_pyproject_toml(self, output_path: str, package_name: str,
                               version: str = "0.1.0",
                               description: str = "",
                               author: str = "",
                               author_email: str = "",
                               requires_python: str = ">=3.7",
                               dependencies: Optional[List[str]] = None,
                               dev_dependencies: Optional[List[str]] = None) -> str:
        """
        Generate pyproject.toml file for Python package.
        
        Args:
            output_path: Path to save the pyproject.toml file.
            package_name: Name of the package.
            version: Version of the package.
            description: Description of the package.
            author: Author of the package.
            author_email: Author's email.
            requires_python: Python version requirements.
            dependencies: Required packages.
            dev_dependencies: Development dependencies.
            
        Returns:
            Path to the generated pyproject.toml file.
        """
        # Default dependencies
        if dependencies is None:
            dependencies = [
                "sbyb",
                "numpy>=1.20.0",
                "pandas>=1.3.0",
                "scikit-learn>=1.0.0"
            ]
        
        # Default dev dependencies
        if dev_dependencies is None:
            dev_dependencies = [
                "pytest>=6.0.0",
                "black>=21.9b0",
                "isort>=5.9.0",
                "flake8>=4.0.0"
            ]
        
        # Create pyproject.toml content
        pyproject = {
            "build-system": {
                "requires": ["setuptools>=42", "wheel"],
                "build-backend": "setuptools.build_meta"
            },
            "tool": {
                "black": {
                    "line-length": 88
                },
                "isort": {
                    "profile": "black"
                }
            },
            "project": {
                "name": package_name,
                "version": version,
                "description": description,
                "authors": [
                    {
                        "name": author,
                        "email": author_email
                    }
                ],
                "requires-python": requires_python,
                "dependencies": dependencies,
                "optional-dependencies": {
                    "dev": dev_dependencies
                }
            }
        }
        
        # Write pyproject.toml file
        with open(output_path, "w") as f:
            toml.dump(pyproject, f)
        
        return output_path
    
    def generate_dockerfile(self, output_path: str, 
                           base_image: str = "python:3.9-slim",
                           working_dir: str = "/app",
                           requirements_path: str = "requirements.txt",
                           entrypoint: Optional[str] = None,
                           cmd: Optional[str] = None,
                           expose_port: Optional[int] = None,
                           env_vars: Optional[Dict[str, str]] = None) -> str:
        """
        Generate Dockerfile for containerizing the application.
        
        Args:
            output_path: Path to save the Dockerfile.
            base_image: Base Docker image.
            working_dir: Working directory in the container.
            requirements_path: Path to requirements.txt file.
            entrypoint: Entrypoint command.
            cmd: CMD command.
            expose_port: Port to expose.
            env_vars: Environment variables.
            
        Returns:
            Path to the generated Dockerfile.
        """
        # Start with base image
        dockerfile_content = f"FROM {base_image}\n\n"
        
        # Set working directory
        dockerfile_content += f"WORKDIR {working_dir}\n\n"
        
        # Copy requirements and install dependencies
        dockerfile_content += f"COPY {requirements_path} .\n"
        dockerfile_content += "RUN pip install --no-cache-dir -r requirements.txt\n\n"
        
        # Copy application code
        dockerfile_content += "COPY . .\n\n"
        
        # Set environment variables
        if env_vars:
            for key, value in env_vars.items():
                dockerfile_content += f"ENV {key}={value}\n"
            dockerfile_content += "\n"
        
        # Expose port
        if expose_port:
            dockerfile_content += f"EXPOSE {expose_port}\n\n"
        
        # Set entrypoint
        if entrypoint:
            dockerfile_content += f"ENTRYPOINT {entrypoint}\n"
        
        # Set cmd
        if cmd:
            dockerfile_content += f"CMD {cmd}\n"
        
        # Write Dockerfile
        with open(output_path, "w") as f:
            f.write(dockerfile_content)
        
        return output_path
    
    def generate_docker_compose(self, output_path: str, 
                               service_name: str,
                               image: Optional[str] = None,
                               build_context: Optional[str] = ".",
                               ports: Optional[List[str]] = None,
                               volumes: Optional[List[str]] = None,
                               environment: Optional[Dict[str, str]] = None,
                               depends_on: Optional[List[str]] = None,
                               networks: Optional[List[str]] = None) -> str:
        """
        Generate docker-compose.yml file.
        
        Args:
            output_path: Path to save the docker-compose.yml file.
            service_name: Name of the service.
            image: Docker image to use.
            build_context: Build context for the image.
            ports: Ports to expose.
            volumes: Volumes to mount.
            environment: Environment variables.
            depends_on: Services this service depends on.
            networks: Networks to connect to.
            
        Returns:
            Path to the generated docker-compose.yml file.
        """
        # Initialize docker-compose configuration
        compose = {
            "version": "3",
            "services": {
                service_name: {}
            }
        }
        
        # Set image or build context
        if image:
            compose["services"][service_name]["image"] = image
        else:
            compose["services"][service_name]["build"] = build_context
        
        # Set ports
        if ports:
            compose["services"][service_name]["ports"] = ports
        
        # Set volumes
        if volumes:
            compose["services"][service_name]["volumes"] = volumes
        
        # Set environment variables
        if environment:
            compose["services"][service_name]["environment"] = environment
        
        # Set dependencies
        if depends_on:
            compose["services"][service_name]["depends_on"] = depends_on
        
        # Set networks
        if networks:
            compose["services"][service_name]["networks"] = networks
            compose["networks"] = {network: {"driver": "bridge"} for network in networks}
        
        # Write docker-compose.yml file
        with open(output_path, "w") as f:
            yaml.dump(compose, f, default_flow_style=False)
        
        return output_path
    
    def generate_gitignore(self, output_path: str, 
                          include_python: bool = True,
                          include_jupyter: bool = True,
                          include_vscode: bool = True,
                          include_pycharm: bool = False,
                          include_macos: bool = True,
                          include_windows: bool = True,
                          include_linux: bool = True,
                          additional_patterns: Optional[List[str]] = None) -> str:
        """
        Generate .gitignore file.
        
        Args:
            output_path: Path to save the .gitignore file.
            include_python: Whether to include Python patterns.
            include_jupyter: Whether to include Jupyter patterns.
            include_vscode: Whether to include VS Code patterns.
            include_pycharm: Whether to include PyCharm patterns.
            include_macos: Whether to include macOS patterns.
            include_windows: Whether to include Windows patterns.
            include_linux: Whether to include Linux patterns.
            additional_patterns: Additional patterns to include.
            
        Returns:
            Path to the generated .gitignore file.
        """
        patterns = []
        
        # Python patterns
        if include_python:
            patterns.extend([
                "# Python",
                "__pycache__/",
                "*.py[cod]",
                "*$py.class",
                "*.so",
                ".Python",
                "build/",
                "develop-eggs/",
                "dist/",
                "downloads/",
                "eggs/",
                ".eggs/",
                "lib/",
                "lib64/",
                "parts/",
                "sdist/",
                "var/",
                "wheels/",
                "*.egg-info/",
                ".installed.cfg",
                "*.egg",
                "MANIFEST",
                ".env",
                ".venv",
                "env/",
                "venv/",
                "ENV/",
                "env.bak/",
                "venv.bak/",
                "pip-log.txt",
                "pip-delete-this-directory.txt",
                ".coverage",
                "htmlcov/",
                ".pytest_cache/",
                ""
            ])
        
        # Jupyter patterns
        if include_jupyter:
            patterns.extend([
                "# Jupyter Notebook",
                ".ipynb_checkpoints",
                "profile_default/",
                "ipython_config.py",
                ""
            ])
        
        # VS Code patterns
        if include_vscode:
            patterns.extend([
                "# VS Code",
                ".vscode/",
                "*.code-workspace",
                ""
            ])
        
        # PyCharm patterns
        if include_pycharm:
            patterns.extend([
                "# PyCharm",
                ".idea/",
                "*.iml",
                "*.iws",
                "*.ipr",
                ""
            ])
        
        # macOS patterns
        if include_macos:
            patterns.extend([
                "# macOS",
                ".DS_Store",
                ".AppleDouble",
                ".LSOverride",
                "Icon",
                "._*",
                ""
            ])
        
        # Windows patterns
        if include_windows:
            patterns.extend([
                "# Windows",
                "Thumbs.db",
                "ehthumbs.db",
                "Desktop.ini",
                "*.lnk",
                ""
            ])
        
        # Linux patterns
        if include_linux:
            patterns.extend([
                "# Linux",
                "*~",
                ".fuse_hidden*",
                ".directory",
                ".Trash-*",
                ".nfs*",
                ""
            ])
        
        # Add additional patterns
        if additional_patterns:
            patterns.extend(["# Custom patterns"] + additional_patterns + [""])
        
        # Write .gitignore file
        with open(output_path, "w") as f:
            f.write("\n".join(patterns))
        
        return output_path
