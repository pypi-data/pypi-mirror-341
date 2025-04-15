"""
Main AutoML engine for SBYB.

This module provides the main AutoML engine that orchestrates model selection,
hyperparameter optimization, and model ensembling.
"""

import time
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.model_selection import train_test_split

from sbyb.core.base import SBYBComponent, Model
from sbyb.core.config import Config
from sbyb.core.exceptions import ModelError
from sbyb.core.utils import is_classification_target, is_regression_target
from sbyb.automl.model_selection import ModelSelector
from sbyb.automl.hyperparameter import HyperparameterOptimizer
from sbyb.automl.feature_selection import FeatureSelector
from sbyb.automl.stacking import ModelStacker


class AutoMLEngine(SBYBComponent):
    """
    AutoML engine component.
    
    This component orchestrates the entire AutoML process, including model selection,
    hyperparameter optimization, feature selection, and model stacking.
    """
    
    def __init__(self, task: Optional[str] = None, 
                 time_limit: int = 300,
                 cv_folds: int = 5,
                 scoring: Optional[Union[str, Dict[str, float]]] = None,
                 n_trials: int = 50,
                 early_stopping: bool = True,
                 models: Optional[List[str]] = None,
                 stack_models: bool = True,
                 feature_selection: bool = True,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the AutoML engine.
        
        Args:
            task: Machine learning task type. If None, will be auto-detected.
            time_limit: Time limit in seconds for the AutoML process.
            cv_folds: Number of cross-validation folds.
            scoring: Scoring metric(s) to optimize. If None, will be selected based on the task.
                Can be a string for a single metric or a dictionary mapping metric names to weights.
            n_trials: Number of hyperparameter optimization trials.
            early_stopping: Whether to use early stopping for hyperparameter optimization.
            models: List of model names to consider. If None, all suitable models will be used.
            stack_models: Whether to use model stacking.
            feature_selection: Whether to perform feature selection.
            config: Configuration dictionary for the AutoML engine.
        """
        super().__init__(config)
        
        # Store parameters
        self.task = task
        self.time_limit = time_limit
        self.cv_folds = cv_folds
        self.scoring = scoring
        self.n_trials = n_trials
        self.early_stopping = early_stopping
        self.models = models
        self.stack_models = stack_models
        self.feature_selection = feature_selection
        
        # Initialize components
        self.model_selector = ModelSelector(config=config)
        self.hyperparameter_optimizer = HyperparameterOptimizer(
            n_trials=n_trials,
            early_stopping=early_stopping,
            config=config
        )
        self.feature_selector = FeatureSelector(config=config) if feature_selection else None
        self.model_stacker = ModelStacker(config=config) if stack_models else None
        
        # Results storage
        self.best_model = None
        self.best_score = None
        self.feature_importance = None
        self.leaderboard = None
        self.training_time = None
        self.selected_features = None
    
    def fit(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray], 
            task: Optional[str] = None, **kwargs) -> 'AutoMLEngine':
        """
        Run the AutoML process to find the best model.
        
        Args:
            X: Input features.
            y: Target variable.
            task: Machine learning task type. If None, will use the task specified in the constructor
                or auto-detect it.
            **kwargs: Additional keyword arguments.
            
        Returns:
            self: The fitted AutoML engine.
        """
        start_time = time.time()
        
        # Convert to pandas DataFrame/Series if numpy arrays
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
        if isinstance(y, np.ndarray):
            y = pd.Series(y)
        
        # Determine the task if not specified
        if task is not None:
            self.task = task
        elif self.task is None:
            self.task = self._detect_task(y)
        
        # Select scoring metric if not specified
        if self.scoring is None:
            self.scoring = self._select_default_scoring()
        
        # Split data for evaluation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, 
            stratify=y if self.task in ['binary', 'multiclass'] else None
        )
        
        # Feature selection if enabled
        if self.feature_selection and self.feature_selector:
            X_train, X_val, self.selected_features = self.feature_selector.select_features(
                X_train, X_val, y_train, self.task
            )
        
        # Select candidate models
        candidate_models = self.model_selector.select_models(
            self.task, models=self.models
        )
        
        # Optimize each model
        optimized_models = []
        model_scores = []
        
        remaining_time = self.time_limit - (time.time() - start_time)
        if remaining_time <= 0:
            raise ModelError("Time limit exceeded before model optimization could start")
        
        # Allocate time for each model
        time_per_model = remaining_time / len(candidate_models)
        
        for model_name, model_class, default_params in candidate_models:
            model_start_time = time.time()
            
            try:
                # Optimize hyperparameters
                best_params, best_score = self.hyperparameter_optimizer.optimize(
                    model_class, X_train, y_train, self.task, 
                    default_params=default_params,
                    scoring=self.scoring,
                    cv=self.cv_folds,
                    time_limit=time_per_model
                )
                
                # Create and fit the model with best parameters
                model = model_class(**best_params)
                model.fit(X_train, y_train)
                
                # Evaluate on validation set
                val_score = self._evaluate_model(model, X_val, y_val)
                
                optimized_models.append((model_name, model, best_params))
                model_scores.append(val_score)
                
            except Exception as e:
                # Log the error but continue with other models
                print(f"Error optimizing {model_name}: {str(e)}")
                continue
            
            # Check if time limit is exceeded
            if time.time() - start_time >= self.time_limit:
                break
        
        # Create leaderboard
        self.leaderboard = pd.DataFrame({
            'model': [m[0] for m in optimized_models],
            'score': model_scores
        })
        self.leaderboard = self.leaderboard.sort_values('score', ascending=False).reset_index(drop=True)
        
        # Stack models if enabled and we have multiple models
        if self.stack_models and self.model_stacker and len(optimized_models) > 1:
            try:
                remaining_time = self.time_limit - (time.time() - start_time)
                if remaining_time > 0:
                    stacked_model = self.model_stacker.stack_models(
                        [m[1] for m in optimized_models], 
                        X_train, y_train, X_val, y_val,
                        self.task,
                        time_limit=remaining_time
                    )
                    
                    # Evaluate stacked model
                    stacked_score = self._evaluate_model(stacked_model, X_val, y_val)
                    
                    # Add to leaderboard
                    self.leaderboard = pd.concat([
                        pd.DataFrame({'model': ['Stacked Ensemble'], 'score': [stacked_score]}),
                        self.leaderboard
                    ]).reset_index(drop=True)
                    
                    # Update best model if stacked model is better
                    if stacked_score > model_scores[0]:
                        self.best_model = stacked_model
                        self.best_score = stacked_score
                    else:
                        self.best_model = optimized_models[0][1]
                        self.best_score = model_scores[0]
                else:
                    # If no time left for stacking, use the best individual model
                    self.best_model = optimized_models[0][1]
                    self.best_score = model_scores[0]
            except Exception as e:
                # If stacking fails, use the best individual model
                print(f"Error in model stacking: {str(e)}")
                self.best_model = optimized_models[0][1]
                self.best_score = model_scores[0]
        else:
            # Use the best individual model
            self.best_model = optimized_models[0][1]
            self.best_score = model_scores[0]
        
        # Calculate feature importance if possible
        self.feature_importance = self._calculate_feature_importance(X)
        
        # Record total training time
        self.training_time = time.time() - start_time
        
        return self
    
    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Make predictions using the best model.
        
        Args:
            X: Input features.
            
        Returns:
            Predictions.
        """
        if self.best_model is None:
            raise ModelError("Model has not been fitted yet. Call 'fit' before using 'predict'.")
        
        # Convert to pandas DataFrame if numpy array
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
        
        # Apply feature selection if used during training
        if self.selected_features is not None:
            X = X[self.selected_features]
        
        return self.best_model.predict(X)
    
    def predict_proba(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Predict class probabilities using the best model (for classification tasks).
        
        Args:
            X: Input features.
            
        Returns:
            Class probabilities.
        """
        if self.best_model is None:
            raise ModelError("Model has not been fitted yet. Call 'fit' before using 'predict_proba'.")
        
        if self.task not in ['binary', 'multiclass']:
            raise ModelError("predict_proba is only available for classification tasks")
        
        # Convert to pandas DataFrame if numpy array
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
        
        # Apply feature selection if used during training
        if self.selected_features is not None:
            X = X[self.selected_features]
        
        # Check if the model has predict_proba method
        if hasattr(self.best_model, 'predict_proba'):
            return self.best_model.predict_proba(X)
        else:
            raise ModelError("The best model does not support probability predictions")
    
    def get_leaderboard(self) -> pd.DataFrame:
        """
        Get the leaderboard of models.
        
        Returns:
            DataFrame with model names and scores.
        """
        if self.leaderboard is None:
            raise ModelError("AutoML has not been run yet. Call 'fit' first.")
        
        return self.leaderboard
    
    def get_feature_importance(self) -> Optional[pd.DataFrame]:
        """
        Get feature importance.
        
        Returns:
            DataFrame with feature names and importance scores, or None if not available.
        """
        return self.feature_importance
    
    def get_best_model(self) -> BaseEstimator:
        """
        Get the best model.
        
        Returns:
            The best model found by AutoML.
        """
        if self.best_model is None:
            raise ModelError("AutoML has not been run yet. Call 'fit' first.")
        
        return self.best_model
    
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
        
        if is_classification_target(y):
            n_classes = y.nunique()
            return 'binary' if n_classes == 2 else 'multiclass'
        elif is_regression_target(y):
            return 'regression'
        else:
            raise ModelError("Could not automatically detect task type from target variable")
    
    def _select_default_scoring(self) -> Union[str, Dict[str, float]]:
        """
        Select default scoring metric based on the task.
        
        Returns:
            Scoring metric name or dictionary.
        """
        if self.task == 'binary':
            return 'roc_auc'
        elif self.task == 'multiclass':
            return 'accuracy'
        elif self.task == 'regression':
            return 'neg_root_mean_squared_error'
        else:
            return 'accuracy'  # Default
    
    def _evaluate_model(self, model: BaseEstimator, X: pd.DataFrame, y: Union[pd.Series, np.ndarray]) -> float:
        """
        Evaluate a model on validation data.
        
        Args:
            model: Fitted model to evaluate.
            X: Validation features.
            y: Validation target.
            
        Returns:
            Evaluation score.
        """
        from sklearn.metrics import (
            accuracy_score, roc_auc_score, f1_score, 
            mean_squared_error, mean_absolute_error, r2_score
        )
        
        # Make predictions
        if self.task in ['binary', 'multiclass']:
            y_pred = model.predict(X)
            
            # For binary classification with probability support, use ROC AUC
            if self.task == 'binary' and hasattr(model, 'predict_proba'):
                try:
                    y_prob = model.predict_proba(X)[:, 1]
                    return roc_auc_score(y, y_prob)
                except:
                    # Fall back to accuracy if ROC AUC fails
                    return accuracy_score(y, y_pred)
            
            # For multiclass, use accuracy
            return accuracy_score(y, y_pred)
        
        elif self.task == 'regression':
            y_pred = model.predict(X)
            
            # Use negative RMSE (higher is better)
            return -np.sqrt(mean_squared_error(y, y_pred))
        
        else:
            raise ModelError(f"Unsupported task type for evaluation: {self.task}")
    
    def _calculate_feature_importance(self, X: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Calculate feature importance from the best model if available.
        
        Args:
            X: Input features.
            
        Returns:
            DataFrame with feature names and importance scores, or None if not available.
        """
        if self.best_model is None:
            return None
        
        # Get feature names
        feature_names = X.columns if self.selected_features is None else self.selected_features
        
        # Try different methods to get feature importance
        if hasattr(self.best_model, 'feature_importances_'):
            # For tree-based models
            importances = self.best_model.feature_importances_
            return pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            }).sort_values('importance', ascending=False).reset_index(drop=True)
        
        elif hasattr(self.best_model, 'coef_'):
            # For linear models
            if self.task in ['binary', 'regression']:
                importances = np.abs(self.best_model.coef_)
                if importances.ndim > 1:
                    importances = importances.mean(axis=0)
                return pd.DataFrame({
                    'feature': feature_names,
                    'importance': importances
                }).sort_values('importance', ascending=False).reset_index(drop=True)
            
            elif self.task == 'multiclass':
                importances = np.abs(self.best_model.coef_).mean(axis=0)
                return pd.DataFrame({
                    'feature': feature_names,
                    'importance': importances
                }).sort_values('importance', ascending=False).reset_index(drop=True)
        
        # For ensemble models, try to get feature importance from base estimators
        elif hasattr(self.best_model, 'estimators_'):
            try:
                # For voting/stacking ensembles, use the first estimator that has feature importance
                for estimator in self.best_model.estimators_:
                    if hasattr(estimator, 'feature_importances_'):
                        importances = estimator.feature_importances_
                        return pd.DataFrame({
                            'feature': feature_names,
                            'importance': importances
                        }).sort_values('importance', ascending=False).reset_index(drop=True)
                    
                    elif hasattr(estimator, 'coef_'):
                        importances = np.abs(estimator.coef_)
                        if importances.ndim > 1:
                            importances = importances.mean(axis=0)
                        return pd.DataFrame({
                            'feature': feature_names,
                            'importance': importances
                        }).sort_values('importance', ascending=False).reset_index(drop=True)
            except:
                pass
        
        return None
