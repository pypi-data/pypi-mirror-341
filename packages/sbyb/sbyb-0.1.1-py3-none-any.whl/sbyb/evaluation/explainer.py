"""
Model explainability component for SBYB evaluation.

This module provides functionality for explaining machine learning models
using various interpretability techniques.
"""

from typing import Any, Dict, List, Optional, Union, Tuple, Callable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance, partial_dependence
from sklearn.base import BaseEstimator

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import ExplainabilityError


class ModelExplainer(SBYBComponent):
    """
    Model explainability component.
    
    This component provides various techniques for explaining machine learning models.
    """
    
    def __init__(self, task: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the model explainer.
        
        Args:
            task: Machine learning task type. If None, will be auto-detected.
            config: Configuration dictionary for the explainer.
        """
        super().__init__(config)
        self.task = task
        self.explanations = {}
        
        # Try to import optional dependencies
        try:
            import shap
            self._shap = shap
        except ImportError:
            self._shap = None
        
        try:
            import lime
            import lime.lime_tabular
            self._lime = lime
        except ImportError:
            self._lime = None
        
        try:
            import eli5
            self._eli5 = eli5
        except ImportError:
            self._eli5 = None
    
    def explain_feature_importance(self, model: BaseEstimator, X: pd.DataFrame, y: Union[pd.Series, np.ndarray],
                                  n_repeats: int = 10, random_state: int = 42) -> pd.DataFrame:
        """
        Explain model using permutation feature importance.
        
        Args:
            model: Trained model.
            X: Input features.
            y: Target variable.
            n_repeats: Number of times to permute each feature.
            random_state: Random seed.
            
        Returns:
            DataFrame with feature importance values.
        """
        # Calculate permutation importance
        result = permutation_importance(
            model, X, y, n_repeats=n_repeats, random_state=random_state
        )
        
        # Create DataFrame with results
        importance_df = pd.DataFrame({
            'feature': X.columns,
            'importance_mean': result.importances_mean,
            'importance_std': result.importances_std
        })
        
        # Sort by importance
        importance_df = importance_df.sort_values('importance_mean', ascending=False)
        
        # Store explanation
        self.explanations['feature_importance'] = importance_df
        
        return importance_df
    
    def explain_with_shap(self, model: BaseEstimator, X: pd.DataFrame, 
                         background_data: Optional[pd.DataFrame] = None,
                         n_samples: int = 100) -> Dict[str, Any]:
        """
        Explain model using SHAP (SHapley Additive exPlanations).
        
        Args:
            model: Trained model.
            X: Input features to explain.
            background_data: Background data for SHAP explainer. If None, will use X.
            n_samples: Number of samples to use for background data if subsampling.
            
        Returns:
            Dictionary with SHAP values and explainer.
        """
        if self._shap is None:
            raise ExplainabilityError("SHAP is not installed. Please install it with 'pip install shap'.")
        
        shap = self._shap
        
        # If background data is not provided, use X
        if background_data is None:
            background_data = X
        
        # Subsample background data if it's too large
        if len(background_data) > n_samples:
            background_data = background_data.sample(n_samples, random_state=42)
        
        # Try different explainers based on model type
        try:
            # First try TreeExplainer for tree-based models
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X)
            explainer_type = 'TreeExplainer'
        except Exception:
            try:
                # Then try KernelExplainer for other models
                explainer = shap.KernelExplainer(
                    model.predict if hasattr(model, 'predict') else model,
                    background_data
                )
                shap_values = explainer.shap_values(X)
                explainer_type = 'KernelExplainer'
            except Exception as e:
                raise ExplainabilityError(f"Failed to create SHAP explainer: {str(e)}")
        
        # Store explanation
        self.explanations['shap'] = {
            'explainer': explainer,
            'explainer_type': explainer_type,
            'shap_values': shap_values,
            'data': X
        }
        
        return self.explanations['shap']
    
    def explain_with_lime(self, model: BaseEstimator, X: pd.DataFrame, 
                         instance_index: int = 0,
                         num_features: int = 10,
                         categorical_features: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Explain model prediction using LIME (Local Interpretable Model-agnostic Explanations).
        
        Args:
            model: Trained model.
            X: Input features.
            instance_index: Index of the instance to explain.
            num_features: Number of features to include in the explanation.
            categorical_features: Indices of categorical features.
            
        Returns:
            Dictionary with LIME explanation.
        """
        if self._lime is None:
            raise ExplainabilityError("LIME is not installed. Please install it with 'pip install lime'.")
        
        lime = self._lime
        
        # Determine mode based on task
        if self.task is None:
            # Try to infer task from model
            if hasattr(model, 'predict_proba'):
                mode = 'classification'
            else:
                mode = 'regression'
        elif self.task in ['binary', 'multiclass']:
            mode = 'classification'
        else:
            mode = 'regression'
        
        # Create explainer
        explainer = lime.lime_tabular.LimeTabularExplainer(
            X.values,
            feature_names=X.columns.tolist(),
            class_names=None,  # Could be set for classification
            categorical_features=categorical_features,
            mode=mode
        )
        
        # Get instance to explain
        instance = X.iloc[instance_index].values
        
        # Create explanation
        if mode == 'classification' and hasattr(model, 'predict_proba'):
            explanation = explainer.explain_instance(
                instance, model.predict_proba, num_features=num_features
            )
        else:
            explanation = explainer.explain_instance(
                instance, model.predict, num_features=num_features
            )
        
        # Extract explanation data
        feature_importance = {}
        for feature, importance in explanation.as_list():
            feature_importance[feature] = importance
        
        # Store explanation
        self.explanations['lime'] = {
            'explainer': explainer,
            'explanation': explanation,
            'instance_index': instance_index,
            'feature_importance': feature_importance
        }
        
        return self.explanations['lime']
    
    def explain_with_eli5(self, model: BaseEstimator, X: pd.DataFrame) -> Dict[str, Any]:
        """
        Explain model using ELI5.
        
        Args:
            model: Trained model.
            X: Input features.
            
        Returns:
            Dictionary with ELI5 explanation.
        """
        if self._eli5 is None:
            raise ExplainabilityError("ELI5 is not installed. Please install it with 'pip install eli5'.")
        
        eli5 = self._eli5
        
        # Get explanation
        explanation = eli5.explain_weights(model, feature_names=X.columns.tolist())
        
        # Store explanation
        self.explanations['eli5'] = {
            'explanation': explanation
        }
        
        return self.explanations['eli5']
    
    def explain_partial_dependence(self, model: BaseEstimator, X: pd.DataFrame, 
                                  features: List[Union[int, str, Tuple[Union[int, str], Union[int, str]]]],
                                  grid_resolution: int = 20) -> Dict[str, Any]:
        """
        Explain model using partial dependence plots.
        
        Args:
            model: Trained model.
            X: Input features.
            features: List of features or feature pairs to compute partial dependence for.
                Can be feature names, indices, or tuples of feature names/indices for 2D plots.
            grid_resolution: Number of points in the grid.
            
        Returns:
            Dictionary with partial dependence results.
        """
        # Convert feature names to indices if needed
        feature_indices = []
        for feature in features:
            if isinstance(feature, tuple):
                # Handle 2D features
                feature_idx_1 = feature[0] if isinstance(feature[0], int) else X.columns.get_loc(feature[0])
                feature_idx_2 = feature[1] if isinstance(feature[1], int) else X.columns.get_loc(feature[1])
                feature_indices.append((feature_idx_1, feature_idx_2))
            else:
                # Handle 1D features
                feature_idx = feature if isinstance(feature, int) else X.columns.get_loc(feature)
                feature_indices.append(feature_idx)
        
        # Compute partial dependence
        pdp_results = {}
        
        for feature_idx in feature_indices:
            if isinstance(feature_idx, tuple):
                # 2D partial dependence
                feature_name_1 = X.columns[feature_idx[0]] if isinstance(feature_idx[0], int) else feature_idx[0]
                feature_name_2 = X.columns[feature_idx[1]] if isinstance(feature_idx[1], int) else feature_idx[1]
                feature_name = (feature_name_1, feature_name_2)
                
                # Compute partial dependence
                pdp = partial_dependence(
                    model, X, [feature_idx], grid_resolution=grid_resolution
                )
                
                pdp_results[str(feature_name)] = {
                    'feature': feature_name,
                    'values': pdp['values'][0],
                    'pdp': pdp['average'][0],
                    'is_2d': True
                }
            else:
                # 1D partial dependence
                feature_name = X.columns[feature_idx] if isinstance(feature_idx, int) else feature_idx
                
                # Compute partial dependence
                pdp = partial_dependence(
                    model, X, [feature_idx], grid_resolution=grid_resolution
                )
                
                pdp_results[str(feature_name)] = {
                    'feature': feature_name,
                    'values': pdp['values'][0],
                    'pdp': pdp['average'][0],
                    'is_2d': False
                }
        
        # Store explanation
        self.explanations['partial_dependence'] = pdp_results
        
        return pdp_results
    
    def plot_feature_importance(self, importance_df: Optional[pd.DataFrame] = None,
                               top_n: int = 20,
                               figsize: Tuple[int, int] = (12, 8),
                               title: str = 'Feature Importance') -> plt.Figure:
        """
        Plot feature importance.
        
        Args:
            importance_df: DataFrame with feature importance values.
                If None, will use the stored feature importance.
            top_n: Number of top features to show.
            figsize: Figure size.
            title: Plot title.
            
        Returns:
            Matplotlib figure.
        """
        # Use stored feature importance if not provided
        if importance_df is None:
            if 'feature_importance' not in self.explanations:
                raise ExplainabilityError("No feature importance data available. Call 'explain_feature_importance' first.")
            importance_df = self.explanations['feature_importance']
        
        # Sort by importance
        importance_df = importance_df.sort_values('importance_mean', ascending=False)
        
        # Take top N features
        if len(importance_df) > top_n:
            importance_df = importance_df.head(top_n)
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot horizontal bar chart with error bars
        ax.barh(importance_df['feature'], importance_df['importance_mean'], 
               xerr=importance_df['importance_std'], capsize=5)
        ax.set_title(title)
        ax.set_xlabel('Importance')
        ax.set_ylabel('Feature')
        
        # Invert y-axis to show most important features at the top
        ax.invert_yaxis()
        
        fig.tight_layout()
        
        return fig
    
    def plot_shap_summary(self, shap_values: Optional[np.ndarray] = None,
                         data: Optional[pd.DataFrame] = None,
                         max_display: int = 20,
                         plot_type: str = 'bar',
                         figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """
        Plot SHAP summary.
        
        Args:
            shap_values: SHAP values.
                If None, will use the stored SHAP values.
            data: Input features.
                If None, will use the stored data.
            max_display: Maximum number of features to display.
            plot_type: Type of plot ('bar', 'dot', or 'violin').
            figsize: Figure size.
            
        Returns:
            Matplotlib figure.
        """
        if self._shap is None:
            raise ExplainabilityError("SHAP is not installed. Please install it with 'pip install shap'.")
        
        shap = self._shap
        
        # Use stored SHAP values if not provided
        if shap_values is None or data is None:
            if 'shap' not in self.explanations:
                raise ExplainabilityError("No SHAP data available. Call 'explain_with_shap' first.")
            shap_values = self.explanations['shap']['shap_values']
            data = self.explanations['shap']['data']
        
        # Create figure
        plt.figure(figsize=figsize)
        
        # Plot SHAP summary
        if plot_type == 'bar':
            shap.summary_plot(shap_values, data, plot_type='bar', max_display=max_display, show=False)
        elif plot_type == 'dot':
            shap.summary_plot(shap_values, data, plot_type='dot', max_display=max_display, show=False)
        elif plot_type == 'violin':
            shap.summary_plot(shap_values, data, plot_type='violin', max_display=max_display, show=False)
        else:
            raise ExplainabilityError(f"Unknown plot type: {plot_type}")
        
        # Get current figure
        fig = plt.gcf()
        
        return fig
    
    def plot_shap_dependence(self, feature: Union[int, str],
                            interaction_feature: Optional[Union[int, str]] = None,
                            figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """
        Plot SHAP dependence plot.
        
        Args:
            feature: Feature to plot.
            interaction_feature: Interaction feature.
            figsize: Figure size.
            
        Returns:
            Matplotlib figure.
        """
        if self._shap is None:
            raise ExplainabilityError("SHAP is not installed. Please install it with 'pip install shap'.")
        
        shap = self._shap
        
        # Check if SHAP data is available
        if 'shap' not in self.explanations:
            raise ExplainabilityError("No SHAP data available. Call 'explain_with_shap' first.")
        
        # Get SHAP data
        shap_values = self.explanations['shap']['shap_values']
        data = self.explanations['shap']['data']
        
        # Convert feature name to index if needed
        if isinstance(feature, str):
            feature_idx = data.columns.get_loc(feature)
        else:
            feature_idx = feature
            feature = data.columns[feature_idx]
        
        # Convert interaction feature name to index if needed
        if interaction_feature is not None:
            if isinstance(interaction_feature, str):
                interaction_idx = data.columns.get_loc(interaction_feature)
            else:
                interaction_idx = interaction_feature
                interaction_feature = data.columns[interaction_idx]
        
        # Create figure
        plt.figure(figsize=figsize)
        
        # Plot SHAP dependence
        if interaction_feature is None:
            shap.dependence_plot(feature_idx, shap_values, data, show=False)
        else:
            shap.dependence_plot(feature_idx, shap_values, data, interaction_index=interaction_idx, show=False)
        
        # Get current figure
        fig = plt.gcf()
        
        return fig
    
    def plot_lime_explanation(self, explanation: Optional[Any] = None,
                             figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """
        Plot LIME explanation.
        
        Args:
            explanation: LIME explanation.
                If None, will use the stored LIME explanation.
            figsize: Figure size.
            
        Returns:
            Matplotlib figure.
        """
        # Use stored LIME explanation if not provided
        if explanation is None:
            if 'lime' not in self.explanations:
                raise ExplainabilityError("No LIME data available. Call 'explain_with_lime' first.")
            explanation = self.explanations['lime']['explanation']
        
        # Create figure
        fig = plt.figure(figsize=figsize)
        
        # Plot LIME explanation
        explanation.as_pyplot_figure(fig=fig)
        
        return fig
    
    def plot_partial_dependence(self, feature: Union[str, Tuple[str, str]],
                               figsize: Tuple[int, int] = (10, 6),
                               title: Optional[str] = None) -> plt.Figure:
        """
        Plot partial dependence.
        
        Args:
            feature: Feature or feature pair to plot.
            figsize: Figure size.
            title: Plot title.
            
        Returns:
            Matplotlib figure.
        """
        # Check if partial dependence data is available
        if 'partial_dependence' not in self.explanations:
            raise ExplainabilityError("No partial dependence data available. Call 'explain_partial_dependence' first.")
        
        # Get partial dependence data
        pdp_results = self.explanations['partial_dependence']
        
        # Convert feature to string for lookup
        feature_key = str(feature)
        
        if feature_key not in pdp_results:
            raise ExplainabilityError(f"No partial dependence data available for feature: {feature}")
        
        pdp_data = pdp_results[feature_key]
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        if pdp_data['is_2d']:
            # 2D partial dependence
            feature_name_1, feature_name_2 = pdp_data['feature']
            
            # Create meshgrid
            X, Y = np.meshgrid(pdp_data['values'][0], pdp_data['values'][1])
            
            # Plot 2D partial dependence
            contour = ax.contourf(X, Y, pdp_data['pdp'].T, cmap='viridis')
            fig.colorbar(contour, ax=ax)
            
            ax.set_xlabel(feature_name_1)
            ax.set_ylabel(feature_name_2)
            
            if title is None:
                title = f'Partial Dependence of {feature_name_1} and {feature_name_2}'
        else:
            # 1D partial dependence
            feature_name = pdp_data['feature']
            
            # Plot 1D partial dependence
            ax.plot(pdp_data['values'], pdp_data['pdp'])
            
            ax.set_xlabel(feature_name)
            ax.set_ylabel('Partial Dependence')
            
            if title is None:
                title = f'Partial Dependence of {feature_name}'
        
        ax.set_title(title)
        fig.tight_layout()
        
        return fig
    
    def _detect_task(self, y: np.ndarray) -> str:
        """
        Detect the machine learning task type from the target variable.
        
        Args:
            y: Target variable.
            
        Returns:
            Task type ('binary', 'multiclass', or 'regression').
        """
        # Check if it's classification or regression
        if np.issubdtype(y.dtype, np.number):
            n_unique = len(np.unique(y))
            
            if n_unique == 2:
                return 'binary'
            elif n_unique <= 20:  # Arbitrary threshold for multiclass
                return 'multiclass'
            else:
                return 'regression'
        else:
            # Non-numeric types are assumed to be classification
            n_unique = len(np.unique(y))
            return 'binary' if n_unique == 2 else 'multiclass'
