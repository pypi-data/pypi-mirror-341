"""
Model stacking component for SBYB AutoML.

This module provides functionality for creating stacked ensemble models
by combining multiple base models.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, clone
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import StackingError


class ModelStacker(SBYBComponent):
    """
    Model stacking component.
    
    This component creates stacked ensemble models by combining multiple base models.
    """
    
    def __init__(self, meta_learner: Optional[str] = 'auto', 
                 cv_folds: int = 5, use_features: bool = True,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the model stacker.
        
        Args:
            meta_learner: Meta-learner model type ('auto', 'linear', 'forest').
            cv_folds: Number of cross-validation folds for generating meta-features.
            use_features: Whether to include original features in the meta-learner.
            config: Configuration dictionary for the stacker.
        """
        super().__init__(config)
        
        self.meta_learner = meta_learner
        self.cv_folds = cv_folds
        self.use_features = use_features
        self.base_models = None
        self.meta_model = None
    
    def stack_models(self, models: List[BaseEstimator], X_train: pd.DataFrame, y: Union[pd.Series, np.ndarray],
                    X_val: Optional[pd.DataFrame] = None, y_val: Optional[Union[pd.Series, np.ndarray]] = None,
                    task: str = 'auto', time_limit: Optional[float] = None) -> BaseEstimator:
        """
        Create a stacked ensemble model.
        
        Args:
            models: List of base models to stack.
            X_train: Training features.
            y: Target variable.
            X_val: Validation features (optional).
            y_val: Validation target (optional).
            task: Machine learning task type ('auto', 'binary', 'multiclass', 'regression').
            time_limit: Time limit in seconds for stacking.
            
        Returns:
            Stacked ensemble model.
        """
        import time
        start_time = time.time()
        
        # Store base models
        self.base_models = models
        
        # Determine task type if auto
        if task == 'auto':
            task = self._detect_task(y)
        
        # Generate meta-features using cross-validation
        meta_features_train = self._generate_meta_features(models, X_train, y, task)
        
        # Generate meta-features for validation set if provided
        meta_features_val = None
        if X_val is not None and y_val is not None:
            # Fit base models on all training data
            fitted_models = []
            for model in models:
                fitted_model = clone(model)
                fitted_model.fit(X_train, y)
                fitted_models.append(fitted_model)
            
            # Generate predictions for validation set
            meta_features_val = np.column_stack([
                model.predict_proba(X_val)[:, 1] if task == 'binary' and hasattr(model, 'predict_proba')
                else model.predict_proba(X_val) if task == 'multiclass' and hasattr(model, 'predict_proba')
                else model.predict(X_val).reshape(-1, 1)
                for model in fitted_models
            ])
            
            # Include original features if specified
            if self.use_features:
                meta_features_val = np.column_stack([meta_features_val, X_val.values])
        
        # Create meta-learner
        meta_model = self._create_meta_learner(task)
        
        # Fit meta-learner
        meta_model.fit(meta_features_train, y)
        
        # Create and return stacked model
        stacked_model = StackedEnsemble(
            base_models=models,
            meta_model=meta_model,
            task=task,
            use_features=self.use_features
        )
        
        # Store meta-model
        self.meta_model = meta_model
        
        return stacked_model
    
    def _generate_meta_features(self, models: List[BaseEstimator], X: pd.DataFrame, 
                               y: Union[pd.Series, np.ndarray], task: str) -> np.ndarray:
        """
        Generate meta-features using cross-validation.
        
        Args:
            models: List of base models.
            X: Input features.
            y: Target variable.
            task: Machine learning task type.
            
        Returns:
            Meta-features array.
        """
        # Create cross-validation object
        if task in ['binary', 'multiclass']:
            cv = StratifiedKFold(n_splits=self.cv_folds, shuffle=True, random_state=42)
        else:
            cv = KFold(n_splits=self.cv_folds, shuffle=True, random_state=42)
        
        # Initialize meta-features array
        n_models = len(models)
        meta_features = np.zeros((X.shape[0], n_models))
        
        # Generate meta-features for each fold
        for train_idx, val_idx in cv.split(X, y):
            X_fold_train, X_fold_val = X.iloc[train_idx], X.iloc[val_idx]
            y_fold_train = y.iloc[train_idx] if isinstance(y, pd.Series) else y[train_idx]
            
            # Train each model on the fold
            for i, model in enumerate(models):
                # Clone the model to avoid modifying the original
                model_clone = clone(model)
                
                try:
                    # Fit the model
                    model_clone.fit(X_fold_train, y_fold_train)
                    
                    # Generate predictions
                    if task == 'binary' and hasattr(model_clone, 'predict_proba'):
                        # For binary classification with probability support
                        meta_features[val_idx, i] = model_clone.predict_proba(X_fold_val)[:, 1]
                    elif task == 'multiclass' and hasattr(model_clone, 'predict_proba'):
                        # For multiclass, use the predicted class (not probabilities)
                        # This is a simplification; in practice, you might want to use all class probabilities
                        meta_features[val_idx, i] = model_clone.predict(X_fold_val)
                    else:
                        # For regression or models without probability support
                        meta_features[val_idx, i] = model_clone.predict(X_fold_val)
                except Exception as e:
                    # If model fails, use zeros
                    meta_features[val_idx, i] = 0
                    print(f"Error in model {i} for fold: {str(e)}")
        
        # Include original features if specified
        if self.use_features:
            meta_features = np.column_stack([meta_features, X.values])
        
        return meta_features
    
    def _create_meta_learner(self, task: str) -> BaseEstimator:
        """
        Create a meta-learner model.
        
        Args:
            task: Machine learning task type.
            
        Returns:
            Meta-learner model.
        """
        if self.meta_learner == 'auto':
            # Choose meta-learner based on task
            if task == 'binary':
                return LogisticRegression(C=1.0, solver='lbfgs', max_iter=1000)
            elif task == 'multiclass':
                return RandomForestClassifier(n_estimators=100, random_state=42)
            else:  # regression
                return Ridge(alpha=1.0)
        
        elif self.meta_learner == 'linear':
            # Use linear models
            if task in ['binary', 'multiclass']:
                return LogisticRegression(C=1.0, solver='lbfgs', max_iter=1000)
            else:  # regression
                return Ridge(alpha=1.0)
        
        elif self.meta_learner == 'forest':
            # Use random forest
            if task in ['binary', 'multiclass']:
                return RandomForestClassifier(n_estimators=100, random_state=42)
            else:  # regression
                return RandomForestRegressor(n_estimators=100, random_state=42)
        
        else:
            raise StackingError(f"Unknown meta-learner type: {self.meta_learner}")
    
    def _detect_task(self, y: Union[pd.Series, np.ndarray]) -> str:
        """
        Detect the machine learning task type from the target variable.
        
        Args:
            y: Target variable.
            
        Returns:
            Task type ('binary', 'multiclass', or 'regression').
        """
        if isinstance(y, np.ndarray):
            y = pd.Series(y)
        
        # Check if it's classification or regression
        if pd.api.types.is_numeric_dtype(y.dtype):
            n_unique = y.nunique()
            
            if n_unique == 2:
                return 'binary'
            elif n_unique <= 20:  # Arbitrary threshold for multiclass
                return 'multiclass'
            else:
                return 'regression'
        else:
            # Non-numeric types are assumed to be classification
            return 'multiclass'


class StackedEnsemble(BaseEstimator):
    """
    Stacked ensemble model.
    
    This class represents a stacked ensemble model that combines multiple base models
    with a meta-learner.
    """
    
    def __init__(self, base_models: List[BaseEstimator], meta_model: BaseEstimator, 
                task: str, use_features: bool = True):
        """
        Initialize the stacked ensemble model.
        
        Args:
            base_models: List of base models.
            meta_model: Meta-learner model.
            task: Machine learning task type.
            use_features: Whether to include original features in the meta-learner.
        """
        self.base_models = base_models
        self.meta_model = meta_model
        self.task = task
        self.use_features = use_features
        self._is_fitted = False
    
    def fit(self, X: pd.DataFrame, y: Union[pd.Series, np.ndarray]) -> 'StackedEnsemble':
        """
        Fit the stacked ensemble model.
        
        Args:
            X: Input features.
            y: Target variable.
            
        Returns:
            self: The fitted model.
        """
        # Fit base models
        for model in self.base_models:
            model.fit(X, y)
        
        # Generate meta-features
        meta_features = self._generate_meta_features(X)
        
        # Fit meta-model
        self.meta_model.fit(meta_features, y)
        
        self._is_fitted = True
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions using the stacked ensemble model.
        
        Args:
            X: Input features.
            
        Returns:
            Predictions.
        """
        if not self._is_fitted:
            raise StackingError("Model has not been fitted yet. Call 'fit' before using 'predict'.")
        
        # Generate meta-features
        meta_features = self._generate_meta_features(X)
        
        # Make predictions with meta-model
        return self.meta_model.predict(meta_features)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict class probabilities using the stacked ensemble model.
        
        Args:
            X: Input features.
            
        Returns:
            Class probabilities.
        """
        if not self._is_fitted:
            raise StackingError("Model has not been fitted yet. Call 'fit' before using 'predict_proba'.")
        
        if self.task not in ['binary', 'multiclass']:
            raise StackingError("predict_proba is only available for classification tasks")
        
        # Check if meta-model supports probability predictions
        if not hasattr(self.meta_model, 'predict_proba'):
            raise StackingError("Meta-model does not support probability predictions")
        
        # Generate meta-features
        meta_features = self._generate_meta_features(X)
        
        # Make probability predictions with meta-model
        return self.meta_model.predict_proba(meta_features)
    
    def _generate_meta_features(self, X: pd.DataFrame) -> np.ndarray:
        """
        Generate meta-features from base models.
        
        Args:
            X: Input features.
            
        Returns:
            Meta-features array.
        """
        # Generate predictions from base models
        meta_features = np.column_stack([
            model.predict_proba(X)[:, 1] if self.task == 'binary' and hasattr(model, 'predict_proba')
            else model.predict_proba(X) if self.task == 'multiclass' and hasattr(model, 'predict_proba')
            else model.predict(X).reshape(-1, 1)
            for model in self.base_models
        ])
        
        # Include original features if specified
        if self.use_features:
            meta_features = np.column_stack([meta_features, X.values])
        
        return meta_features
