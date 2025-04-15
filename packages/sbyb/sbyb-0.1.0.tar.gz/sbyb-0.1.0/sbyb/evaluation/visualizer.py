"""
Visualization component for SBYB evaluation.

This module provides functionality for visualizing model performance and results
through various plots and charts.
"""

from typing import Any, Dict, List, Optional, Union, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, roc_curve, precision_recall_curve, 
    auc, roc_auc_score, average_precision_score
)
from sklearn.preprocessing import label_binarize
from sklearn.inspection import permutation_importance

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import VisualizationError


class ModelVisualizer(SBYBComponent):
    """
    Model visualization component.
    
    This component creates visualizations for model performance and results.
    """
    
    def __init__(self, task: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the model visualizer.
        
        Args:
            task: Machine learning task type. If None, will be auto-detected.
            config: Configuration dictionary for the visualizer.
        """
        super().__init__(config)
        self.task = task
        self.figures = {}
    
    def plot_confusion_matrix(self, y_true: Union[pd.Series, np.ndarray], 
                             y_pred: Union[pd.Series, np.ndarray],
                             normalize: bool = True,
                             class_names: Optional[List[str]] = None,
                             figsize: Tuple[int, int] = (10, 8),
                             cmap: str = 'Blues',
                             title: str = 'Confusion Matrix') -> plt.Figure:
        """
        Plot confusion matrix.
        
        Args:
            y_true: True target values.
            y_pred: Predicted target values.
            normalize: Whether to normalize the confusion matrix.
            class_names: Names of the classes.
            figsize: Figure size.
            cmap: Colormap.
            title: Plot title.
            
        Returns:
            Matplotlib figure.
        """
        # Convert to numpy arrays
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
        # Compute confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # Normalize if requested
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot heatmap
        im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.get_cmap(cmap))
        ax.figure.colorbar(im, ax=ax)
        
        # Set labels
        if class_names is None:
            class_names = [str(i) for i in range(cm.shape[0])]
        
        ax.set(xticks=np.arange(cm.shape[1]),
               yticks=np.arange(cm.shape[0]),
               xticklabels=class_names,
               yticklabels=class_names,
               title=title,
               ylabel='True label',
               xlabel='Predicted label')
        
        # Rotate the tick labels and set their alignment
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Loop over data dimensions and create text annotations
        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], fmt),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
        
        fig.tight_layout()
        
        # Store figure
        self.figures['confusion_matrix'] = fig
        
        return fig
    
    def plot_roc_curve(self, y_true: Union[pd.Series, np.ndarray], 
                      y_prob: Union[pd.Series, np.ndarray],
                      figsize: Tuple[int, int] = (10, 8),
                      title: str = 'ROC Curve') -> plt.Figure:
        """
        Plot ROC curve.
        
        Args:
            y_true: True target values.
            y_prob: Predicted probabilities.
            figsize: Figure size.
            title: Plot title.
            
        Returns:
            Matplotlib figure.
        """
        # Convert to numpy arrays
        y_true = np.array(y_true)
        y_prob = np.array(y_prob)
        
        # Determine task type if not specified
        if self.task is None:
            self.task = self._detect_task(y_true)
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        if self.task == 'binary':
            # For binary classification
            if y_prob.ndim > 1 and y_prob.shape[1] > 1:
                # If multi-dimensional, take the second column (probability of positive class)
                y_prob_pos = y_prob[:, 1]
            else:
                # Otherwise, use as is
                y_prob_pos = y_prob.ravel()
            
            # Compute ROC curve and ROC area
            fpr, tpr, _ = roc_curve(y_true, y_prob_pos)
            roc_auc = auc(fpr, tpr)
            
            # Plot ROC curve
            ax.plot(fpr, tpr, lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
            ax.plot([0, 1], [0, 1], 'k--', lw=2)
            ax.set_xlim([0.0, 1.0])
            ax.set_ylim([0.0, 1.05])
            ax.set_xlabel('False Positive Rate')
            ax.set_ylabel('True Positive Rate')
            ax.set_title(title)
            ax.legend(loc="lower right")
        
        elif self.task == 'multiclass':
            # For multiclass classification
            n_classes = y_prob.shape[1]
            
            # Binarize the labels
            y_true_bin = label_binarize(y_true, classes=np.unique(y_true))
            
            # Compute ROC curve and ROC area for each class
            fpr = {}
            tpr = {}
            roc_auc = {}
            
            for i in range(n_classes):
                fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_prob[:, i])
                roc_auc[i] = auc(fpr[i], tpr[i])
                
                # Plot ROC curve for each class
                ax.plot(fpr[i], tpr[i], lw=2,
                        label=f'ROC curve of class {i} (area = {roc_auc[i]:.2f})')
            
            ax.plot([0, 1], [0, 1], 'k--', lw=2)
            ax.set_xlim([0.0, 1.0])
            ax.set_ylim([0.0, 1.05])
            ax.set_xlabel('False Positive Rate')
            ax.set_ylabel('True Positive Rate')
            ax.set_title(title)
            ax.legend(loc="lower right")
        
        else:
            raise VisualizationError(f"ROC curve is not applicable for task type: {self.task}")
        
        fig.tight_layout()
        
        # Store figure
        self.figures['roc_curve'] = fig
        
        return fig
    
    def plot_precision_recall_curve(self, y_true: Union[pd.Series, np.ndarray], 
                                   y_prob: Union[pd.Series, np.ndarray],
                                   figsize: Tuple[int, int] = (10, 8),
                                   title: str = 'Precision-Recall Curve') -> plt.Figure:
        """
        Plot precision-recall curve.
        
        Args:
            y_true: True target values.
            y_prob: Predicted probabilities.
            figsize: Figure size.
            title: Plot title.
            
        Returns:
            Matplotlib figure.
        """
        # Convert to numpy arrays
        y_true = np.array(y_true)
        y_prob = np.array(y_prob)
        
        # Determine task type if not specified
        if self.task is None:
            self.task = self._detect_task(y_true)
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        if self.task == 'binary':
            # For binary classification
            if y_prob.ndim > 1 and y_prob.shape[1] > 1:
                # If multi-dimensional, take the second column (probability of positive class)
                y_prob_pos = y_prob[:, 1]
            else:
                # Otherwise, use as is
                y_prob_pos = y_prob.ravel()
            
            # Compute precision-recall curve and average precision
            precision, recall, _ = precision_recall_curve(y_true, y_prob_pos)
            avg_precision = average_precision_score(y_true, y_prob_pos)
            
            # Plot precision-recall curve
            ax.plot(recall, precision, lw=2, label=f'Precision-Recall curve (AP = {avg_precision:.2f})')
            ax.set_xlim([0.0, 1.0])
            ax.set_ylim([0.0, 1.05])
            ax.set_xlabel('Recall')
            ax.set_ylabel('Precision')
            ax.set_title(title)
            ax.legend(loc="lower left")
        
        elif self.task == 'multiclass':
            # For multiclass classification
            n_classes = y_prob.shape[1]
            
            # Binarize the labels
            y_true_bin = label_binarize(y_true, classes=np.unique(y_true))
            
            # Compute precision-recall curve and average precision for each class
            precision = {}
            recall = {}
            avg_precision = {}
            
            for i in range(n_classes):
                precision[i], recall[i], _ = precision_recall_curve(y_true_bin[:, i], y_prob[:, i])
                avg_precision[i] = average_precision_score(y_true_bin[:, i], y_prob[:, i])
                
                # Plot precision-recall curve for each class
                ax.plot(recall[i], precision[i], lw=2,
                        label=f'P-R curve of class {i} (AP = {avg_precision[i]:.2f})')
            
            ax.set_xlim([0.0, 1.0])
            ax.set_ylim([0.0, 1.05])
            ax.set_xlabel('Recall')
            ax.set_ylabel('Precision')
            ax.set_title(title)
            ax.legend(loc="lower left")
        
        else:
            raise VisualizationError(f"Precision-recall curve is not applicable for task type: {self.task}")
        
        fig.tight_layout()
        
        # Store figure
        self.figures['precision_recall_curve'] = fig
        
        return fig
    
    def plot_feature_importance(self, feature_importance: Union[pd.DataFrame, Dict[str, float], np.ndarray],
                               feature_names: Optional[List[str]] = None,
                               top_n: int = 20,
                               figsize: Tuple[int, int] = (12, 8),
                               title: str = 'Feature Importance') -> plt.Figure:
        """
        Plot feature importance.
        
        Args:
            feature_importance: Feature importance values.
            feature_names: Names of the features.
            top_n: Number of top features to show.
            figsize: Figure size.
            title: Plot title.
            
        Returns:
            Matplotlib figure.
        """
        # Convert to DataFrame if not already
        if isinstance(feature_importance, dict):
            feature_importance = pd.DataFrame({
                'feature': list(feature_importance.keys()),
                'importance': list(feature_importance.values())
            })
        elif isinstance(feature_importance, np.ndarray):
            if feature_names is None:
                feature_names = [f'Feature {i}' for i in range(len(feature_importance))]
            feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': feature_importance
            })
        
        # Sort by importance
        feature_importance = feature_importance.sort_values('importance', ascending=False)
        
        # Take top N features
        if len(feature_importance) > top_n:
            feature_importance = feature_importance.head(top_n)
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot horizontal bar chart
        sns.barplot(x='importance', y='feature', data=feature_importance, ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Importance')
        ax.set_ylabel('Feature')
        
        fig.tight_layout()
        
        # Store figure
        self.figures['feature_importance'] = fig
        
        return fig
    
    def plot_residuals(self, y_true: Union[pd.Series, np.ndarray], 
                      y_pred: Union[pd.Series, np.ndarray],
                      figsize: Tuple[int, int] = (16, 6),
                      title: str = 'Residual Analysis') -> plt.Figure:
        """
        Plot residuals for regression models.
        
        Args:
            y_true: True target values.
            y_pred: Predicted target values.
            figsize: Figure size.
            title: Plot title.
            
        Returns:
            Matplotlib figure.
        """
        # Convert to numpy arrays
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
        # Calculate residuals
        residuals = y_true - y_pred
        
        # Create figure with subplots
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        # Residuals vs Predicted
        axes[0].scatter(y_pred, residuals, alpha=0.5)
        axes[0].axhline(y=0, color='r', linestyle='-')
        axes[0].set_title('Residuals vs Predicted')
        axes[0].set_xlabel('Predicted Values')
        axes[0].set_ylabel('Residuals')
        
        # Histogram of residuals
        axes[1].hist(residuals, bins=30, alpha=0.7, color='blue', edgecolor='black')
        axes[1].axvline(x=0, color='r', linestyle='-')
        axes[1].set_title('Histogram of Residuals')
        axes[1].set_xlabel('Residual Value')
        axes[1].set_ylabel('Frequency')
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(residuals, plot=axes[2])
        axes[2].set_title('Q-Q Plot')
        
        fig.suptitle(title, fontsize=16)
        fig.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust for suptitle
        
        # Store figure
        self.figures['residuals'] = fig
        
        return fig
    
    def plot_learning_curve(self, train_sizes: np.ndarray, train_scores: np.ndarray, 
                           test_scores: np.ndarray,
                           figsize: Tuple[int, int] = (10, 6),
                           title: str = 'Learning Curve') -> plt.Figure:
        """
        Plot learning curve.
        
        Args:
            train_sizes: Training set sizes.
            train_scores: Training scores for each training size.
            test_scores: Test scores for each training size.
            figsize: Figure size.
            title: Plot title.
            
        Returns:
            Matplotlib figure.
        """
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Calculate mean and std for train and test scores
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        
        # Plot learning curve
        ax.grid()
        ax.fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1, color="r")
        ax.fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1, color="g")
        ax.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training score")
        ax.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation score")
        ax.set_title(title)
        ax.set_xlabel("Training examples")
        ax.set_ylabel("Score")
        ax.legend(loc="best")
        
        fig.tight_layout()
        
        # Store figure
        self.figures['learning_curve'] = fig
        
        return fig
    
    def plot_validation_curve(self, param_range: np.ndarray, train_scores: np.ndarray, 
                             test_scores: np.ndarray, param_name: str,
                             figsize: Tuple[int, int] = (10, 6),
                             title: str = 'Validation Curve') -> plt.Figure:
        """
        Plot validation curve.
        
        Args:
            param_range: Parameter values.
            train_scores: Training scores for each parameter value.
            test_scores: Test scores for each parameter value.
            param_name: Name of the parameter.
            figsize: Figure size.
            title: Plot title.
            
        Returns:
            Matplotlib figure.
        """
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Calculate mean and std for train and test scores
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        
        # Plot validation curve
        ax.grid()
        ax.fill_between(param_range, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1, color="r")
        ax.fill_between(param_range, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1, color="g")
        ax.plot(param_range, train_scores_mean, 'o-', color="r", label="Training score")
        ax.plot(param_range, test_scores_mean, 'o-', color="g", label="Cross-validation score")
        ax.set_title(title)
        ax.set_xlabel(param_name)
        ax.set_ylabel("Score")
        ax.legend(loc="best")
        
        # If param_range is logarithmic, use log scale
        if np.all(np.diff(np.log(param_range)) > 0):
            ax.set_xscale('log')
        
        fig.tight_layout()
        
        # Store figure
        self.figures['validation_curve'] = fig
        
        return fig
    
    def plot_cluster_analysis(self, X: Union[pd.DataFrame, np.ndarray], 
                             labels: Union[pd.Series, np.ndarray],
                             figsize: Tuple[int, int] = (16, 6),
                             title: str = 'Cluster Analysis') -> plt.Figure:
        """
        Plot cluster analysis for clustering models.
        
        Args:
            X: Input features.
            labels: Cluster labels.
            figsize: Figure size.
            title: Plot title.
            
        Returns:
            Matplotlib figure.
        """
        # Convert to numpy arrays
        X = np.array(X)
        labels = np.array(labels)
        
        # Create figure with subplots
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        # If more than 2 dimensions, use PCA to reduce to 2D
        if X.shape[1] > 2:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=2)
            X_2d = pca.fit_transform(X)
            explained_var = pca.explained_variance_ratio_
            axes[0].set_title(f'PCA Projection\nExplained variance: {sum(explained_var):.2f}')
        else:
            X_2d = X
            axes[0].set_title('Data Projection')
        
        # Scatter plot of clusters
        unique_labels = np.unique(labels)
        colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))
        
        for i, label in enumerate(unique_labels):
            mask = labels == label
            axes[0].scatter(X_2d[mask, 0], X_2d[mask, 1], color=colors[i], alpha=0.7, label=f'Cluster {label}')
        
        axes[0].set_xlabel('Dimension 1')
        axes[0].set_ylabel('Dimension 2')
        axes[0].legend()
        
        # Cluster sizes
        cluster_sizes = np.bincount(labels.astype(int))
        axes[1].bar(range(len(cluster_sizes)), cluster_sizes, color=colors)
        axes[1].set_title('Cluster Sizes')
        axes[1].set_xlabel('Cluster')
        axes[1].set_ylabel('Size')
        axes[1].set_xticks(range(len(cluster_sizes)))
        axes[1].set_xticklabels([f'{i}' for i in range(len(cluster_sizes))])
        
        # Silhouette analysis
        try:
            from sklearn.metrics import silhouette_samples
            silhouette_vals = silhouette_samples(X, labels)
            
            # Sort by cluster and silhouette value
            indices = np.argsort(labels)
            sorted_labels = labels[indices]
            sorted_silhouette = silhouette_vals[indices]
            
            # Plot silhouette
            y_lower = 10
            for i, label in enumerate(unique_labels):
                cluster_silhouette = sorted_silhouette[sorted_labels == label]
                cluster_silhouette.sort()
                size = cluster_silhouette.shape[0]
                y_upper = y_lower + size
                
                axes[2].fill_betweenx(np.arange(y_lower, y_upper), 0, cluster_silhouette,
                                     alpha=0.7, color=colors[i])
                
                # Label the silhouette plots with cluster numbers
                axes[2].text(-0.05, y_lower + 0.5 * size, str(label))
                
                # Compute new y_lower for next plot
                y_lower = y_upper + 10
            
            axes[2].set_title('Silhouette Analysis')
            axes[2].set_xlabel('Silhouette coefficient')
            axes[2].set_ylabel('Cluster')
            axes[2].axvline(x=np.mean(silhouette_vals), color='red', linestyle='--')
            axes[2].set_yticks([])
            axes[2].set_xlim([-0.1, 1])
        except Exception as e:
            axes[2].text(0.5, 0.5, f"Silhouette analysis failed:\n{str(e)}", 
                        ha='center', va='center', transform=axes[2].transAxes)
        
        fig.suptitle(title, fontsize=16)
        fig.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust for suptitle
        
        # Store figure
        self.figures['cluster_analysis'] = fig
        
        return fig
    
    def save_figures(self, output_dir: str, format: str = 'png', dpi: int = 300) -> Dict[str, str]:
        """
        Save all figures to files.
        
        Args:
            output_dir: Output directory.
            format: File format (png, pdf, svg, etc.).
            dpi: Resolution in dots per inch.
            
        Returns:
            Dictionary mapping figure names to file paths.
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save each figure
        file_paths = {}
        for name, fig in self.figures.items():
            file_path = os.path.join(output_dir, f"{name}.{format}")
            fig.savefig(file_path, format=format, dpi=dpi, bbox_inches='tight')
            file_paths[name] = file_path
        
        return file_paths
    
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
