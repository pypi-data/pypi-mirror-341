"""
Visualization tools for SBYB EDA.

This module provides functionality to create interactive and static visualizations
for exploratory data analysis.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import datetime
import warnings

from sbyb.core.base import SBYBComponent
from sbyb.core.config import Config


class Visualizer(SBYBComponent):
    """
    Visualization tools for exploratory data analysis.
    
    This component provides functionality to create interactive and static visualizations
    for exploratory data analysis.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the visualizer.
        
        Args:
            config: Configuration dictionary for the visualizer.
        """
        super().__init__(config)
        
        # Set default style
        plt.style.use('seaborn-whitegrid')
        sns.set_style('whitegrid')
        
        # Configure default figure size
        plt.rcParams['figure.figsize'] = (12, 8)
        
        # Suppress warnings
        warnings.filterwarnings('ignore')
    
    def plot_histogram(self, data: pd.DataFrame, column: str, bins: int = 30,
                      kde: bool = True, title: Optional[str] = None,
                      color: str = 'skyblue', figsize: Tuple[int, int] = (12, 8),
                      output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot histogram for a numeric column.
        
        Args:
            data: DataFrame containing the data.
            column: Column to plot.
            bins: Number of bins for the histogram.
            kde: Whether to include KDE plot.
            title: Title for the plot.
            color: Color for the histogram.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        if column not in data.columns:
            raise ValueError(f"Column '{column}' not found in the DataFrame")
        
        if not pd.api.types.is_numeric_dtype(data[column]):
            raise ValueError(f"Column '{column}' is not numeric")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot histogram
        sns.histplot(data[column].dropna(), bins=bins, kde=kde, color=color, ax=ax)
        
        # Set title
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(f'Distribution of {column}', fontsize=14)
        
        # Set labels
        ax.set_xlabel(column, fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add statistics
        stats_text = (
            f"Mean: {data[column].mean():.2f}\n"
            f"Median: {data[column].median():.2f}\n"
            f"Std Dev: {data[column].std():.2f}\n"
            f"Min: {data[column].min():.2f}\n"
            f"Max: {data[column].max():.2f}"
        )
        
        # Add text box with statistics
        props = dict(boxstyle='round', facecolor='white', alpha=0.7)
        ax.text(0.05, 0.95, stats_text, transform=ax.transAxes, fontsize=10,
               verticalalignment='top', bbox=props)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_boxplot(self, data: pd.DataFrame, column: str, by: Optional[str] = None,
                    title: Optional[str] = None, color: str = 'skyblue',
                    figsize: Tuple[int, int] = (12, 8),
                    output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot boxplot for a numeric column.
        
        Args:
            data: DataFrame containing the data.
            column: Column to plot.
            by: Column to group by.
            title: Title for the plot.
            color: Color for the boxplot.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        if column not in data.columns:
            raise ValueError(f"Column '{column}' not found in the DataFrame")
        
        if not pd.api.types.is_numeric_dtype(data[column]):
            raise ValueError(f"Column '{column}' is not numeric")
        
        if by is not None and by not in data.columns:
            raise ValueError(f"Column '{by}' not found in the DataFrame")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot boxplot
        if by is None:
            sns.boxplot(x=data[column].dropna(), color=color, ax=ax)
            
            # Set title
            if title:
                ax.set_title(title, fontsize=14)
            else:
                ax.set_title(f'Boxplot of {column}', fontsize=14)
            
            # Set labels
            ax.set_xlabel(column, fontsize=12)
        else:
            # Check if 'by' column has too many unique values
            if data[by].nunique() > 10:
                warnings.warn(f"Column '{by}' has more than 10 unique values, which may make the boxplot crowded")
            
            sns.boxplot(x=by, y=column, data=data, palette='Set3', ax=ax)
            
            # Set title
            if title:
                ax.set_title(title, fontsize=14)
            else:
                ax.set_title(f'Boxplot of {column} by {by}', fontsize=14)
            
            # Set labels
            ax.set_xlabel(by, fontsize=12)
            ax.set_ylabel(column, fontsize=12)
            
            # Rotate x-axis labels if there are many categories
            if data[by].nunique() > 5:
                plt.xticks(rotation=45, ha='right')
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_scatter(self, data: pd.DataFrame, x: str, y: str, 
                    hue: Optional[str] = None, size: Optional[str] = None,
                    title: Optional[str] = None, figsize: Tuple[int, int] = (12, 8),
                    output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot scatter plot for two numeric columns.
        
        Args:
            data: DataFrame containing the data.
            x: Column for x-axis.
            y: Column for y-axis.
            hue: Column for color encoding.
            size: Column for size encoding.
            title: Title for the plot.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        if x not in data.columns:
            raise ValueError(f"Column '{x}' not found in the DataFrame")
        
        if y not in data.columns:
            raise ValueError(f"Column '{y}' not found in the DataFrame")
        
        if not pd.api.types.is_numeric_dtype(data[x]):
            raise ValueError(f"Column '{x}' is not numeric")
        
        if not pd.api.types.is_numeric_dtype(data[y]):
            raise ValueError(f"Column '{y}' is not numeric")
        
        if hue is not None and hue not in data.columns:
            raise ValueError(f"Column '{hue}' not found in the DataFrame")
        
        if size is not None and size not in data.columns:
            raise ValueError(f"Column '{size}' not found in the DataFrame")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot scatter plot
        sns.scatterplot(x=x, y=y, hue=hue, size=size, data=data, ax=ax)
        
        # Set title
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(f'Scatter Plot of {y} vs {x}', fontsize=14)
        
        # Set labels
        ax.set_xlabel(x, fontsize=12)
        ax.set_ylabel(y, fontsize=12)
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add correlation coefficient
        corr = data[[x, y]].corr().iloc[0, 1]
        ax.text(0.05, 0.95, f"Correlation: {corr:.2f}", transform=ax.transAxes,
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_correlation_matrix(self, data: pd.DataFrame, columns: Optional[List[str]] = None,
                               method: str = 'pearson', cmap: str = 'coolwarm',
                               figsize: Tuple[int, int] = (12, 10),
                               output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot correlation matrix for numeric columns.
        
        Args:
            data: DataFrame containing the data.
            columns: List of columns to include. If None, use all numeric columns.
            method: Correlation method ('pearson', 'spearman', or 'kendall').
            cmap: Colormap for the heatmap.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        # Get numeric columns
        numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_columns:
            raise ValueError("No numeric columns found in the DataFrame")
        
        # Filter columns if provided
        if columns:
            numeric_columns = [col for col in columns if col in numeric_columns]
            
            if not numeric_columns:
                raise ValueError("No valid numeric columns provided")
        
        # Calculate correlation matrix
        corr_matrix = data[numeric_columns].corr(method=method)
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create mask for upper triangle
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        # Plot heatmap
        sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                   annot=True, fmt=".2f", square=True, linewidths=.5,
                   cbar_kws={"shrink": .5}, ax=ax)
        
        # Set title
        ax.set_title(f'Correlation Matrix ({method.capitalize()})', fontsize=14)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_pairplot(self, data: pd.DataFrame, columns: Optional[List[str]] = None,
                     hue: Optional[str] = None, diag_kind: str = 'kde',
                     figsize: Tuple[int, int] = (12, 12),
                     output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot pairplot for numeric columns.
        
        Args:
            data: DataFrame containing the data.
            columns: List of columns to include. If None, use all numeric columns (limited to 5).
            hue: Column for color encoding.
            diag_kind: Kind of plot for diagonal ('hist' or 'kde').
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        # Get numeric columns
        numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_columns:
            raise ValueError("No numeric columns found in the DataFrame")
        
        # Filter columns if provided
        if columns:
            numeric_columns = [col for col in columns if col in numeric_columns]
            
            if not numeric_columns:
                raise ValueError("No valid numeric columns provided")
        
        # Limit to 5 columns for readability
        if len(numeric_columns) > 5:
            warnings.warn(f"Limiting pairplot to 5 columns out of {len(numeric_columns)}")
            numeric_columns = numeric_columns[:5]
        
        # Check hue column
        if hue is not None:
            if hue not in data.columns:
                raise ValueError(f"Column '{hue}' not found in the DataFrame")
            
            # Check if hue column has too many unique values
            if data[hue].nunique() > 10:
                warnings.warn(f"Column '{hue}' has more than 10 unique values, which may make the pairplot crowded")
        
        # Create pairplot
        g = sns.pairplot(data, vars=numeric_columns, hue=hue, diag_kind=diag_kind,
                        height=figsize[0]/len(numeric_columns))
        
        # Set title
        g.fig.suptitle('Pairplot of Numeric Variables', fontsize=16, y=1.02)
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return g.fig
    
    def plot_count(self, data: pd.DataFrame, column: str, 
                  hue: Optional[str] = None, title: Optional[str] = None,
                  figsize: Tuple[int, int] = (12, 8),
                  output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot count plot for a categorical column.
        
        Args:
            data: DataFrame containing the data.
            column: Column to plot.
            hue: Column for color encoding.
            title: Title for the plot.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        if column not in data.columns:
            raise ValueError(f"Column '{column}' not found in the DataFrame")
        
        if hue is not None and hue not in data.columns:
            raise ValueError(f"Column '{hue}' not found in the DataFrame")
        
        # Check if column has too many unique values
        if data[column].nunique() > 20:
            warnings.warn(f"Column '{column}' has more than 20 unique values, which may make the count plot crowded")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot count plot
        sns.countplot(x=column, hue=hue, data=data, ax=ax)
        
        # Set title
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(f'Count Plot of {column}', fontsize=14)
        
        # Set labels
        ax.set_xlabel(column, fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        
        # Rotate x-axis labels if there are many categories
        if data[column].nunique() > 5:
            plt.xticks(rotation=45, ha='right')
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add value counts
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', 
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_bar(self, data: pd.DataFrame, x: str, y: str,
                hue: Optional[str] = None, title: Optional[str] = None,
                figsize: Tuple[int, int] = (12, 8),
                output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot bar plot for categorical and numeric columns.
        
        Args:
            data: DataFrame containing the data.
            x: Column for x-axis (categorical).
            y: Column for y-axis (numeric).
            hue: Column for color encoding.
            title: Title for the plot.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        if x not in data.columns:
            raise ValueError(f"Column '{x}' not found in the DataFrame")
        
        if y not in data.columns:
            raise ValueError(f"Column '{y}' not found in the DataFrame")
        
        if not pd.api.types.is_numeric_dtype(data[y]):
            raise ValueError(f"Column '{y}' is not numeric")
        
        if hue is not None and hue not in data.columns:
            raise ValueError(f"Column '{hue}' not found in the DataFrame")
        
        # Check if x column has too many unique values
        if data[x].nunique() > 20:
            warnings.warn(f"Column '{x}' has more than 20 unique values, which may make the bar plot crowded")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot bar plot
        sns.barplot(x=x, y=y, hue=hue, data=data, ax=ax)
        
        # Set title
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(f'Bar Plot of {y} by {x}', fontsize=14)
        
        # Set labels
        ax.set_xlabel(x, fontsize=12)
        ax.set_ylabel(y, fontsize=12)
        
        # Rotate x-axis labels if there are many categories
        if data[x].nunique() > 5:
            plt.xticks(rotation=45, ha='right')
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_line(self, data: pd.DataFrame, x: str, y: str,
                 hue: Optional[str] = None, title: Optional[str] = None,
                 figsize: Tuple[int, int] = (12, 8),
                 output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot line plot for two columns.
        
        Args:
            data: DataFrame containing the data.
            x: Column for x-axis.
            y: Column for y-axis.
            hue: Column for color encoding.
            title: Title for the plot.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        if x not in data.columns:
            raise ValueError(f"Column '{x}' not found in the DataFrame")
        
        if y not in data.columns:
            raise ValueError(f"Column '{y}' not found in the DataFrame")
        
        if not pd.api.types.is_numeric_dtype(data[y]):
            raise ValueError(f"Column '{y}' is not numeric")
        
        if hue is not None and hue not in data.columns:
            raise ValueError(f"Column '{hue}' not found in the DataFrame")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot line plot
        sns.lineplot(x=x, y=y, hue=hue, data=data, ax=ax)
        
        # Set title
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(f'Line Plot of {y} vs {x}', fontsize=14)
        
        # Set labels
        ax.set_xlabel(x, fontsize=12)
        ax.set_ylabel(y, fontsize=12)
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_time_series(self, data: pd.DataFrame, date_column: str, value_column: str,
                        freq: Optional[str] = None, title: Optional[str] = None,
                        figsize: Tuple[int, int] = (15, 8),
                        output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot time series for date and value columns.
        
        Args:
            data: DataFrame containing the data.
            date_column: Column with dates.
            value_column: Column with values to plot.
            freq: Frequency for resampling (e.g., 'D', 'W', 'M').
            title: Title for the plot.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        if date_column not in data.columns:
            raise ValueError(f"Column '{date_column}' not found in the DataFrame")
        
        if value_column not in data.columns:
            raise ValueError(f"Column '{value_column}' not found in the DataFrame")
        
        if not pd.api.types.is_numeric_dtype(data[value_column]):
            raise ValueError(f"Column '{value_column}' is not numeric")
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_dtype(data[date_column]):
            try:
                data = data.copy()
                data[date_column] = pd.to_datetime(data[date_column])
            except:
                raise ValueError(f"Column '{date_column}' cannot be converted to datetime")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Resample if frequency is provided
        if freq:
            # Set date as index
            df_temp = data.set_index(date_column)
            
            # Resample and plot
            df_temp[value_column].resample(freq).mean().plot(ax=ax)
            
            # Add original data as scatter points
            ax.scatter(data[date_column], data[value_column], alpha=0.3, color='gray')
        else:
            # Plot time series
            ax.plot(data[date_column], data[value_column])
        
        # Set title
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(f'Time Series of {value_column}', fontsize=14)
        
        # Set labels
        ax.set_xlabel(date_column, fontsize=12)
        ax.set_ylabel(value_column, fontsize=12)
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Format x-axis
        fig.autofmt_xdate()
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_missing_values(self, data: pd.DataFrame, figsize: Tuple[int, int] = (12, 8),
                           output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot missing values heatmap.
        
        Args:
            data: DataFrame containing the data.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create missing values mask
        missing = data.isna()
        
        # Plot heatmap
        sns.heatmap(missing, cmap='viridis', cbar=False, ax=ax)
        
        # Set title
        ax.set_title('Missing Values Heatmap', fontsize=14)
        
        # Set labels
        ax.set_xlabel('Columns', fontsize=12)
        ax.set_ylabel('Rows', fontsize=12)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_missing_values_bar(self, data: pd.DataFrame, figsize: Tuple[int, int] = (12, 8),
                              output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot missing values bar chart.
        
        Args:
            data: DataFrame containing the data.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        # Calculate missing values
        missing = data.isna().sum().sort_values(ascending=False)
        missing_percent = (data.isna().sum() / len(data) * 100).sort_values(ascending=False)
        
        # Filter columns with missing values
        missing = missing[missing > 0]
        missing_percent = missing_percent[missing_percent > 0]
        
        if missing.empty:
            warnings.warn("No missing values found in the DataFrame")
            
            # Create empty figure
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(0.5, 0.5, "No missing values found", ha='center', va='center', fontsize=14)
            ax.set_title('Missing Values', fontsize=14)
            
            # Save if output path is provided
            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
            
            return fig
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot bar chart
        missing.plot(kind='bar', ax=ax, color='skyblue')
        
        # Set title
        ax.set_title('Missing Values by Column', fontsize=14)
        
        # Set labels
        ax.set_xlabel('Column', fontsize=12)
        ax.set_ylabel('Missing Count', fontsize=12)
        
        # Add percentages
        for i, v in enumerate(missing):
            ax.text(i, v + 0.5, f"{missing_percent.iloc[i]:.1f}%", ha='center', fontsize=10)
        
        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_distribution_grid(self, data: pd.DataFrame, columns: Optional[List[str]] = None,
                              figsize: Tuple[int, int] = (15, 12),
                              output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot distribution grid for numeric columns.
        
        Args:
            data: DataFrame containing the data.
            columns: List of columns to include. If None, use all numeric columns.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        # Get numeric columns
        numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_columns:
            raise ValueError("No numeric columns found in the DataFrame")
        
        # Filter columns if provided
        if columns:
            numeric_columns = [col for col in columns if col in numeric_columns]
            
            if not numeric_columns:
                raise ValueError("No valid numeric columns provided")
        
        # Limit to 16 columns for readability
        if len(numeric_columns) > 16:
            warnings.warn(f"Limiting distribution grid to 16 columns out of {len(numeric_columns)}")
            numeric_columns = numeric_columns[:16]
        
        # Calculate grid dimensions
        n_cols = min(4, len(numeric_columns))
        n_rows = (len(numeric_columns) + n_cols - 1) // n_cols
        
        # Create figure
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        
        # Flatten axes for easy iteration
        if n_rows == 1 and n_cols == 1:
            axes = np.array([axes])
        axes = axes.flatten()
        
        # Plot distributions
        for i, col in enumerate(numeric_columns):
            if i < len(axes):
                # Calculate statistics
                mean = data[col].mean()
                median = data[col].median()
                skewness = data[col].skew()
                
                # Plot histogram with KDE
                sns.histplot(data[col].dropna(), kde=True, ax=axes[i], color='skyblue')
                
                # Add vertical lines for mean and median
                axes[i].axvline(mean, color='red', linestyle='--', label=f'Mean: {mean:.2f}')
                axes[i].axvline(median, color='green', linestyle='-.', label=f'Median: {median:.2f}')
                
                # Add title with skewness
                axes[i].set_title(f"{col}\n(Skewness: {skewness:.2f})")
                
                # Add legend
                axes[i].legend(fontsize=8)
                
                # Add grid
                axes[i].grid(linestyle='--', alpha=0.7)
        
        # Hide unused subplots
        for i in range(len(numeric_columns), len(axes)):
            axes[i].set_visible(False)
        
        # Add overall title
        fig.suptitle('Distribution of Numeric Variables', fontsize=16, y=1.02)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_categorical_grid(self, data: pd.DataFrame, columns: Optional[List[str]] = None,
                             max_categories: int = 10, figsize: Tuple[int, int] = (15, 12),
                             output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot categorical grid for categorical columns.
        
        Args:
            data: DataFrame containing the data.
            columns: List of columns to include. If None, use all categorical columns.
            max_categories: Maximum number of categories to show per column.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        # Get categorical columns
        categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if not categorical_columns:
            raise ValueError("No categorical columns found in the DataFrame")
        
        # Filter columns if provided
        if columns:
            categorical_columns = [col for col in columns if col in categorical_columns]
            
            if not categorical_columns:
                raise ValueError("No valid categorical columns provided")
        
        # Limit to 9 columns for readability
        if len(categorical_columns) > 9:
            warnings.warn(f"Limiting categorical grid to 9 columns out of {len(categorical_columns)}")
            categorical_columns = categorical_columns[:9]
        
        # Calculate grid dimensions
        n_cols = min(3, len(categorical_columns))
        n_rows = (len(categorical_columns) + n_cols - 1) // n_cols
        
        # Create figure
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        
        # Flatten axes for easy iteration
        if n_rows == 1 and n_cols == 1:
            axes = np.array([axes])
        axes = axes.flatten()
        
        # Plot distributions
        for i, col in enumerate(categorical_columns):
            if i < len(axes):
                # Get value counts
                value_counts = data[col].value_counts()
                
                # Limit categories
                if len(value_counts) > max_categories:
                    other_count = value_counts.iloc[max_categories:].sum()
                    value_counts = value_counts.iloc[:max_categories]
                    value_counts['Other'] = other_count
                
                # Plot bar chart
                value_counts.plot(kind='bar', ax=axes[i], color='skyblue')
                
                # Add title with unique count
                axes[i].set_title(f"{col}\n({data[col].nunique()} unique values)")
                
                # Rotate x-axis labels
                axes[i].set_xticklabels(axes[i].get_xticklabels(), rotation=45, ha='right')
                
                # Add grid
                axes[i].grid(axis='y', linestyle='--', alpha=0.7)
                
                # Add value counts
                for j, v in enumerate(value_counts):
                    axes[i].text(j, v + 0.1, str(v), ha='center', fontsize=8)
        
        # Hide unused subplots
        for i in range(len(categorical_columns), len(axes)):
            axes[i].set_visible(False)
        
        # Add overall title
        fig.suptitle('Distribution of Categorical Variables', fontsize=16, y=1.02)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_correlation_heatmap(self, data: pd.DataFrame, columns: Optional[List[str]] = None,
                               method: str = 'pearson', cmap: str = 'coolwarm',
                               figsize: Tuple[int, int] = (12, 10),
                               output_path: Optional[str] = None) -> plt.Figure:
        """
        Plot correlation heatmap for numeric columns.
        
        Args:
            data: DataFrame containing the data.
            columns: List of columns to include. If None, use all numeric columns.
            method: Correlation method ('pearson', 'spearman', or 'kendall').
            cmap: Colormap for the heatmap.
            figsize: Figure size.
            output_path: Path to save the plot.
            
        Returns:
            Matplotlib figure.
        """
        # Get numeric columns
        numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_columns:
            raise ValueError("No numeric columns found in the DataFrame")
        
        # Filter columns if provided
        if columns:
            numeric_columns = [col for col in columns if col in numeric_columns]
            
            if not numeric_columns:
                raise ValueError("No valid numeric columns provided")
        
        # Calculate correlation matrix
        corr_matrix = data[numeric_columns].corr(method=method)
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot heatmap
        sns.heatmap(corr_matrix, cmap=cmap, vmax=1, vmin=-1, center=0,
                   annot=True, fmt=".2f", square=True, linewidths=.5,
                   cbar_kws={"shrink": .5}, ax=ax)
        
        # Set title
        ax.set_title(f'Correlation Heatmap ({method.capitalize()})', fontsize=14)
        
        plt.tight_layout()
        
        # Save if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_dashboard(self, data: pd.DataFrame, output_dir: str,
                        include_missing: bool = True,
                        include_distributions: bool = True,
                        include_correlations: bool = True,
                        include_categorical: bool = True) -> str:
        """
        Create a dashboard with multiple visualizations.
        
        Args:
            data: DataFrame containing the data.
            output_dir: Directory to save the dashboard.
            include_missing: Whether to include missing values visualizations.
            include_distributions: Whether to include distribution visualizations.
            include_correlations: Whether to include correlation visualizations.
            include_categorical: Whether to include categorical visualizations.
            
        Returns:
            Path to the dashboard HTML file.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create plots directory
        plots_dir = os.path.join(output_dir, 'plots')
        os.makedirs(plots_dir, exist_ok=True)
        
        # Generate plots
        plots = []
        
        # Missing values plots
        if include_missing and data.isna().sum().sum() > 0:
            # Missing values bar chart
            missing_bar_path = os.path.join(plots_dir, 'missing_bar.png')
            self.plot_missing_values_bar(data, output_path=missing_bar_path)
            plots.append(('Missing Values by Column', 'plots/missing_bar.png'))
            
            # Missing values heatmap
            missing_heatmap_path = os.path.join(plots_dir, 'missing_heatmap.png')
            self.plot_missing_values(data, output_path=missing_heatmap_path)
            plots.append(('Missing Values Heatmap', 'plots/missing_heatmap.png'))
        
        # Distribution plots
        if include_distributions:
            # Numeric distributions
            numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
            if numeric_columns:
                dist_grid_path = os.path.join(plots_dir, 'distribution_grid.png')
                self.plot_distribution_grid(data, output_path=dist_grid_path)
                plots.append(('Distribution of Numeric Variables', 'plots/distribution_grid.png'))
        
        # Correlation plots
        if include_correlations:
            # Correlation heatmap
            numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
            if len(numeric_columns) > 1:
                corr_heatmap_path = os.path.join(plots_dir, 'correlation_heatmap.png')
                self.plot_correlation_heatmap(data, output_path=corr_heatmap_path)
                plots.append(('Correlation Heatmap', 'plots/correlation_heatmap.png'))
                
                # Pairplot (limited to 5 columns)
                if len(numeric_columns) > 1:
                    pairplot_path = os.path.join(plots_dir, 'pairplot.png')
                    self.plot_pairplot(data, output_path=pairplot_path)
                    plots.append(('Pairplot of Numeric Variables', 'plots/pairplot.png'))
        
        # Categorical plots
        if include_categorical:
            # Categorical distributions
            categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
            if categorical_columns:
                cat_grid_path = os.path.join(plots_dir, 'categorical_grid.png')
                self.plot_categorical_grid(data, output_path=cat_grid_path)
                plots.append(('Distribution of Categorical Variables', 'plots/categorical_grid.png'))
        
        # Create HTML dashboard
        dashboard_path = os.path.join(output_dir, 'dashboard.html')
        
        # Generate HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SBYB Data Visualization Dashboard</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    color: #333;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                .plot-container {{
                    margin-bottom: 30px;
                    padding: 20px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .plot-image {{
                    max-width: 100%;
                    height: auto;
                }}
                .footer {{
                    margin-top: 50px;
                    text-align: center;
                    font-size: 12px;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>SBYB Data Visualization Dashboard</h1>
                <p>Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                
                <div class="plot-container">
                    <h2>Dataset Overview</h2>
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Number of Rows</td>
                            <td>{len(data)}</td>
                        </tr>
                        <tr>
                            <td>Number of Columns</td>
                            <td>{len(data.columns)}</td>
                        </tr>
                        <tr>
                            <td>Numeric Columns</td>
                            <td>{len(data.select_dtypes(include=['number']).columns)}</td>
                        </tr>
                        <tr>
                            <td>Categorical Columns</td>
                            <td>{len(data.select_dtypes(include=['object', 'category']).columns)}</td>
                        </tr>
                        <tr>
                            <td>Missing Values</td>
                            <td>{data.isna().sum().sum()}</td>
                        </tr>
                    </table>
                </div>
        """
        
        # Add plots
        for title, path in plots:
            html_content += f"""
                <div class="plot-container">
                    <h2>{title}</h2>
                    <img src="{path}" class="plot-image" alt="{title}">
                </div>
            """
        
        # Close HTML
        html_content += """
                <div class="footer">
                    <p>Generated by SBYB Visualizer</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Write HTML to file
        with open(dashboard_path, "w") as f:
            f.write(html_content)
        
        return dashboard_path
    
    def create_interactive_dashboard(self, data: pd.DataFrame, output_path: str) -> str:
        """
        Create an interactive dashboard using Plotly.
        
        Args:
            data: DataFrame containing the data.
            output_path: Path to save the dashboard.
            
        Returns:
            Path to the dashboard HTML file.
        """
        try:
            import plotly.express as px
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
        except ImportError:
            raise ImportError("Plotly is required for interactive dashboards. Install it with 'pip install plotly'.")
        
        # Create figures
        figures = []
        
        # Dataset overview
        dataset_info = {
            "Metric": ["Number of Rows", "Number of Columns", "Numeric Columns", "Categorical Columns", "Missing Values"],
            "Value": [
                len(data),
                len(data.columns),
                len(data.select_dtypes(include=['number']).columns),
                len(data.select_dtypes(include=['object', 'category']).columns),
                data.isna().sum().sum()
            ]
        }
        
        dataset_table = go.Figure(data=[go.Table(
            header=dict(values=list(dataset_info.keys()),
                       fill_color='paleturquoise',
                       align='left'),
            cells=dict(values=[dataset_info["Metric"], dataset_info["Value"]],
                      fill_color='lavender',
                      align='left'))
        ])
        
        dataset_table.update_layout(title="Dataset Overview")
        figures.append(dataset_table)
        
        # Missing values bar chart
        missing = data.isna().sum().sort_values(ascending=False)
        missing_percent = (data.isna().sum() / len(data) * 100).sort_values(ascending=False)
        
        # Filter columns with missing values
        missing = missing[missing > 0]
        missing_percent = missing_percent[missing_percent > 0]
        
        if not missing.empty:
            missing_fig = go.Figure()
            
            missing_fig.add_trace(go.Bar(
                x=missing.index,
                y=missing.values,
                name="Missing Count",
                marker_color='skyblue'
            ))
            
            missing_fig.add_trace(go.Scatter(
                x=missing.index,
                y=missing_percent.values,
                name="Missing Percent",
                yaxis="y2",
                marker_color='red'
            ))
            
            missing_fig.update_layout(
                title="Missing Values by Column",
                xaxis=dict(title="Column"),
                yaxis=dict(title="Missing Count"),
                yaxis2=dict(title="Missing Percent", overlaying="y", side="right"),
                legend=dict(x=0.7, y=1)
            )
            
            figures.append(missing_fig)
        
        # Numeric distributions
        numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_columns:
            # Limit to 9 columns for readability
            if len(numeric_columns) > 9:
                numeric_columns = numeric_columns[:9]
            
            # Create subplots
            n_cols = min(3, len(numeric_columns))
            n_rows = (len(numeric_columns) + n_cols - 1) // n_cols
            
            dist_fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=numeric_columns)
            
            for i, col in enumerate(numeric_columns):
                row = i // n_cols + 1
                col_idx = i % n_cols + 1
                
                # Create histogram
                hist = go.Histogram(x=data[col].dropna(), name=col, marker_color='skyblue')
                
                dist_fig.add_trace(hist, row=row, col=col_idx)
            
            dist_fig.update_layout(
                title="Distribution of Numeric Variables",
                showlegend=False,
                height=300 * n_rows
            )
            
            figures.append(dist_fig)
        
        # Correlation heatmap
        if len(numeric_columns) > 1:
            corr_matrix = data[numeric_columns].corr()
            
            corr_fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu_r',
                zmin=-1,
                zmax=1,
                text=corr_matrix.round(2).values,
                texttemplate="%{text}",
                colorbar=dict(title="Correlation")
            ))
            
            corr_fig.update_layout(
                title="Correlation Heatmap",
                xaxis=dict(title="Column"),
                yaxis=dict(title="Column")
            )
            
            figures.append(corr_fig)
        
        # Categorical distributions
        categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if categorical_columns:
            # Limit to 9 columns for readability
            if len(categorical_columns) > 9:
                categorical_columns = categorical_columns[:9]
            
            # Create subplots
            n_cols = min(3, len(categorical_columns))
            n_rows = (len(categorical_columns) + n_cols - 1) // n_cols
            
            cat_fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=categorical_columns)
            
            for i, col in enumerate(categorical_columns):
                row = i // n_cols + 1
                col_idx = i % n_cols + 1
                
                # Get value counts
                value_counts = data[col].value_counts()
                
                # Limit categories
                if len(value_counts) > 10:
                    other_count = value_counts.iloc[10:].sum()
                    value_counts = value_counts.iloc[:10]
                    value_counts['Other'] = other_count
                
                # Create bar chart
                bar = go.Bar(x=value_counts.index, y=value_counts.values, name=col, marker_color='skyblue')
                
                cat_fig.add_trace(bar, row=row, col=col_idx)
            
            cat_fig.update_layout(
                title="Distribution of Categorical Variables",
                showlegend=False,
                height=300 * n_rows
            )
            
            figures.append(cat_fig)
        
        # Create dashboard
        dashboard = go.Figure()
        
        # Add dropdown menu
        dropdown_buttons = []
        
        for i, fig in enumerate(figures):
            dropdown_buttons.append(
                dict(
                    method="update",
                    args=[{"visible": [j == i for j in range(len(figures))]}],
                    label=fig.layout.title.text
                )
            )
        
        # Make first figure visible
        for i, fig in enumerate(figures):
            for trace in fig.data:
                if i == 0:
                    trace.visible = True
                else:
                    trace.visible = False
                dashboard.add_trace(trace)
        
        # Update layout
        dashboard.update_layout(
            title="SBYB Interactive Dashboard",
            updatemenus=[
                dict(
                    active=0,
                    buttons=dropdown_buttons,
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.15,
                    yanchor="top"
                )
            ]
        )
        
        # Update layout for each figure
        for i, fig in enumerate(figures):
            if i == 0:
                dashboard.update_layout(
                    title=fig.layout.title.text,
                    xaxis=fig.layout.xaxis,
                    yaxis=fig.layout.yaxis
                )
        
        # Write to HTML file
        dashboard.write_html(output_path)
        
        return output_path
