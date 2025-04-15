"""
Hyperparameter optimization component for SBYB AutoML.

This module provides functionality for optimizing hyperparameters of machine learning models
using various optimization strategies.
"""

import time
from typing import Any, Dict, List, Optional, Tuple, Union, Callable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.model_selection import cross_val_score, KFold, StratifiedKFold

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import OptimizationError


class HyperparameterOptimizer(SBYBComponent):
    """
    Hyperparameter optimization component.
    
    This component optimizes hyperparameters of machine learning models using
    various optimization strategies.
    """
    
    def __init__(self, n_trials: int = 50, early_stopping: bool = True, 
                 strategy: str = 'bayesian', config: Optional[Dict[str, Any]] = None):
        """
        Initialize the hyperparameter optimizer.
        
        Args:
            n_trials: Number of optimization trials.
            early_stopping: Whether to use early stopping.
            strategy: Optimization strategy ('bayesian', 'random', 'grid').
            config: Configuration dictionary for the optimizer.
        """
        super().__init__(config)
        
        self.n_trials = n_trials
        self.early_stopping = early_stopping
        self.strategy = strategy
        
        # Import optimization libraries lazily to avoid dependencies if not used
        self._optuna = None
        self._hyperopt = None
    
    def optimize(self, model_class: type, X: pd.DataFrame, y: Union[pd.Series, np.ndarray], 
                task: str, default_params: Dict[str, Any], scoring: Union[str, Dict[str, float]], 
                cv: int = 5, time_limit: Optional[float] = None) -> Tuple[Dict[str, Any], float]:
        """
        Optimize hyperparameters for a model.
        
        Args:
            model_class: Model class to optimize.
            X: Input features.
            y: Target variable.
            task: Machine learning task type.
            default_params: Default hyperparameters for the model.
            scoring: Scoring metric(s) to optimize.
            cv: Number of cross-validation folds.
            time_limit: Time limit in seconds for optimization.
            
        Returns:
            Tuple of (best_params, best_score).
        """
        # Choose optimization strategy
        if self.strategy == 'bayesian':
            return self._bayesian_optimization(
                model_class, X, y, task, default_params, scoring, cv, time_limit
            )
        elif self.strategy == 'random':
            return self._random_search(
                model_class, X, y, task, default_params, scoring, cv, time_limit
            )
        elif self.strategy == 'grid':
            return self._grid_search(
                model_class, X, y, task, default_params, scoring, cv, time_limit
            )
        else:
            raise OptimizationError(f"Unknown optimization strategy: {self.strategy}")
    
    def _bayesian_optimization(self, model_class: type, X: pd.DataFrame, y: Union[pd.Series, np.ndarray], 
                              task: str, default_params: Dict[str, Any], scoring: Union[str, Dict[str, float]], 
                              cv: int = 5, time_limit: Optional[float] = None) -> Tuple[Dict[str, Any], float]:
        """
        Optimize hyperparameters using Bayesian optimization.
        
        Args:
            model_class: Model class to optimize.
            X: Input features.
            y: Target variable.
            task: Machine learning task type.
            default_params: Default hyperparameters for the model.
            scoring: Scoring metric(s) to optimize.
            cv: Number of cross-validation folds.
            time_limit: Time limit in seconds for optimization.
            
        Returns:
            Tuple of (best_params, best_score).
        """
        # Import optuna lazily
        if self._optuna is None:
            try:
                import optuna
                self._optuna = optuna
            except ImportError:
                # Fall back to random search if optuna is not available
                print("Optuna not available, falling back to random search")
                return self._random_search(
                    model_class, X, y, task, default_params, scoring, cv, time_limit
                )
        
        optuna = self._optuna
        
        # Define parameter search space
        param_space = self._get_param_space(model_class, default_params)
        
        # Create cross-validation object
        if task in ['binary', 'multiclass']:
            cv_obj = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
        else:
            cv_obj = KFold(n_splits=cv, shuffle=True, random_state=42)
        
        # Define objective function
        def objective(trial):
            # Sample parameters
            params = {}
            for param_name, param_info in param_space.items():
                param_type = param_info['type']
                
                if param_type == 'categorical':
                    params[param_name] = trial.suggest_categorical(
                        param_name, param_info['values']
                    )
                elif param_type == 'int':
                    params[param_name] = trial.suggest_int(
                        param_name, param_info['low'], param_info['high'], 
                        log=param_info.get('log', False)
                    )
                elif param_type == 'float':
                    params[param_name] = trial.suggest_float(
                        param_name, param_info['low'], param_info['high'], 
                        log=param_info.get('log', False)
                    )
                elif param_type == 'bool':
                    params[param_name] = trial.suggest_categorical(
                        param_name, [True, False]
                    )
            
            # Add fixed parameters
            for param_name, param_value in default_params.items():
                if param_name not in param_space:
                    params[param_name] = param_value
            
            # Create and evaluate model
            try:
                model = model_class(**params)
                scores = cross_val_score(
                    model, X, y, cv=cv_obj, scoring=scoring, n_jobs=-1
                )
                return scores.mean()
            except Exception as e:
                # Return a poor score for failed trials
                return float('-inf')
        
        # Create study
        study = optuna.create_study(direction='maximize')
        
        # Run optimization
        try:
            if time_limit is not None:
                study.optimize(
                    objective, n_trials=self.n_trials, timeout=time_limit,
                    callbacks=[optuna.callbacks.EarlyStopping(5)] if self.early_stopping else None
                )
            else:
                study.optimize(
                    objective, n_trials=self.n_trials,
                    callbacks=[optuna.callbacks.EarlyStopping(5)] if self.early_stopping else None
                )
        except Exception as e:
            # If optimization fails, return default parameters
            return default_params, float('-inf')
        
        # Get best parameters
        best_params = study.best_params
        
        # Add fixed parameters
        for param_name, param_value in default_params.items():
            if param_name not in best_params:
                best_params[param_name] = param_value
        
        return best_params, study.best_value
    
    def _random_search(self, model_class: type, X: pd.DataFrame, y: Union[pd.Series, np.ndarray], 
                      task: str, default_params: Dict[str, Any], scoring: Union[str, Dict[str, float]], 
                      cv: int = 5, time_limit: Optional[float] = None) -> Tuple[Dict[str, Any], float]:
        """
        Optimize hyperparameters using random search.
        
        Args:
            model_class: Model class to optimize.
            X: Input features.
            y: Target variable.
            task: Machine learning task type.
            default_params: Default hyperparameters for the model.
            scoring: Scoring metric(s) to optimize.
            cv: Number of cross-validation folds.
            time_limit: Time limit in seconds for optimization.
            
        Returns:
            Tuple of (best_params, best_score).
        """
        from sklearn.model_selection import RandomizedSearchCV
        
        # Define parameter search space
        param_space = self._get_param_distributions(model_class, default_params)
        
        # Create cross-validation object
        if task in ['binary', 'multiclass']:
            cv_obj = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
        else:
            cv_obj = KFold(n_splits=cv, shuffle=True, random_state=42)
        
        # Create and run random search
        try:
            n_iter = min(self.n_trials, 10)  # Limit number of iterations for random search
            
            search = RandomizedSearchCV(
                model_class(**default_params), param_space, n_iter=n_iter,
                cv=cv_obj, scoring=scoring, n_jobs=-1, random_state=42
            )
            
            # Run with time limit if specified
            if time_limit is not None:
                start_time = time.time()
                search.fit(X, y)
                
                # If time limit is exceeded, return best parameters found so far
                if time.time() - start_time > time_limit:
                    return search.best_params_, search.best_score_
            else:
                search.fit(X, y)
            
            return search.best_params_, search.best_score_
        
        except Exception as e:
            # If search fails, return default parameters
            return default_params, float('-inf')
    
    def _grid_search(self, model_class: type, X: pd.DataFrame, y: Union[pd.Series, np.ndarray], 
                    task: str, default_params: Dict[str, Any], scoring: Union[str, Dict[str, float]], 
                    cv: int = 5, time_limit: Optional[float] = None) -> Tuple[Dict[str, Any], float]:
        """
        Optimize hyperparameters using grid search.
        
        Args:
            model_class: Model class to optimize.
            X: Input features.
            y: Target variable.
            task: Machine learning task type.
            default_params: Default hyperparameters for the model.
            scoring: Scoring metric(s) to optimize.
            cv: Number of cross-validation folds.
            time_limit: Time limit in seconds for optimization.
            
        Returns:
            Tuple of (best_params, best_score).
        """
        from sklearn.model_selection import GridSearchCV
        
        # Define parameter search space (simplified for grid search)
        param_grid = self._get_param_grid(model_class, default_params)
        
        # Create cross-validation object
        if task in ['binary', 'multiclass']:
            cv_obj = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
        else:
            cv_obj = KFold(n_splits=cv, shuffle=True, random_state=42)
        
        # Create and run grid search
        try:
            search = GridSearchCV(
                model_class(**default_params), param_grid,
                cv=cv_obj, scoring=scoring, n_jobs=-1
            )
            
            # Run with time limit if specified
            if time_limit is not None:
                start_time = time.time()
                search.fit(X, y)
                
                # If time limit is exceeded, return best parameters found so far
                if time.time() - start_time > time_limit:
                    return search.best_params_, search.best_score_
            else:
                search.fit(X, y)
            
            return search.best_params_, search.best_score_
        
        except Exception as e:
            # If search fails, return default parameters
            return default_params, float('-inf')
    
    def _get_param_space(self, model_class: type, default_params: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Get parameter search space for Bayesian optimization.
        
        Args:
            model_class: Model class.
            default_params: Default hyperparameters.
            
        Returns:
            Parameter search space.
        """
        # Define search space based on model class
        if model_class.__name__ == 'RandomForestClassifier' or model_class.__name__ == 'RandomForestRegressor':
            return {
                'n_estimators': {'type': 'int', 'low': 50, 'high': 500, 'log': True},
                'max_depth': {'type': 'int', 'low': 3, 'high': 30},
                'min_samples_split': {'type': 'int', 'low': 2, 'high': 20},
                'min_samples_leaf': {'type': 'int', 'low': 1, 'high': 20},
                'max_features': {'type': 'categorical', 'values': ['sqrt', 'log2', None]}
            }
        
        elif model_class.__name__ == 'GradientBoostingClassifier' or model_class.__name__ == 'GradientBoostingRegressor':
            return {
                'n_estimators': {'type': 'int', 'low': 50, 'high': 500, 'log': True},
                'learning_rate': {'type': 'float', 'low': 0.01, 'high': 0.3, 'log': True},
                'max_depth': {'type': 'int', 'low': 3, 'high': 10},
                'min_samples_split': {'type': 'int', 'low': 2, 'high': 20},
                'min_samples_leaf': {'type': 'int', 'low': 1, 'high': 20},
                'subsample': {'type': 'float', 'low': 0.5, 'high': 1.0}
            }
        
        elif model_class.__name__ == 'XGBClassifier' or model_class.__name__ == 'XGBRegressor':
            return {
                'n_estimators': {'type': 'int', 'low': 50, 'high': 500, 'log': True},
                'learning_rate': {'type': 'float', 'low': 0.01, 'high': 0.3, 'log': True},
                'max_depth': {'type': 'int', 'low': 3, 'high': 10},
                'min_child_weight': {'type': 'int', 'low': 1, 'high': 10},
                'subsample': {'type': 'float', 'low': 0.5, 'high': 1.0},
                'colsample_bytree': {'type': 'float', 'low': 0.5, 'high': 1.0},
                'gamma': {'type': 'float', 'low': 0, 'high': 5}
            }
        
        elif model_class.__name__ == 'LGBMClassifier' or model_class.__name__ == 'LGBMRegressor':
            return {
                'n_estimators': {'type': 'int', 'low': 50, 'high': 500, 'log': True},
                'learning_rate': {'type': 'float', 'low': 0.01, 'high': 0.3, 'log': True},
                'num_leaves': {'type': 'int', 'low': 20, 'high': 150},
                'max_depth': {'type': 'int', 'low': 3, 'high': 10},
                'min_child_samples': {'type': 'int', 'low': 5, 'high': 100},
                'subsample': {'type': 'float', 'low': 0.5, 'high': 1.0},
                'colsample_bytree': {'type': 'float', 'low': 0.5, 'high': 1.0}
            }
        
        elif model_class.__name__ == 'CatBoostClassifier' or model_class.__name__ == 'CatBoostRegressor':
            return {
                'iterations': {'type': 'int', 'low': 50, 'high': 500, 'log': True},
                'learning_rate': {'type': 'float', 'low': 0.01, 'high': 0.3, 'log': True},
                'depth': {'type': 'int', 'low': 4, 'high': 10},
                'l2_leaf_reg': {'type': 'float', 'low': 1, 'high': 10},
                'border_count': {'type': 'int', 'low': 32, 'high': 255}
            }
        
        elif model_class.__name__ == 'LogisticRegression':
            return {
                'C': {'type': 'float', 'low': 0.001, 'high': 10.0, 'log': True},
                'penalty': {'type': 'categorical', 'values': ['l1', 'l2', 'elasticnet', 'none']},
                'solver': {'type': 'categorical', 'values': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']}
            }
        
        elif model_class.__name__ == 'SVC':
            return {
                'C': {'type': 'float', 'low': 0.001, 'high': 10.0, 'log': True},
                'kernel': {'type': 'categorical', 'values': ['linear', 'poly', 'rbf', 'sigmoid']},
                'gamma': {'type': 'categorical', 'values': ['scale', 'auto']}
            }
        
        elif model_class.__name__ == 'KNeighborsClassifier' or model_class.__name__ == 'KNeighborsRegressor':
            return {
                'n_neighbors': {'type': 'int', 'low': 3, 'high': 20},
                'weights': {'type': 'categorical', 'values': ['uniform', 'distance']},
                'p': {'type': 'int', 'low': 1, 'high': 2}
            }
        
        elif model_class.__name__ == 'DecisionTreeClassifier' or model_class.__name__ == 'DecisionTreeRegressor':
            return {
                'max_depth': {'type': 'int', 'low': 3, 'high': 20},
                'min_samples_split': {'type': 'int', 'low': 2, 'high': 20},
                'min_samples_leaf': {'type': 'int', 'low': 1, 'high': 20},
                'criterion': {'type': 'categorical', 'values': ['gini', 'entropy'] if 'Classifier' in model_class.__name__ else ['mse', 'mae']}
            }
        
        elif model_class.__name__ == 'LinearRegression':
            # LinearRegression has no hyperparameters to tune
            return {}
        
        elif model_class.__name__ == 'Ridge':
            return {
                'alpha': {'type': 'float', 'low': 0.001, 'high': 10.0, 'log': True},
                'solver': {'type': 'categorical', 'values': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga']}
            }
        
        elif model_class.__name__ == 'Lasso':
            return {
                'alpha': {'type': 'float', 'low': 0.001, 'high': 10.0, 'log': True},
                'selection': {'type': 'categorical', 'values': ['cyclic', 'random']}
            }
        
        elif model_class.__name__ == 'ElasticNet':
            return {
                'alpha': {'type': 'float', 'low': 0.001, 'high': 10.0, 'log': True},
                'l1_ratio': {'type': 'float', 'low': 0.0, 'high': 1.0},
                'selection': {'type': 'categorical', 'values': ['cyclic', 'random']}
            }
        
        elif model_class.__name__ == 'SVR':
            return {
                'C': {'type': 'float', 'low': 0.001, 'high': 10.0, 'log': True},
                'kernel': {'type': 'categorical', 'values': ['linear', 'poly', 'rbf', 'sigmoid']},
                'gamma': {'type': 'categorical', 'values': ['scale', 'auto']},
                'epsilon': {'type': 'float', 'low': 0.01, 'high': 1.0}
            }
        
        # Default empty search space
        return {}
    
    def _get_param_distributions(self, model_class: type, default_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get parameter distributions for random search.
        
        Args:
            model_class: Model class.
            default_params: Default hyperparameters.
            
        Returns:
            Parameter distributions.
        """
        from scipy.stats import uniform, loguniform, randint
        
        # Convert param space to distributions
        param_space = self._get_param_space(model_class, default_params)
        param_distributions = {}
        
        for param_name, param_info in param_space.items():
            param_type = param_info['type']
            
            if param_type == 'categorical':
                param_distributions[param_name] = param_info['values']
            elif param_type == 'int':
                if param_info.get('log', False):
                    # For log-scale integers, use randint with a wider range
                    param_distributions[param_name] = randint(param_info['low'], param_info['high'] + 1)
                else:
                    param_distributions[param_name] = randint(param_info['low'], param_info['high'] + 1)
            elif param_type == 'float':
                if param_info.get('log', False):
                    param_distributions[param_name] = loguniform(param_info['low'], param_info['high'])
                else:
                    param_distributions[param_name] = uniform(param_info['low'], param_info['high'] - param_info['low'])
            elif param_type == 'bool':
                param_distributions[param_name] = [True, False]
        
        return param_distributions
    
    def _get_param_grid(self, model_class: type, default_params: Dict[str, Any]) -> Dict[str, List[Any]]:
        """
        Get parameter grid for grid search.
        
        Args:
            model_class: Model class.
            default_params: Default hyperparameters.
            
        Returns:
            Parameter grid.
        """
        import numpy as np
        
        # Convert param space to grid
        param_space = self._get_param_space(model_class, default_params)
        param_grid = {}
        
        for param_name, param_info in param_space.items():
            param_type = param_info['type']
            
            if param_type == 'categorical':
                param_grid[param_name] = param_info['values']
            elif param_type == 'int':
                if param_info.get('log', False):
                    # For log-scale integers, use logarithmically spaced values
                    param_grid[param_name] = np.unique(np.logspace(
                        np.log10(param_info['low']), 
                        np.log10(param_info['high']), 
                        num=min(5, param_info['high'] - param_info['low'] + 1)
                    ).astype(int)).tolist()
                else:
                    # For linear-scale integers, use linearly spaced values
                    param_grid[param_name] = np.unique(np.linspace(
                        param_info['low'], 
                        param_info['high'], 
                        num=min(5, param_info['high'] - param_info['low'] + 1)
                    ).astype(int)).tolist()
            elif param_type == 'float':
                if param_info.get('log', False):
                    # For log-scale floats, use logarithmically spaced values
                    param_grid[param_name] = np.logspace(
                        np.log10(param_info['low']), 
                        np.log10(param_info['high']), 
                        num=5
                    ).tolist()
                else:
                    # For linear-scale floats, use linearly spaced values
                    param_grid[param_name] = np.linspace(
                        param_info['low'], 
                        param_info['high'], 
                        num=5
                    ).tolist()
            elif param_type == 'bool':
                param_grid[param_name] = [True, False]
        
        return param_grid
