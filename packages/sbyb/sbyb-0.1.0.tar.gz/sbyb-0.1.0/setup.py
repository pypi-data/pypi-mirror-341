from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from __init__.py
with open(os.path.join("sbyb", "__init__.py"), "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break
    else:
        version = "0.1.0"  # Default version if not found

setup(
    name="sbyb",
    version=version,
    author="SBYB Team",
    author_email="info@sbyb.ai",
    description="A comprehensive ML library that unifies the entire ML pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sbyb/sbyb",
    project_urls={
        "Bug Tracker": "https://github.com/sbyb/sbyb/issues",
        "Documentation": "https://sbyb.readthedocs.io/",
        "Source Code": "https://github.com/sbyb/sbyb",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "plotly>=5.0.0",
        "streamlit>=1.10.0",
        "dash>=2.0.0",
        "flask>=2.0.0",
        "fastapi>=0.70.0",
        "uvicorn>=0.15.0",
        "shap>=0.40.0",
        "lime>=0.2.0",
        "eli5>=0.11.0",
        "onnx>=1.10.0",
        "onnxruntime>=1.8.0",
        "tensorflow>=2.8.0",
        "pytorch>=1.10.0",
        "xgboost>=1.5.0",
        "lightgbm>=3.3.0",
        "catboost>=1.0.0",
        "optuna>=2.10.0",
        "hyperopt>=0.2.5",
        "pyyaml>=6.0",
        "tqdm>=4.62.0",
        "joblib>=1.1.0",
        "pytest>=6.2.5",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "isort",
            "mypy",
            "pytest",
            "pytest-cov",
            "sphinx",
            "sphinx-rtd-theme",
            "twine",
            "wheel",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
            "myst-parser",
        ],
        "test": [
            "pytest",
            "pytest-cov",
        ],
    },
    entry_points={
        "console_scripts": [
            "sbyb=sbyb.cli.commands:main",
        ],
    },
)
