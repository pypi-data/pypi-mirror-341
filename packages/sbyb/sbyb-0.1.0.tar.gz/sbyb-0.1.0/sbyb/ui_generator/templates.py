"""
Template manager for SBYB UI Generator.

This module provides a template manager for UI Generator
to manage and apply templates for different UI frameworks.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import shutil
import tempfile
import jinja2

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import UIGenerationError


class TemplateManager(SBYBComponent):
    """
    Template manager for UI Generator.
    
    This component provides a template manager for UI Generator
    to manage and apply templates for different UI frameworks.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the template manager.
        
        Args:
            config: Configuration dictionary for the template manager.
        """
        super().__init__(config)
        self.templates = {}
        self.template_dirs = {}
        self._setup_template_dirs()
        self._load_default_templates()
    
    def _setup_template_dirs(self) -> None:
        """
        Set up template directories.
        """
        # Default template directory
        default_template_dir = os.path.join(os.path.dirname(__file__), "templates")
        
        # Create template directory if it doesn't exist
        if not os.path.exists(default_template_dir):
            os.makedirs(default_template_dir)
        
        # Set up template directories for each framework
        for framework in ["streamlit", "dash", "flask", "html", "react", "vue"]:
            framework_dir = os.path.join(default_template_dir, framework)
            if not os.path.exists(framework_dir):
                os.makedirs(framework_dir)
            self.template_dirs[framework] = framework_dir
    
    def _load_default_templates(self) -> None:
        """
        Load default templates.
        """
        # Streamlit templates
        self.register_template(
            "streamlit_basic",
            "Basic Streamlit App",
            "streamlit",
            {
                "description": "A basic Streamlit application template.",
                "files": {
                    "app.py": """
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(
    page_title="{{ app_title }}",
    page_icon="{{ app_icon }}",
    layout="{{ layout }}",
    initial_sidebar_state="{{ sidebar_state }}"
)

# Title and description
st.title("{{ app_title }}")
st.write("{{ app_description }}")

# Main content
{{ content }}
"""
                }
            }
        )
        
        self.register_template(
            "streamlit_ml_dashboard",
            "ML Dashboard (Streamlit)",
            "streamlit",
            {
                "description": "A Streamlit dashboard for machine learning models.",
                "files": {
                    "app.py": """
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc, precision_recall_curve

# Set page config
st.set_page_config(
    page_title="{{ app_title }}",
    page_icon="{{ app_icon }}",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("{{ app_title }}")
st.write("{{ app_description }}")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to", ["Overview", "Model Performance", "Predictions", "About"])

# Load data and model
@st.cache_data
def load_data():
    return pd.read_csv("{{ data_path }}")

@st.cache_resource
def load_model():
    with open("{{ model_path }}", "rb") as f:
        return pickle.load(f)

try:
    data = load_data()
    model = load_model()
except Exception as e:
    st.error(f"Error loading data or model: {str(e)}")
    st.stop()

# Pages
if page == "Overview":
    st.header("Dataset Overview")
    
    # Display dataset info
    st.subheader("Dataset Information")
    st.write(f"Number of rows: {data.shape[0]}")
    st.write(f"Number of columns: {data.shape[1]}")
    
    # Display first few rows
    st.subheader("Sample Data")
    st.dataframe(data.head())
    
    # Display summary statistics
    st.subheader("Summary Statistics")
    st.dataframe(data.describe())
    
    # Display visualizations
    st.subheader("Visualizations")
    
    # Select columns for visualization
    col1, col2 = st.columns(2)
    with col1:
        numeric_cols = data.select_dtypes(include=["number"]).columns.tolist()
        x_col = st.selectbox("Select X-axis", numeric_cols)
    with col2:
        y_col = st.selectbox("Select Y-axis", numeric_cols)
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=data, x=x_col, y=y_col, ax=ax)
    ax.set_title(f"{y_col} vs {x_col}")
    st.pyplot(fig)

elif page == "Model Performance":
    st.header("Model Performance")
    
    # Get target column
    target_col = "{{ target_column }}"
    
    # Get feature columns
    feature_cols = [col for col in data.columns if col != target_col]
    
    # Split data
    X = data[feature_cols]
    y = data[target_col]
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Classification metrics
    if hasattr(model, "predict_proba"):
        st.subheader("Classification Metrics")
        
        # Confusion Matrix
        st.write("Confusion Matrix")
        cm = confusion_matrix(y, y_pred)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("True")
        st.pyplot(fig)
        
        # Classification Report
        st.write("Classification Report")
        report = classification_report(y, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        st.dataframe(report_df)
        
        # ROC Curve
        st.write("ROC Curve")
        y_proba = model.predict_proba(X)
        
        # For binary classification
        if y_proba.shape[1] == 2:
            fpr, tpr, _ = roc_curve(y, y_proba[:, 1])
            roc_auc = auc(fpr, tpr)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(fpr, tpr, label=f"ROC curve (area = {roc_auc:.2f})")
            ax.plot([0, 1], [0, 1], "k--")
            ax.set_xlim([0.0, 1.0])
            ax.set_ylim([0.0, 1.05])
            ax.set_xlabel("False Positive Rate")
            ax.set_ylabel("True Positive Rate")
            ax.set_title("Receiver Operating Characteristic")
            ax.legend(loc="lower right")
            st.pyplot(fig)
    
    # Regression metrics
    else:
        st.subheader("Regression Metrics")
        
        # Residuals
        residuals = y - y_pred
        
        # Residual plot
        st.write("Residual Plot")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(y_pred, residuals)
        ax.axhline(y=0, color="r", linestyle="-")
        ax.set_xlabel("Predicted Values")
        ax.set_ylabel("Residuals")
        ax.set_title("Residuals vs Predicted Values")
        st.pyplot(fig)
        
        # Residual histogram
        st.write("Residual Histogram")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(residuals, bins=20, edgecolor="black")
        ax.axvline(x=0, color="r", linestyle="-")
        ax.set_xlabel("Residuals")
        ax.set_ylabel("Frequency")
        ax.set_title("Histogram of Residuals")
        st.pyplot(fig)
        
        # Actual vs Predicted
        st.write("Actual vs Predicted")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(y, y_pred)
        ax.plot([y.min(), y.max()], [y.min(), y.max()], "k--")
        ax.set_xlabel("Actual Values")
        ax.set_ylabel("Predicted Values")
        ax.set_title("Actual vs Predicted Values")
        st.pyplot(fig)

elif page == "Predictions":
    st.header("Make Predictions")
    
    # Get feature columns
    feature_cols = [col for col in data.columns if col != "{{ target_column }}"]
    
    # Create input form
    st.subheader("Input Features")
    
    # Create columns for input fields
    cols = st.columns(2)
    input_data = {}
    
    for i, col in enumerate(feature_cols):
        with cols[i % 2]:
            # Determine input type based on data type
            if data[col].dtype == "float64":
                input_data[col] = st.number_input(f"{col}", value=float(data[col].mean()))
            elif data[col].dtype == "int64":
                input_data[col] = st.number_input(f"{col}", value=int(data[col].mean()), step=1)
            elif data[col].nunique() < 10:  # Categorical with few values
                input_data[col] = st.selectbox(f"{col}", options=data[col].unique())
            else:
                input_data[col] = st.text_input(f"{col}", value=str(data[col].iloc[0]))
    
    # Make prediction
    if st.button("Predict"):
        try:
            # Create input DataFrame
            input_df = pd.DataFrame([input_data])
            
            # Make prediction
            prediction = model.predict(input_df)
            
            # Display prediction
            st.success(f"Prediction: {prediction[0]}")
            
            # Display probability if available
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(input_df)
                st.write("Prediction Probabilities:")
                
                # Get class names if available
                if hasattr(model, "classes_"):
                    class_names = model.classes_
                    proba_df = pd.DataFrame([proba[0]], columns=class_names)
                else:
                    proba_df = pd.DataFrame([proba[0]], columns=[f"Class {i}" for i in range(proba.shape[1])])
                
                st.dataframe(proba_df)
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")

else:  # About page
    st.header("About")
    
    st.subheader("Application Information")
    st.write("{{ app_description }}")
    
    st.subheader("Model Information")
    st.write(f"Model Type: {type(model).__name__}")
    
    # Display model parameters if available
    if hasattr(model, "get_params"):
        st.write("Model Parameters:")
        params = model.get_params()
        params_df = pd.DataFrame({"Parameter": list(params.keys()), "Value": list(params.values())})
        st.dataframe(params_df)
    
    st.subheader("Dataset Information")
    st.write(f"Dataset Shape: {data.shape}")
    st.write(f"Features: {', '.join([col for col in data.columns if col != '{{ target_column }}'])}")
    st.write(f"Target: {{ target_column }}")
"""
                }
            }
        )
        
        # Dash templates
        self.register_template(
            "dash_basic",
            "Basic Dash App",
            "dash",
            {
                "description": "A basic Dash application template.",
                "files": {
                    "app.py": """
import dash
from dash import dcc, html, callback, Input, Output
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__, title="{{ app_title }}")

# Define the layout
app.layout = html.Div([
    html.H1("{{ app_title }}"),
    html.P("{{ app_description }}"),
    
    # Main content
    {{ content }}
])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
"""
                }
            }
        )
        
        self.register_template(
            "dash_ml_dashboard",
            "ML Dashboard (Dash)",
            "dash",
            {
                "description": "A Dash dashboard for machine learning models.",
                "files": {
                    "app.py": """
import dash
from dash import dcc, html, callback, Input, Output, State, dash_table
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle
import os
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc, precision_recall_curve

# Initialize the Dash app
app = dash.Dash(__name__, title="{{ app_title }}")

# Load data and model
def load_data():
    return pd.read_csv("{{ data_path }}")

def load_model():
    with open("{{ model_path }}", "rb") as f:
        return pickle.load(f)

try:
    data = load_data()
    model = load_model()
except Exception as e:
    print(f"Error loading data or model: {str(e)}")

# Get target column
target_col = "{{ target_column }}"

# Get feature columns
feature_cols = [col for col in data.columns if col != target_col]

# Define the layout
app.layout = html.Div([
    # Header
    html.H1("{{ app_title }}"),
    html.P("{{ app_description }}"),
    
    # Tabs
    dcc.Tabs([
        # Overview Tab
        dcc.Tab(label="Overview", children=[
            html.Div([
                html.H2("Dataset Overview"),
                
                # Dataset info
                html.H3("Dataset Information"),
                html.P(f"Number of rows: {data.shape[0]}"),
                html.P(f"Number of columns: {data.shape[1]}"),
                
                # Sample data
                html.H3("Sample Data"),
                dash_table.DataTable(
                    data=data.head().to_dict("records"),
                    columns=[{"name": i, "id": i} for i in data.columns],
                    page_size=5,
                    style_table={"overflowX": "auto"}
                ),
                
                # Summary statistics
                html.H3("Summary Statistics"),
                dash_table.DataTable(
                    data=data.describe().reset_index().to_dict("records"),
                    columns=[{"name": i, "id": i} for i in data.describe().reset_index().columns],
                    page_size=10,
                    style_table={"overflowX": "auto"}
                ),
                
                # Visualizations
                html.H3("Visualizations"),
                
                # Controls for visualization
                html.Div([
                    html.Div([
                        html.Label("Select X-axis"),
                        dcc.Dropdown(
                            id="x-column",
                            options=[{"label": col, "value": col} for col in data.select_dtypes(include=["number"]).columns],
                            value=data.select_dtypes(include=["number"]).columns[0]
                        )
                    ], style={"width": "48%", "display": "inline-block"}),
                    
                    html.Div([
                        html.Label("Select Y-axis"),
                        dcc.Dropdown(
                            id="y-column",
                            options=[{"label": col, "value": col} for col in data.select_dtypes(include=["number"]).columns],
                            value=data.select_dtypes(include=["number"]).columns[1] if len(data.select_dtypes(include=["number"]).columns) > 1 else data.select_dtypes(include=["number"]).columns[0]
                        )
                    ], style={"width": "48%", "float": "right", "display": "inline-block"})
                ]),
                
                # Scatter plot
                dcc.Graph(id="scatter-plot")
            ])
        ]),
        
        # Model Performance Tab
        dcc.Tab(label="Model Performance", children=[
            html.Div([
                html.H2("Model Performance"),
                
                # Classification metrics
                html.Div(id="classification-metrics", children=[
                    html.H3("Classification Metrics"),
                    
                    # Confusion Matrix
                    html.H4("Confusion Matrix"),
                    dcc.Graph(id="confusion-matrix"),
                    
                    # Classification Report
                    html.H4("Classification Report"),
                    html.Div(id="classification-report"),
                    
                    # ROC Curve
                    html.H4("ROC Curve"),
                    dcc.Graph(id="roc-curve")
                ]) if hasattr(model, "predict_proba") else [],
                
                # Regression metrics
                html.Div(id="regression-metrics", children=[
                    html.H3("Regression Metrics"),
                    
                    # Residual Plot
                    html.H4("Residual Plot"),
                    dcc.Graph(id="residual-plot"),
                    
                    # Residual Histogram
                    html.H4("Residual Histogram"),
                    dcc.Graph(id="residual-histogram"),
                    
                    # Actual vs Predicted
                    html.H4("Actual vs Predicted"),
                    dcc.Graph(id="actual-vs-predicted")
                ]) if not hasattr(model, "predict_proba") else []
            ])
        ]),
        
        # Predictions Tab
        dcc.Tab(label="Predictions", children=[
            html.Div([
                html.H2("Make Predictions"),
                
                # Input form
                html.H3("Input Features"),
                
                # Create input fields
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label(col),
                            dcc.Input(
                                id=f"input-{col}",
                                type="number",
                                value=float(data[col].mean()) if data[col].dtype in ["float64", "int64"] else 0,
                                step=1 if data[col].dtype == "int64" else 0.1
                            )
                        ]) for col in feature_cols[i::2]
                    ], style={"width": "48%", "display": "inline-block"}) for i in range(2)
                ]),
                
                # Predict button
                html.Button("Predict", id="predict-button", n_clicks=0),
                
                # Prediction output
                html.Div(id="prediction-output")
            ])
        ]),
        
        # About Tab
        dcc.Tab(label="About", children=[
            html.Div([
                html.H2("About"),
                
                # Application Information
                html.H3("Application Information"),
                html.P("{{ app_description }}"),
                
                # Model Information
                html.H3("Model Information"),
                html.P(f"Model Type: {type(model).__name__}"),
                
                # Model Parameters
                html.H4("Model Parameters"),
                html.Div(id="model-parameters"),
                
                # Dataset Information
                html.H3("Dataset Information"),
                html.P(f"Dataset Shape: {data.shape}"),
                html.P(f"Features: {', '.join([col for col in data.columns if col != target_col])}"),
                html.P(f"Target: {target_col}")
            ])
        ])
    ])
])

# Callbacks
@callback(
    Output("scatter-plot", "figure"),
    [Input("x-column", "value"), Input("y-column", "value")]
)
def update_scatter_plot(x_col, y_col):
    fig = px.scatter(data, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    return fig

# Classification metrics callbacks
if hasattr(model, "predict_proba"):
    # Confusion Matrix
    @callback(
        Output("confusion-matrix", "figure"),
        [Input("classification-metrics", "children")]
    )
    def update_confusion_matrix(_):
        # Make predictions
        y_pred = model.predict(data[feature_cols])
        
        # Compute confusion matrix
        cm = confusion_matrix(data[target_col], y_pred)
        
        # Create heatmap
        fig = px.imshow(
            cm,
            labels=dict(x="Predicted", y="True", color="Count"),
            x=model.classes_ if hasattr(model, "classes_") else [f"Class {i}" for i in range(cm.shape[1])],
            y=model.classes_ if hasattr(model, "classes_") else [f"Class {i}" for i in range(cm.shape[0])],
            text_auto=True,
            color_continuous_scale="Blues"
        )
        
        return fig
    
    # Classification Report
    @callback(
        Output("classification-report", "children"),
        [Input("classification-metrics", "children")]
    )
    def update_classification_report(_):
        # Make predictions
        y_pred = model.predict(data[feature_cols])
        
        # Compute classification report
        report = classification_report(data[target_col], y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        
        # Create table
        return dash_table.DataTable(
            data=report_df.reset_index().to_dict("records"),
            columns=[{"name": i, "id": i} for i in report_df.reset_index().columns],
            page_size=10,
            style_table={"overflowX": "auto"}
        )
    
    # ROC Curve
    @callback(
        Output("roc-curve", "figure"),
        [Input("classification-metrics", "children")]
    )
    def update_roc_curve(_):
        # Make predictions
        y_proba = model.predict_proba(data[feature_cols])
        
        # For binary classification
        if y_proba.shape[1] == 2:
            fpr, tpr, _ = roc_curve(data[target_col], y_proba[:, 1])
            roc_auc = auc(fpr, tpr)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name=f"ROC curve (area = {roc_auc:.2f})"))
            fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random", line=dict(dash="dash")))
            
            fig.update_layout(
                title="Receiver Operating Characteristic",
                xaxis_title="False Positive Rate",
                yaxis_title="True Positive Rate",
                legend=dict(x=0.7, y=0.1),
                xaxis=dict(range=[0, 1]),
                yaxis=dict(range=[0, 1.05])
            )
            
            return fig
        else:
            # For multiclass, return empty figure
            return go.Figure()

# Regression metrics callbacks
else:
    # Residual Plot
    @callback(
        Output("residual-plot", "figure"),
        [Input("regression-metrics", "children")]
    )
    def update_residual_plot(_):
        # Make predictions
        y_pred = model.predict(data[feature_cols])
        
        # Compute residuals
        residuals = data[target_col] - y_pred
        
        # Create scatter plot
        fig = px.scatter(
            x=y_pred,
            y=residuals,
            labels={"x": "Predicted Values", "y": "Residuals"},
            title="Residuals vs Predicted Values"
        )
        
        # Add horizontal line at y=0
        fig.add_shape(
            type="line",
            x0=min(y_pred),
            y0=0,
            x1=max(y_pred),
            y1=0,
            line=dict(color="red", width=2, dash="dash")
        )
        
        return fig
    
    # Residual Histogram
    @callback(
        Output("residual-histogram", "figure"),
        [Input("regression-metrics", "children")]
    )
    def update_residual_histogram(_):
        # Make predictions
        y_pred = model.predict(data[feature_cols])
        
        # Compute residuals
        residuals = data[target_col] - y_pred
        
        # Create histogram
        fig = px.histogram(
            residuals,
            labels={"value": "Residuals", "count": "Frequency"},
            title="Histogram of Residuals"
        )
        
        # Add vertical line at x=0
        fig.add_shape(
            type="line",
            x0=0,
            y0=0,
            x1=0,
            y1=max(fig.data[0].y),
            line=dict(color="red", width=2, dash="dash")
        )
        
        return fig
    
    # Actual vs Predicted
    @callback(
        Output("actual-vs-predicted", "figure"),
        [Input("regression-metrics", "children")]
    )
    def update_actual_vs_predicted(_):
        # Make predictions
        y_pred = model.predict(data[feature_cols])
        
        # Create scatter plot
        fig = px.scatter(
            x=data[target_col],
            y=y_pred,
            labels={"x": "Actual Values", "y": "Predicted Values"},
            title="Actual vs Predicted Values"
        )
        
        # Add diagonal line
        min_val = min(min(data[target_col]), min(y_pred))
        max_val = max(max(data[target_col]), max(y_pred))
        
        fig.add_shape(
            type="line",
            x0=min_val,
            y0=min_val,
            x1=max_val,
            y1=max_val,
            line=dict(color="red", width=2, dash="dash")
        )
        
        return fig

# Prediction callback
@callback(
    Output("prediction-output", "children"),
    [Input("predict-button", "n_clicks")],
    [State(f"input-{col}", "value") for col in feature_cols]
)
def make_prediction(n_clicks, *feature_values):
    if n_clicks == 0:
        return html.Div()
    
    try:
        # Create input dictionary
        input_data = {col: val for col, val in zip(feature_cols, feature_values)}
        
        # Create input DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(input_df)
        
        # Create output
        output = [html.Div(html.H3(f"Prediction: {prediction[0]}"), style={"color": "green"})]
        
        # Add probability if available
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_df)
            
            # Get class names if available
            if hasattr(model, "classes_"):
                class_names = model.classes_
                proba_df = pd.DataFrame([proba[0]], columns=class_names)
            else:
                proba_df = pd.DataFrame([proba[0]], columns=[f"Class {i}" for i in range(proba.shape[1])])
            
            output.append(html.H4("Prediction Probabilities:"))
            output.append(dash_table.DataTable(
                data=proba_df.to_dict("records"),
                columns=[{"name": str(i), "id": str(i)} for i in proba_df.columns],
                style_table={"overflowX": "auto"}
            ))
        
        return html.Div(output)
    except Exception as e:
        return html.Div(html.H3(f"Error: {str(e)}"), style={"color": "red"})

# Model parameters callback
@callback(
    Output("model-parameters", "children"),
    [Input("model-parameters", "children")]
)
def update_model_parameters(_):
    if hasattr(model, "get_params"):
        params = model.get_params()
        params_df = pd.DataFrame({"Parameter": list(params.keys()), "Value": list(params.values())})
        
        return dash_table.DataTable(
            data=params_df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in params_df.columns],
            page_size=10,
            style_table={"overflowX": "auto"}
        )
    else:
        return html.P("Model parameters not available.")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
"""
                }
            }
        )
        
        # Flask templates
        self.register_template(
            "flask_basic",
            "Basic Flask App",
            "flask",
            {
                "description": "A basic Flask application template.",
                "files": {
                    "app.py": """
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", title="{{ app_title }}")

{{ content }}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
""",
                    "templates/index.html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <h1>{{ title }}</h1>
        <p>{{ app_description }}</p>
    </header>
    
    <main>
        <!-- Main content will go here -->
    </main>
    
    <footer>
        <p>&copy; {{ current_year }} {{ app_title }}</p>
    </footer>
    
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
""",
                    "static/css/style.css": """
/* Basic styles */
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    color: #333;
}

header {
    background-color: #f4f4f4;
    padding: 1rem;
    text-align: center;
}

main {
    padding: 1rem;
    max-width: 1200px;
    margin: 0 auto;
}

footer {
    background-color: #f4f4f4;
    padding: 1rem;
    text-align: center;
    margin-top: 2rem;
}
""",
                    "static/js/script.js": """
// JavaScript for the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Application loaded');
});
"""
                }
            }
        )
        
        self.register_template(
            "flask_ml_api",
            "ML API (Flask)",
            "flask",
            {
                "description": "A Flask API for machine learning models.",
                "files": {
                    "app.py": """
from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import pickle
import os
import json

app = Flask(__name__)

# Load model
def load_model():
    with open("{{ model_path }}", "rb") as f:
        return pickle.load(f)

try:
    model = load_model()
    print(f"Model loaded: {type(model).__name__}")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

# Get feature names
try:
    if hasattr(model, "feature_names_in_"):
        feature_names = model.feature_names_in_.tolist()
    else:
        # Try to load feature names from a file
        try:
            with open("{{ feature_names_path }}", "r") as f:
                feature_names = json.load(f)
        except:
            feature_names = []
except:
    feature_names = []

@app.route("/")
def index():
    return render_template("index.html", 
                          title="{{ app_title }}", 
                          description="{{ app_description }}",
                          feature_names=feature_names)

@app.route("/api/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        # Get input data
        data = request.json
        
        # Validate input
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid input format. Expected JSON object."}), 400
        
        # Create input DataFrame
        input_df = pd.DataFrame([data])
        
        # Check if all required features are present
        if feature_names and not all(feature in input_df.columns for feature in feature_names):
            missing_features = [feature for feature in feature_names if feature not in input_df.columns]
            return jsonify({"error": f"Missing features: {', '.join(missing_features)}"}), 400
        
        # Make prediction
        prediction = model.predict(input_df)
        
        # Prepare response
        response = {
            "prediction": prediction[0].tolist() if isinstance(prediction[0], (np.ndarray, list)) else float(prediction[0])
        }
        
        # Add probability if available
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_df)
            
            # Get class names if available
            if hasattr(model, "classes_"):
                class_names = model.classes_.tolist()
                response["probabilities"] = {str(class_name): float(prob) for class_name, prob in zip(class_names, proba[0])}
            else:
                response["probabilities"] = {f"class_{i}": float(prob) for i, prob in enumerate(proba[0])}
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/model-info")
def model_info():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        # Get model information
        info = {
            "model_type": type(model).__name__,
            "feature_names": feature_names
        }
        
        # Add model parameters if available
        if hasattr(model, "get_params"):
            params = model.get_params()
            info["parameters"] = {k: str(v) for k, v in params.items()}
        
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
""",
                    "templates/index.html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <h1>{{ title }}</h1>
        <p>{{ description }}</p>
    </header>
    
    <main>
        <section class="api-docs">
            <h2>API Documentation</h2>
            
            <div class="endpoint">
                <h3>Prediction Endpoint</h3>
                <p><strong>URL:</strong> <code>/api/predict</code></p>
                <p><strong>Method:</strong> POST</p>
                <p><strong>Content-Type:</strong> application/json</p>
                
                <h4>Request Body:</h4>
                <pre><code>{
    {% for feature in feature_names %}
    "{{ feature }}": value{% if not loop.last %},{% endif %}
    {% endfor %}
}</code></pre>
                
                <h4>Response:</h4>
                <pre><code>{
    "prediction": value
    {% if has_probabilities %}
    "probabilities": {
        "class_1": probability_1,
        "class_2": probability_2,
        ...
    }
    {% endif %}
}</code></pre>
            </div>
            
            <div class="endpoint">
                <h3>Model Information Endpoint</h3>
                <p><strong>URL:</strong> <code>/api/model-info</code></p>
                <p><strong>Method:</strong> GET</p>
                
                <h4>Response:</h4>
                <pre><code>{
    "model_type": "ModelType",
    "feature_names": ["feature1", "feature2", ...],
    "parameters": {
        "param1": "value1",
        "param2": "value2",
        ...
    }
}</code></pre>
            </div>
        </section>
        
        <section class="test-api">
            <h2>Test API</h2>
            
            <div class="input-form">
                <h3>Input Features</h3>
                
                <form id="prediction-form">
                    {% for feature in feature_names %}
                    <div class="form-group">
                        <label for="{{ feature }}">{{ feature }}</label>
                        <input type="number" id="{{ feature }}" name="{{ feature }}" step="0.01" required>
                    </div>
                    {% endfor %}
                    
                    <button type="submit">Predict</button>
                </form>
            </div>
            
            <div class="output-result">
                <h3>Prediction Result</h3>
                <div id="prediction-result"></div>
            </div>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2023 {{ title }}</p>
    </footer>
    
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
""",
                    "static/css/style.css": """
/* Basic styles */
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    color: #333;
}

header {
    background-color: #f4f4f4;
    padding: 1rem;
    text-align: center;
}

main {
    padding: 1rem;
    max-width: 1200px;
    margin: 0 auto;
}

footer {
    background-color: #f4f4f4;
    padding: 1rem;
    text-align: center;
    margin-top: 2rem;
}

/* API Documentation */
.api-docs {
    margin-bottom: 2rem;
}

.endpoint {
    background-color: #f9f9f9;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 5px;
}

pre {
    background-color: #f1f1f1;
    padding: 1rem;
    border-radius: 5px;
    overflow-x: auto;
}

code {
    font-family: monospace;
}

/* Test API */
.test-api {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
}

.input-form, .output-result {
    flex: 1;
    min-width: 300px;
}

.form-group {
    margin-bottom: 1rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
}

input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 3px;
}

button {
    background-color: #4CAF50;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}

#prediction-result {
    background-color: #f9f9f9;
    padding: 1rem;
    border-radius: 5px;
    min-height: 100px;
}
""",
                    "static/js/script.js": """
// JavaScript for the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Application loaded');
    
    // Get prediction form
    const predictionForm = document.getElementById('prediction-form');
    
    // Add submit event listener
    if (predictionForm) {
        predictionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(predictionForm);
            const data = {};
            
            // Convert form data to JSON
            for (const [key, value] of formData.entries()) {
                data[key] = parseFloat(value);
            }
            
            // Make prediction request
            fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                // Display prediction result
                const predictionResult = document.getElementById('prediction-result');
                
                if (result.error) {
                    predictionResult.innerHTML = `<div class="error">${result.error}</div>`;
                } else {
                    let html = `<div class="prediction">Prediction: <strong>${result.prediction}</strong></div>`;
                    
                    // Display probabilities if available
                    if (result.probabilities) {
                        html += '<div class="probabilities"><h4>Probabilities:</h4><ul>';
                        
                        for (const [className, probability] of Object.entries(result.probabilities)) {
                            html += `<li>${className}: ${(probability * 100).toFixed(2)}%</li>`;
                        }
                        
                        html += '</ul></div>';
                    }
                    
                    predictionResult.innerHTML = html;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const predictionResult = document.getElementById('prediction-result');
                predictionResult.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            });
        });
    }
});
"""
                }
            }
        )
        
        # HTML templates
        self.register_template(
            "html_basic",
            "Basic HTML Page",
            "html",
            {
                "description": "A basic HTML page template.",
                "files": {
                    "index.html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ app_title }}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <h1>{{ app_title }}</h1>
        <p>{{ app_description }}</p>
    </header>
    
    <main>
        <!-- Main content will go here -->
        {{ content }}
    </main>
    
    <footer>
        <p>&copy; 2023 {{ app_title }}</p>
    </footer>
    
    <script src="js/script.js"></script>
</body>
</html>
""",
                    "css/style.css": """
/* Basic styles */
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    color: #333;
}

header {
    background-color: #f4f4f4;
    padding: 1rem;
    text-align: center;
}

main {
    padding: 1rem;
    max-width: 1200px;
    margin: 0 auto;
}

footer {
    background-color: #f4f4f4;
    padding: 1rem;
    text-align: center;
    margin-top: 2rem;
}
""",
                    "js/script.js": """
// JavaScript for the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Application loaded');
});
"""
                }
            }
        )
        
        # React templates
        self.register_template(
            "react_basic",
            "Basic React App",
            "react",
            {
                "description": "A basic React application template.",
                "files": {
                    "package.json": """
{
  "name": "{{ app_name }}",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
""",
                    "public/index.html": """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="{{ app_description }}"
    />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <title>{{ app_title }}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
""",
                    "src/index.js": """
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

reportWebVitals();
""",
                    "src/App.js": """
import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>{{ app_title }}</h1>
        <p>{{ app_description }}</p>
      </header>
      
      <main className="App-main">
        {/* Main content will go here */}
        {{ content }}
      </main>
      
      <footer className="App-footer">
        <p>&copy; 2023 {{ app_title }}</p>
      </footer>
    </div>
  );
}

export default App;
""",
                    "src/App.css": """
.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  min-height: 20vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
  padding: 1rem;
}

.App-main {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.App-footer {
  background-color: #f4f4f4;
  padding: 1rem;
  text-align: center;
  margin-top: 2rem;
}
""",
                    "src/index.css": """
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
""",
                    "src/reportWebVitals.js": """
const reportWebVitals = (onPerfEntry) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};

export default reportWebVitals;
"""
                }
            }
        )
        
        # Vue templates
        self.register_template(
            "vue_basic",
            "Basic Vue App",
            "vue",
            {
                "description": "A basic Vue application template.",
                "files": {
                    "package.json": """
{
  "name": "{{ app_name }}",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "serve": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "lint": "vue-cli-service lint"
  },
  "dependencies": {
    "core-js": "^3.8.3",
    "vue": "^3.2.13"
  },
  "devDependencies": {
    "@babel/core": "^7.12.16",
    "@babel/eslint-parser": "^7.12.16",
    "@vue/cli-plugin-babel": "~5.0.0",
    "@vue/cli-plugin-eslint": "~5.0.0",
    "@vue/cli-service": "~5.0.0",
    "eslint": "^7.32.0",
    "eslint-plugin-vue": "^8.0.3"
  },
  "eslintConfig": {
    "root": true,
    "env": {
      "node": true
    },
    "extends": [
      "plugin:vue/vue3-essential",
      "eslint:recommended"
    ],
    "parserOptions": {
      "parser": "@babel/eslint-parser"
    },
    "rules": {}
  },
  "browserslist": [
    "> 1%",
    "last 2 versions",
    "not dead",
    "not ie 11"
  ]
}
""",
                    "public/index.html": """
<!DOCTYPE html>
<html lang="">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="icon" href="<%= BASE_URL %>favicon.ico">
    <title>{{ app_title }}</title>
  </head>
  <body>
    <noscript>
      <strong>We're sorry but {{ app_title }} doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>
    </noscript>
    <div id="app"></div>
    <!-- built files will be auto injected -->
  </body>
</html>
""",
                    "src/main.js": """
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
""",
                    "src/App.vue": """
<template>
  <div id="app">
    <header class="app-header">
      <h1>{{ app_title }}</h1>
      <p>{{ app_description }}</p>
    </header>
    
    <main class="app-main">
      <!-- Main content will go here -->
      {{ content }}
    </main>
    
    <footer class="app-footer">
      <p>&copy; 2023 {{ app_title }}</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      app_title: '{{ app_title }}',
      app_description: '{{ app_description }}'
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.app-header {
  background-color: #282c34;
  min-height: 20vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
  padding: 1rem;
  text-align: center;
}

.app-main {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.app-footer {
  background-color: #f4f4f4;
  padding: 1rem;
  text-align: center;
  margin-top: 2rem;
}
</style>
"""
                }
            }
        )
    
    def register_template(self, template_id: str, template_name: str,
                         framework: str, config: Dict[str, Any]) -> None:
        """
        Register a template in the manager.
        
        Args:
            template_id: Unique identifier for the template.
            template_name: Display name for the template.
            framework: Framework to which the template belongs.
            config: Configuration for the template.
        """
        if template_id in self.templates:
            raise UIGenerationError(f"Template ID '{template_id}' already exists.")
        
        if framework not in self.template_dirs:
            raise UIGenerationError(f"Framework '{framework}' is not supported.")
        
        template = {
            "id": template_id,
            "name": template_name,
            "framework": framework,
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
            raise UIGenerationError(f"Template ID '{template_id}' does not exist.")
        
        return self.templates[template_id]
    
    def get_templates_by_framework(self, framework: str) -> List[Dict[str, Any]]:
        """
        Get all templates for a framework.
        
        Args:
            framework: Framework to get templates for.
            
        Returns:
            List of templates for the framework.
        """
        if framework not in self.template_dirs:
            raise UIGenerationError(f"Framework '{framework}' is not supported.")
        
        return [template for template in self.templates.values() if template["framework"] == framework]
    
    def get_all_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all templates.
        
        Returns:
            Dictionary of all templates.
        """
        return self.templates
    
    def apply_template(self, template_id: str, output_dir: str,
                      context: Dict[str, Any]) -> str:
        """
        Apply a template to generate files.
        
        Args:
            template_id: ID of the template to apply.
            output_dir: Directory to output generated files.
            context: Context variables for template rendering.
            
        Returns:
            Path to the output directory.
        """
        template = self.get_template(template_id)
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create Jinja2 environment
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dirs[template["framework"]]),
            autoescape=jinja2.select_autoescape(["html", "xml"])
        )
        
        # Process each file in the template
        for file_path, file_content in template["config"]["files"].items():
            # Create directory for file if it doesn't exist
            file_dir = os.path.dirname(os.path.join(output_dir, file_path))
            if file_dir and not os.path.exists(file_dir):
                os.makedirs(file_dir)
            
            # Render file content
            template_obj = jinja2.Template(file_content)
            rendered_content = template_obj.render(**context)
            
            # Write file
            with open(os.path.join(output_dir, file_path), "w") as f:
                f.write(rendered_content)
        
        return output_dir
    
    def create_custom_template(self, template_id: str, template_name: str,
                              framework: str, files: Dict[str, str],
                              description: str = "") -> None:
        """
        Create a custom template.
        
        Args:
            template_id: Unique identifier for the template.
            template_name: Display name for the template.
            framework: Framework to which the template belongs.
            files: Dictionary of file paths and contents.
            description: Description of the template.
        """
        config = {
            "description": description,
            "files": files
        }
        
        self.register_template(template_id, template_name, framework, config)
    
    def save_template(self, template_id: str) -> None:
        """
        Save a template to disk.
        
        Args:
            template_id: ID of the template to save.
        """
        template = self.get_template(template_id)
        
        # Create template directory
        template_dir = os.path.join(self.template_dirs[template["framework"]], template_id)
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)
        
        # Save template metadata
        metadata = {
            "id": template["id"],
            "name": template["name"],
            "framework": template["framework"],
            "description": template["config"]["description"]
        }
        
        with open(os.path.join(template_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Save template files
        for file_path, file_content in template["config"]["files"].items():
            # Create directory for file if it doesn't exist
            file_dir = os.path.dirname(os.path.join(template_dir, "files", file_path))
            if file_dir and not os.path.exists(file_dir):
                os.makedirs(file_dir)
            
            # Write file
            with open(os.path.join(template_dir, "files", file_path), "w") as f:
                f.write(file_content)
    
    def load_template_from_disk(self, framework: str, template_id: str) -> None:
        """
        Load a template from disk.
        
        Args:
            framework: Framework to which the template belongs.
            template_id: ID of the template to load.
        """
        template_dir = os.path.join(self.template_dirs[framework], template_id)
        
        if not os.path.exists(template_dir):
            raise UIGenerationError(f"Template directory '{template_dir}' does not exist.")
        
        # Load template metadata
        with open(os.path.join(template_dir, "metadata.json"), "r") as f:
            metadata = json.load(f)
        
        # Load template files
        files = {}
        files_dir = os.path.join(template_dir, "files")
        
        for root, _, filenames in os.walk(files_dir):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, files_dir)
                
                with open(file_path, "r") as f:
                    files[relative_path] = f.read()
        
        # Register template
        self.register_template(
            metadata["id"],
            metadata["name"],
            metadata["framework"],
            {
                "description": metadata["description"],
                "files": files
            }
        )
    
    def export_template(self, template_id: str, output_path: str) -> str:
        """
        Export a template to a zip file.
        
        Args:
            template_id: ID of the template to export.
            output_path: Path to save the exported template.
            
        Returns:
            Path to the exported template.
        """
        import zipfile
        
        template = self.get_template(template_id)
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save template metadata
            metadata = {
                "id": template["id"],
                "name": template["name"],
                "framework": template["framework"],
                "description": template["config"]["description"]
            }
            
            with open(os.path.join(temp_dir, "metadata.json"), "w") as f:
                json.dump(metadata, f, indent=2)
            
            # Save template files
            for file_path, file_content in template["config"]["files"].items():
                # Create directory for file if it doesn't exist
                file_dir = os.path.dirname(os.path.join(temp_dir, "files", file_path))
                if file_dir and not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                
                # Write file
                with open(os.path.join(temp_dir, "files", file_path), "w") as f:
                    f.write(file_content)
            
            # Create zip file
            zip_path = output_path if output_path.endswith(".zip") else f"{output_path}.zip"
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)
        
        return zip_path
    
    def import_template(self, zip_path: str) -> str:
        """
        Import a template from a zip file.
        
        Args:
            zip_path: Path to the zip file.
            
        Returns:
            ID of the imported template.
        """
        import zipfile
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract zip file
            with zipfile.ZipFile(zip_path, "r") as zipf:
                zipf.extractall(temp_dir)
            
            # Load template metadata
            with open(os.path.join(temp_dir, "metadata.json"), "r") as f:
                metadata = json.load(f)
            
            # Load template files
            files = {}
            files_dir = os.path.join(temp_dir, "files")
            
            for root, _, filenames in os.walk(files_dir):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, files_dir)
                    
                    with open(file_path, "r") as f:
                        files[relative_path] = f.read()
            
            # Register template
            self.register_template(
                metadata["id"],
                metadata["name"],
                metadata["framework"],
                {
                    "description": metadata["description"],
                    "files": files
                }
            )
            
            return metadata["id"]
