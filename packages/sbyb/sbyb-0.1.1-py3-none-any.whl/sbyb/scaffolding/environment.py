"""
Environment setup for SBYB Scaffolding.

This module provides functionality to set up development environments
for ML projects, including virtual environments, package installation,
and environment configuration.
"""

from typing import Any, Dict, List, Optional, Union
import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

from sbyb.core.base import SBYBComponent
from sbyb.core.config import Config
from sbyb.core.exceptions import ScaffoldingError


class EnvironmentSetup(SBYBComponent):
    """
    Environment setup for ML projects.
    
    This component provides functionality to set up development environments
    for ML projects, including virtual environments, package installation,
    and environment configuration.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the environment setup.
        
        Args:
            config: Configuration dictionary for the environment setup.
        """
        super().__init__(config)
    
    def create_virtual_env(self, output_dir: str, env_name: str = "venv",
                          python_version: Optional[str] = None) -> str:
        """
        Create a Python virtual environment.
        
        Args:
            output_dir: Directory to create the virtual environment in.
            env_name: Name of the virtual environment.
            python_version: Python version to use.
            
        Returns:
            Path to the virtual environment.
        """
        env_path = os.path.join(output_dir, env_name)
        
        # Check if virtual environment already exists
        if os.path.exists(env_path):
            raise ScaffoldingError(f"Virtual environment already exists at {env_path}")
        
        # Determine Python executable
        if python_version:
            # Try to find specific Python version
            python_cmd = f"python{python_version}"
            try:
                subprocess.run([python_cmd, "--version"], check=True, capture_output=True)
            except (subprocess.SubprocessError, FileNotFoundError):
                raise ScaffoldingError(f"Python version {python_version} not found")
        else:
            # Use current Python
            python_cmd = sys.executable
        
        # Create virtual environment
        try:
            subprocess.run([python_cmd, "-m", "venv", env_path], check=True)
        except subprocess.SubprocessError as e:
            raise ScaffoldingError(f"Failed to create virtual environment: {str(e)}")
        
        return env_path
    
    def install_requirements(self, env_path: str, requirements_path: str) -> None:
        """
        Install requirements in a virtual environment.
        
        Args:
            env_path: Path to the virtual environment.
            requirements_path: Path to the requirements.txt file.
        """
        # Determine pip executable
        if platform.system() == "Windows":
            pip_path = os.path.join(env_path, "Scripts", "pip")
        else:
            pip_path = os.path.join(env_path, "bin", "pip")
        
        # Check if pip exists
        if not os.path.exists(pip_path):
            raise ScaffoldingError(f"Pip not found in virtual environment at {pip_path}")
        
        # Check if requirements file exists
        if not os.path.exists(requirements_path):
            raise ScaffoldingError(f"Requirements file not found at {requirements_path}")
        
        # Install requirements
        try:
            subprocess.run([pip_path, "install", "-r", requirements_path], check=True)
        except subprocess.SubprocessError as e:
            raise ScaffoldingError(f"Failed to install requirements: {str(e)}")
    
    def install_package(self, env_path: str, package_name: str,
                       version: Optional[str] = None) -> None:
        """
        Install a package in a virtual environment.
        
        Args:
            env_path: Path to the virtual environment.
            package_name: Name of the package to install.
            version: Version of the package to install.
        """
        # Determine pip executable
        if platform.system() == "Windows":
            pip_path = os.path.join(env_path, "Scripts", "pip")
        else:
            pip_path = os.path.join(env_path, "bin", "pip")
        
        # Check if pip exists
        if not os.path.exists(pip_path):
            raise ScaffoldingError(f"Pip not found in virtual environment at {pip_path}")
        
        # Prepare package specification
        if version:
            package_spec = f"{package_name}=={version}"
        else:
            package_spec = package_name
        
        # Install package
        try:
            subprocess.run([pip_path, "install", package_spec], check=True)
        except subprocess.SubprocessError as e:
            raise ScaffoldingError(f"Failed to install package {package_spec}: {str(e)}")
    
    def install_development_mode(self, env_path: str, package_dir: str) -> None:
        """
        Install a package in development mode.
        
        Args:
            env_path: Path to the virtual environment.
            package_dir: Path to the package directory.
        """
        # Determine pip executable
        if platform.system() == "Windows":
            pip_path = os.path.join(env_path, "Scripts", "pip")
        else:
            pip_path = os.path.join(env_path, "bin", "pip")
        
        # Check if pip exists
        if not os.path.exists(pip_path):
            raise ScaffoldingError(f"Pip not found in virtual environment at {pip_path}")
        
        # Check if package directory exists
        if not os.path.exists(package_dir):
            raise ScaffoldingError(f"Package directory not found at {package_dir}")
        
        # Install package in development mode
        try:
            subprocess.run([pip_path, "install", "-e", package_dir], check=True)
        except subprocess.SubprocessError as e:
            raise ScaffoldingError(f"Failed to install package in development mode: {str(e)}")
    
    def create_conda_env(self, env_name: str, environment_file: str) -> str:
        """
        Create a conda environment.
        
        Args:
            env_name: Name of the conda environment.
            environment_file: Path to the environment.yml file.
            
        Returns:
            Name of the created conda environment.
        """
        # Check if conda is available
        try:
            subprocess.run(["conda", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise ScaffoldingError("Conda not found. Please install Anaconda or Miniconda.")
        
        # Check if environment file exists
        if not os.path.exists(environment_file):
            raise ScaffoldingError(f"Environment file not found at {environment_file}")
        
        # Create conda environment
        try:
            subprocess.run(["conda", "env", "create", "-n", env_name, "-f", environment_file], check=True)
        except subprocess.SubprocessError as e:
            raise ScaffoldingError(f"Failed to create conda environment: {str(e)}")
        
        return env_name
    
    def setup_jupyter_kernel(self, env_path: str, kernel_name: str,
                            display_name: Optional[str] = None) -> None:
        """
        Set up a Jupyter kernel for a virtual environment.
        
        Args:
            env_path: Path to the virtual environment.
            kernel_name: Name of the kernel.
            display_name: Display name of the kernel.
        """
        # Determine Python executable
        if platform.system() == "Windows":
            python_path = os.path.join(env_path, "Scripts", "python")
        else:
            python_path = os.path.join(env_path, "bin", "python")
        
        # Check if Python exists
        if not os.path.exists(python_path):
            raise ScaffoldingError(f"Python not found in virtual environment at {python_path}")
        
        # Set display name
        if display_name is None:
            display_name = kernel_name
        
        # Install ipykernel if not already installed
        try:
            subprocess.run([python_path, "-m", "pip", "install", "ipykernel"], check=True)
        except subprocess.SubprocessError as e:
            raise ScaffoldingError(f"Failed to install ipykernel: {str(e)}")
        
        # Set up Jupyter kernel
        try:
            subprocess.run([
                python_path, "-m", "ipykernel", "install",
                "--user", "--name", kernel_name, "--display-name", display_name
            ], check=True)
        except subprocess.SubprocessError as e:
            raise ScaffoldingError(f"Failed to set up Jupyter kernel: {str(e)}")
    
    def setup_git_repo(self, project_dir: str, init_commit: bool = True) -> None:
        """
        Set up a Git repository for a project.
        
        Args:
            project_dir: Path to the project directory.
            init_commit: Whether to create an initial commit.
        """
        # Check if git is available
        try:
            subprocess.run(["git", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise ScaffoldingError("Git not found. Please install Git.")
        
        # Check if project directory exists
        if not os.path.exists(project_dir):
            raise ScaffoldingError(f"Project directory not found at {project_dir}")
        
        # Initialize git repository
        try:
            subprocess.run(["git", "init"], check=True, cwd=project_dir)
        except subprocess.SubprocessError as e:
            raise ScaffoldingError(f"Failed to initialize git repository: {str(e)}")
        
        # Create initial commit if requested
        if init_commit:
            try:
                subprocess.run(["git", "add", "."], check=True, cwd=project_dir)
                subprocess.run(["git", "commit", "-m", "Initial commit"], check=True, cwd=project_dir)
            except subprocess.SubprocessError as e:
                raise ScaffoldingError(f"Failed to create initial commit: {str(e)}")
    
    def setup_pre_commit_hooks(self, project_dir: str) -> None:
        """
        Set up pre-commit hooks for a project.
        
        Args:
            project_dir: Path to the project directory.
        """
        # Check if pre-commit is available
        try:
            subprocess.run(["pre-commit", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise ScaffoldingError("pre-commit not found. Please install pre-commit.")
        
        # Check if project directory exists
        if not os.path.exists(project_dir):
            raise ScaffoldingError(f"Project directory not found at {project_dir}")
        
        # Create pre-commit config file
        pre_commit_config = """repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-docstrings]
"""
        
        # Write pre-commit config file
        pre_commit_path = os.path.join(project_dir, ".pre-commit-config.yaml")
        with open(pre_commit_path, "w") as f:
            f.write(pre_commit_config)
        
        # Install pre-commit hooks
        try:
            subprocess.run(["pre-commit", "install"], check=True, cwd=project_dir)
        except subprocess.SubprocessError as e:
            raise ScaffoldingError(f"Failed to install pre-commit hooks: {str(e)}")
    
    def setup_vscode_settings(self, project_dir: str) -> None:
        """
        Set up VS Code settings for a project.
        
        Args:
            project_dir: Path to the project directory.
        """
        # Check if project directory exists
        if not os.path.exists(project_dir):
            raise ScaffoldingError(f"Project directory not found at {project_dir}")
        
        # Create .vscode directory
        vscode_dir = os.path.join(project_dir, ".vscode")
        os.makedirs(vscode_dir, exist_ok=True)
        
        # Create settings.json
        settings = {
            "python.linting.enabled": True,
            "python.linting.flake8Enabled": True,
            "python.linting.pylintEnabled": False,
            "python.formatting.provider": "black",
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": True
            },
            "python.testing.pytestEnabled": True,
            "python.testing.unittestEnabled": False,
            "python.testing.nosetestsEnabled": False,
            "python.testing.pytestArgs": [
                "tests"
            ]
        }
        
        # Write settings.json
        settings_path = os.path.join(vscode_dir, "settings.json")
        with open(settings_path, "w") as f:
            import json
            json.dump(settings, f, indent=4)
        
        # Create launch.json
        launch = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Python: Current File",
                    "type": "python",
                    "request": "launch",
                    "program": "${file}",
                    "console": "integratedTerminal"
                }
            ]
        }
        
        # Write launch.json
        launch_path = os.path.join(vscode_dir, "launch.json")
        with open(launch_path, "w") as f:
            import json
            json.dump(launch, f, indent=4)
    
    def setup_project_environment(self, project_dir: str, env_type: str = "venv",
                                 python_version: Optional[str] = None,
                                 setup_git: bool = True,
                                 setup_jupyter: bool = True,
                                 setup_vscode: bool = True) -> Dict[str, Any]:
        """
        Set up a complete project environment.
        
        Args:
            project_dir: Path to the project directory.
            env_type: Type of environment to create ('venv' or 'conda').
            python_version: Python version to use.
            setup_git: Whether to set up Git.
            setup_jupyter: Whether to set up Jupyter.
            setup_vscode: Whether to set up VS Code.
            
        Returns:
            Dictionary with environment information.
        """
        # Check if project directory exists
        if not os.path.exists(project_dir):
            raise ScaffoldingError(f"Project directory not found at {project_dir}")
        
        # Get project name from directory
        project_name = os.path.basename(os.path.abspath(project_dir))
        
        # Create environment
        env_info = {}
        if env_type == "venv":
            # Create virtual environment
            env_path = self.create_virtual_env(project_dir, "venv", python_version)
            env_info["env_type"] = "venv"
            env_info["env_path"] = env_path
            
            # Install requirements if requirements.txt exists
            requirements_path = os.path.join(project_dir, "requirements.txt")
            if os.path.exists(requirements_path):
                self.install_requirements(env_path, requirements_path)
            
            # Install package in development mode if setup.py exists
            setup_path = os.path.join(project_dir, "setup.py")
            if os.path.exists(setup_path):
                self.install_development_mode(env_path, project_dir)
            
            # Set up Jupyter kernel if requested
            if setup_jupyter:
                self.setup_jupyter_kernel(env_path, project_name, f"{project_name} (venv)")
        
        elif env_type == "conda":
            # Check if environment.yml exists
            env_file = os.path.join(project_dir, "environment.yml")
            if not os.path.exists(env_file):
                raise ScaffoldingError(f"Environment file not found at {env_file}")
            
            # Create conda environment
            env_name = self.create_conda_env(project_name, env_file)
            env_info["env_type"] = "conda"
            env_info["env_name"] = env_name
            
            # Set up Jupyter kernel if requested (conda environments automatically register kernels)
        
        else:
            raise ScaffoldingError(f"Unsupported environment type: {env_type}")
        
        # Set up Git if requested
        if setup_git:
            self.setup_git_repo(project_dir)
            
            # Check if .gitignore exists, create if not
            gitignore_path = os.path.join(project_dir, ".gitignore")
            if not os.path.exists(gitignore_path):
                from sbyb.scaffolding.config import ConfigGenerator
                config_gen = ConfigGenerator()
                config_gen.generate_gitignore(gitignore_path)
        
        # Set up VS Code if requested
        if setup_vscode:
            self.setup_vscode_settings(project_dir)
        
        return env_info
