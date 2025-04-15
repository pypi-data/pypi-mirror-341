"""
Dashboard generator component for SBYB UI Generator.

This module provides functionality for generating interactive dashboards
for machine learning models without writing code.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import shutil
import tempfile

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import UIGenerationError


class DashboardGenerator(SBYBComponent):
    """
    Dashboard generator component.
    
    This component generates interactive dashboards for machine learning models.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the dashboard generator.
        
        Args:
            config: Configuration dictionary for the generator.
        """
        super().__init__(config)
        self.components = []
        self.layout = {}
        self.data_sources = {}
        self.callbacks = {}
        self.theme = "default"
    
    def add_component(self, component_type: str, component_id: str, 
                     title: Optional[str] = None, 
                     config: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a component to the dashboard.
        
        Args:
            component_type: Type of component.
            component_id: Unique identifier for the component.
            title: Title of the component.
            config: Configuration for the component.
            
        Returns:
            ID of the added component.
        """
        # Check if component ID already exists
        if any(comp["id"] == component_id for comp in self.components):
            raise UIGenerationError(f"Component ID '{component_id}' already exists.")
        
        # Create component
        component = {
            "id": component_id,
            "type": component_type,
            "title": title or component_id,
            "config": config or {}
        }
        
        # Add component
        self.components.append(component)
        
        return component_id
    
    def add_data_source(self, source_id: str, source_type: str, 
                       config: Dict[str, Any]) -> str:
        """
        Add a data source to the dashboard.
        
        Args:
            source_id: Unique identifier for the data source.
            source_type: Type of data source.
            config: Configuration for the data source.
            
        Returns:
            ID of the added data source.
        """
        # Check if source ID already exists
        if source_id in self.data_sources:
            raise UIGenerationError(f"Data source ID '{source_id}' already exists.")
        
        # Create data source
        data_source = {
            "type": source_type,
            "config": config
        }
        
        # Add data source
        self.data_sources[source_id] = data_source
        
        return source_id
    
    def add_callback(self, callback_id: str, inputs: List[str], 
                    outputs: List[str], function: str) -> str:
        """
        Add a callback to the dashboard.
        
        Args:
            callback_id: Unique identifier for the callback.
            inputs: List of input component IDs.
            outputs: List of output component IDs.
            function: JavaScript function code.
            
        Returns:
            ID of the added callback.
        """
        # Check if callback ID already exists
        if callback_id in self.callbacks:
            raise UIGenerationError(f"Callback ID '{callback_id}' already exists.")
        
        # Check if input components exist
        for input_id in inputs:
            if not any(comp["id"] == input_id for comp in self.components):
                raise UIGenerationError(f"Input component ID '{input_id}' does not exist.")
        
        # Check if output components exist
        for output_id in outputs:
            if not any(comp["id"] == output_id for comp in self.components):
                raise UIGenerationError(f"Output component ID '{output_id}' does not exist.")
        
        # Create callback
        callback = {
            "inputs": inputs,
            "outputs": outputs,
            "function": function
        }
        
        # Add callback
        self.callbacks[callback_id] = callback
        
        return callback_id
    
    def set_layout(self, layout_type: str, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Set the layout of the dashboard.
        
        Args:
            layout_type: Type of layout.
            config: Configuration for the layout.
        """
        self.layout = {
            "type": layout_type,
            "config": config or {}
        }
    
    def set_theme(self, theme: str) -> None:
        """
        Set the theme of the dashboard.
        
        Args:
            theme: Theme name.
        """
        self.theme = theme
    
    def generate_dashboard(self, output_dir: str, dashboard_name: str = "ML Dashboard",
                          framework: str = "streamlit") -> str:
        """
        Generate a dashboard.
        
        Args:
            output_dir: Directory to save the generated dashboard.
            dashboard_name: Name of the dashboard.
            framework: Framework to use for the dashboard.
            
        Returns:
            Path to the generated dashboard.
        """
        if framework.lower() == "streamlit":
            return self._generate_streamlit_dashboard(output_dir, dashboard_name)
        elif framework.lower() == "dash":
            return self._generate_dash_dashboard(output_dir, dashboard_name)
        elif framework.lower() == "gradio":
            return self._generate_gradio_dashboard(output_dir, dashboard_name)
        else:
            raise UIGenerationError(f"Unsupported framework: {framework}")
    
    def _generate_streamlit_dashboard(self, output_dir: str, dashboard_name: str) -> str:
        """
        Generate a Streamlit dashboard.
        
        Args:
            output_dir: Directory to save the generated dashboard.
            dashboard_name: Name of the dashboard.
            
        Returns:
            Path to the generated dashboard.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate app.py
        app_py_content = self._generate_streamlit_app(dashboard_name)
        
        with open(os.path.join(output_dir, "app.py"), "w") as f:
            f.write(app_py_content)
        
        # Generate requirements.txt
        requirements_txt_content = self._generate_streamlit_requirements()
        
        with open(os.path.join(output_dir, "requirements.txt"), "w") as f:
            f.write(requirements_txt_content)
        
        # Generate README.md
        readme_md_content = self._generate_streamlit_readme(dashboard_name)
        
        with open(os.path.join(output_dir, "README.md"), "w") as f:
            f.write(readme_md_content)
        
        # Generate config.toml
        os.makedirs(os.path.join(output_dir, ".streamlit"), exist_ok=True)
        config_toml_content = self._generate_streamlit_config(dashboard_name)
        
        with open(os.path.join(output_dir, ".streamlit", "config.toml"), "w") as f:
            f.write(config_toml_content)
        
        # Generate dashboard configuration
        dashboard_config = {
            "name": dashboard_name,
            "components": self.components,
            "layout": self.layout,
            "data_sources": self.data_sources,
            "callbacks": self.callbacks,
            "theme": self.theme
        }
        
        with open(os.path.join(output_dir, "dashboard_config.json"), "w") as f:
            json.dump(dashboard_config, f, indent=2)
        
        return output_dir
    
    def _generate_dash_dashboard(self, output_dir: str, dashboard_name: str) -> str:
        """
        Generate a Dash dashboard.
        
        Args:
            output_dir: Directory to save the generated dashboard.
            dashboard_name: Name of the dashboard.
            
        Returns:
            Path to the generated dashboard.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate app.py
        app_py_content = self._generate_dash_app(dashboard_name)
        
        with open(os.path.join(output_dir, "app.py"), "w") as f:
            f.write(app_py_content)
        
        # Generate requirements.txt
        requirements_txt_content = self._generate_dash_requirements()
        
        with open(os.path.join(output_dir, "requirements.txt"), "w") as f:
            f.write(requirements_txt_content)
        
        # Generate README.md
        readme_md_content = self._generate_dash_readme(dashboard_name)
        
        with open(os.path.join(output_dir, "README.md"), "w") as f:
            f.write(readme_md_content)
        
        # Generate assets directory
        os.makedirs(os.path.join(output_dir, "assets"), exist_ok=True)
        
        # Generate custom CSS
        custom_css_content = self._generate_dash_css()
        
        with open(os.path.join(output_dir, "assets", "custom.css"), "w") as f:
            f.write(custom_css_content)
        
        # Generate dashboard configuration
        dashboard_config = {
            "name": dashboard_name,
            "components": self.components,
            "layout": self.layout,
            "data_sources": self.data_sources,
            "callbacks": self.callbacks,
            "theme": self.theme
        }
        
        with open(os.path.join(output_dir, "dashboard_config.json"), "w") as f:
            json.dump(dashboard_config, f, indent=2)
        
        return output_dir
    
    def _generate_gradio_dashboard(self, output_dir: str, dashboard_name: str) -> str:
        """
        Generate a Gradio dashboard.
        
        Args:
            output_dir: Directory to save the generated dashboard.
            dashboard_name: Name of the dashboard.
            
        Returns:
            Path to the generated dashboard.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate app.py
        app_py_content = self._generate_gradio_app(dashboard_name)
        
        with open(os.path.join(output_dir, "app.py"), "w") as f:
            f.write(app_py_content)
        
        # Generate requirements.txt
        requirements_txt_content = self._generate_gradio_requirements()
        
        with open(os.path.join(output_dir, "requirements.txt"), "w") as f:
            f.write(requirements_txt_content)
        
        # Generate README.md
        readme_md_content = self._generate_gradio_readme(dashboard_name)
        
        with open(os.path.join(output_dir, "README.md"), "w") as f:
            f.write(readme_md_content)
        
        # Generate dashboard configuration
        dashboard_config = {
            "name": dashboard_name,
            "components": self.components,
            "layout": self.layout,
            "data_sources": self.data_sources,
            "callbacks": self.callbacks,
            "theme": self.theme
        }
        
        with open(os.path.join(output_dir, "dashboard_config.json"), "w") as f:
            json.dump(dashboard_config, f, indent=2)
        
        return output_dir
    
    def _generate_streamlit_app(self, dashboard_name: str) -> str:
        """
        Generate Streamlit app.py content.
        
        Args:
            dashboard_name: Name of the dashboard.
            
        Returns:
            Content of app.py.
        """
        content = f"""
import os
import json
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Set page title and layout
st.set_page_config(
    page_title="{dashboard_name}",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load dashboard configuration
with open("dashboard_config.json", "r") as f:
    dashboard_config = json.load(f)

# Set dashboard title
st.title(dashboard_config["name"])

# Load data sources
@st.cache_data
def load_data_sources():
    data_sources = {{}}
    
    for source_id, source_config in dashboard_config["data_sources"].items():
        source_type = source_config["type"]
        config = source_config["config"]
        
        if source_type == "csv":
            data_sources[source_id] = pd.read_csv(config["path"])
        elif source_type == "excel":
            data_sources[source_id] = pd.read_excel(config["path"])
        elif source_type == "json":
            data_sources[source_id] = pd.read_json(config["path"])
        elif source_type == "pickle":
            with open(config["path"], "rb") as f:
                data_sources[source_id] = pickle.load(f)
        elif source_type == "model":
            with open(config["path"], "rb") as f:
                data_sources[source_id] = pickle.load(f)
    
    return data_sources

data_sources = load_data_sources()

# Create layout
layout_type = dashboard_config["layout"]["type"]
layout_config = dashboard_config["layout"]["config"]

if layout_type == "tabs":
    tabs = st.tabs([tab["title"] for tab in layout_config["tabs"]])
    
    for i, tab in enumerate(layout_config["tabs"]):
        with tabs[i]:
            for component_id in tab["components"]:
                render_component(component_id)
elif layout_type == "columns":
    cols = st.columns(layout_config["column_widths"])
    
    for i, column in enumerate(layout_config["columns"]):
        with cols[i]:
            for component_id in column["components"]:
                render_component(component_id)
elif layout_type == "sidebar":
    with st.sidebar:
        for component_id in layout_config["sidebar_components"]:
            render_component(component_id)
    
    for component_id in layout_config["main_components"]:
        render_component(component_id)
else:
    # Default layout: render all components sequentially
    for component in dashboard_config["components"]:
        render_component(component["id"])

# Function to render a component
def render_component(component_id):
    # Find component by ID
    component = next((comp for comp in dashboard_config["components"] if comp["id"] == component_id), None)
    
    if component is None:
        st.error(f"Component with ID '{component_id}' not found.")
        return
    
    component_type = component["type"]
    component_title = component["title"]
    component_config = component["config"]
    
    # Render component based on type
    if component_type == "text":
        st.markdown(component_config["text"])
    
    elif component_type == "header":
        level = component_config.get("level", 2)
        if level == 1:
            st.title(component_title)
        elif level == 2:
            st.header(component_title)
        elif level == 3:
            st.subheader(component_title)
        else:
            st.markdown(f"{'#' * level} {{component_title}}")
    
    elif component_type == "data_table":
        data_source_id = component_config["data_source"]
        if data_source_id in data_sources:
            data = data_sources[data_source_id]
            st.dataframe(data)
        else:
            st.error(f"Data source '{data_source_id}' not found.")
    
    elif component_type == "chart":
        chart_type = component_config["chart_type"]
        data_source_id = component_config["data_source"]
        
        if data_source_id not in data_sources:
            st.error(f"Data source '{data_source_id}' not found.")
            return
        
        data = data_sources[data_source_id]
        
        if chart_type == "bar":
            x = component_config["x"]
            y = component_config["y"]
            st.bar_chart(data.set_index(x)[y])
        
        elif chart_type == "line":
            x = component_config["x"]
            y = component_config["y"]
            st.line_chart(data.set_index(x)[y])
        
        elif chart_type == "area":
            x = component_config["x"]
            y = component_config["y"]
            st.area_chart(data.set_index(x)[y])
        
        elif chart_type == "scatter":
            x = component_config["x"]
            y = component_config["y"]
            
            fig, ax = plt.subplots()
            sns.scatterplot(data=data, x=x, y=y, ax=ax)
            st.pyplot(fig)
        
        elif chart_type == "histogram":
            column = component_config["column"]
            bins = component_config.get("bins", 10)
            
            fig, ax = plt.subplots()
            sns.histplot(data=data, x=column, bins=bins, ax=ax)
            st.pyplot(fig)
        
        elif chart_type == "boxplot":
            column = component_config["column"]
            
            fig, ax = plt.subplots()
            sns.boxplot(data=data, y=column, ax=ax)
            st.pyplot(fig)
        
        elif chart_type == "heatmap":
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(data.corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
    
    elif component_type == "metric":
        data_source_id = component_config["data_source"]
        metric_name = component_config["metric"]
        
        if data_source_id not in data_sources:
            st.error(f"Data source '{data_source_id}' not found.")
            return
        
        data = data_sources[data_source_id]
        
        if metric_name == "count":
            value = len(data)
        elif metric_name == "mean":
            column = component_config["column"]
            value = data[column].mean()
        elif metric_name == "sum":
            column = component_config["column"]
            value = data[column].sum()
        elif metric_name == "min":
            column = component_config["column"]
            value = data[column].min()
        elif metric_name == "max":
            column = component_config["column"]
            value = data[column].max()
        else:
            value = "Unknown metric"
        
        st.metric(label=component_title, value=value)
    
    elif component_type == "input":
        input_type = component_config["input_type"]
        
        if input_type == "text":
            st.text_input(component_title, key=component_id)
        elif input_type == "number":
            st.number_input(component_title, key=component_id)
        elif input_type == "slider":
            min_value = component_config.get("min_value", 0)
            max_value = component_config.get("max_value", 100)
            value = component_config.get("value", min_value)
            st.slider(component_title, min_value=min_value, max_value=max_value, value=value, key=component_id)
        elif input_type == "select":
            options = component_config["options"]
            st.selectbox(component_title, options=options, key=component_id)
        elif input_type == "multiselect":
            options = component_config["options"]
            st.multiselect(component_title, options=options, key=component_id)
        elif input_type == "checkbox":
            value = component_config.get("value", False)
            st.checkbox(component_title, value=value, key=component_id)
        elif input_type == "date":
            st.date_input(component_title, key=component_id)
        elif input_type == "file":
            st.file_uploader(component_title, key=component_id)
    
    elif component_type == "button":
        st.button(component_title, key=component_id)
    
    elif component_type == "divider":
        st.divider()
    
    elif component_type == "image":
        image_path = component_config["path"]
        caption = component_config.get("caption", "")
        
        if os.path.exists(image_path):
            st.image(image_path, caption=caption)
        else:
            st.error(f"Image file '{image_path}' not found.")
    
    elif component_type == "model_prediction":
        model_source_id = component_config["model_source"]
        
        if model_source_id not in data_sources:
            st.error(f"Model source '{model_source_id}' not found.")
            return
        
        model = data_sources[model_source_id]
        
        # Create input fields based on model features
        st.subheader("Model Prediction")
        
        input_values = {{}}
        
        if hasattr(model, "feature_names_in_"):
            feature_names = model.feature_names_in_
        else:
            feature_names = component_config.get("feature_names", [])
        
        for feature in feature_names:
            input_values[feature] = st.number_input(f"{{feature}}", key=f"{{component_id}}_{{feature}}")
        
        if st.button("Predict", key=f"{{component_id}}_predict"):
            try:
                # Create input DataFrame
                input_df = pd.DataFrame([input_values])
                
                # Make prediction
                prediction = model.predict(input_df)
                
                st.success(f"Prediction: {{prediction[0]}}")
                
                # Show probability if available
                if hasattr(model, "predict_proba"):
                    probabilities = model.predict_proba(input_df)
                    st.write("Prediction probabilities:")
                    
                    # Get class names if available
                    if hasattr(model, "classes_"):
                        class_names = model.classes_
                        prob_df = pd.DataFrame([probabilities[0]], columns=class_names)
                    else:
                        prob_df = pd.DataFrame([probabilities[0]], columns=[f"Class {{i}}" for i in range(probabilities.shape[1])])
                    
                    st.dataframe(prob_df)
            except Exception as e:
                st.error(f"Error making prediction: {{str(e)}}")
"""
        
        return content
    
    def _generate_streamlit_requirements(self) -> str:
        """
        Generate Streamlit requirements.txt content.
        
        Returns:
            Content of requirements.txt.
        """
        return """
streamlit>=1.10.0
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.4.0
seaborn>=0.11.0
scikit-learn>=0.24.0
openpyxl>=3.0.0
"""
    
    def _generate_streamlit_readme(self, dashboard_name: str) -> str:
        """
        Generate Streamlit README.md content.
        
        Args:
            dashboard_name: Name of the dashboard.
            
        Returns:
            Content of README.md.
        """
        return f"""
# {dashboard_name}

This is a Streamlit dashboard generated by SBYB UI Generator.

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Dashboard

```
streamlit run app.py
```

The dashboard will be available at http://localhost:8501

## Features

- Interactive visualizations
- Data exploration
- Model predictions
- Customizable layout

## Configuration

The dashboard is configured using the `dashboard_config.json` file. You can modify this file to customize the dashboard.
"""
    
    def _generate_streamlit_config(self, dashboard_name: str) -> str:
        """
        Generate Streamlit config.toml content.
        
        Args:
            dashboard_name: Name of the dashboard.
            
        Returns:
            Content of config.toml.
        """
        return f"""
[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[global]
developmentMode = false
"""
    
    def _generate_dash_app(self, dashboard_name: str) -> str:
        """
        Generate Dash app.py content.
        
        Args:
            dashboard_name: Name of the dashboard.
            
        Returns:
            Content of app.py.
        """
        content = f"""
import os
import json
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pickle

# Load dashboard configuration
with open("dashboard_config.json", "r") as f:
    dashboard_config = json.load(f)

# Initialize Dash app
app = dash.Dash(
    __name__,
    title=dashboard_config["name"],
    meta_tags=[{{"name": "viewport", "content": "width=device-width, initial-scale=1"}}]
)
server = app.server

# Load data sources
def load_data_sources():
    data_sources = {{}}
    
    for source_id, source_config in dashboard_config["data_sources"].items():
        source_type = source_config["type"]
        config = source_config["config"]
        
        if source_type == "csv":
            data_sources[source_id] = pd.read_csv(config["path"])
        elif source_type == "excel":
            data_sources[source_id] = pd.read_excel(config["path"])
        elif source_type == "json":
            data_sources[source_id] = pd.read_json(config["path"])
        elif source_type == "pickle":
            with open(config["path"], "rb") as f:
                data_sources[source_id] = pickle.load(f)
        elif source_type == "model":
            with open(config["path"], "rb") as f:
                data_sources[source_id] = pickle.load(f)
    
    return data_sources

data_sources = load_data_sources()

# Create layout
def create_layout():
    layout_type = dashboard_config["layout"]["type"]
    layout_config = dashboard_config["layout"]["config"]
    
    if layout_type == "tabs":
        return html.Div([
            html.H1(dashboard_config["name"], className="dashboard-title"),
            dcc.Tabs(
                id="tabs",
                value=layout_config["tabs"][0]["id"],
                children=[
                    dcc.Tab(
                        label=tab["title"],
                        value=tab["id"],
                        children=[
                            html.Div(
                                [create_component(component_id) for component_id in tab["components"]],
                                className="tab-content"
                            )
                        ]
                    )
                    for tab in layout_config["tabs"]
                ]
            )
        ])
    
    elif layout_type == "columns":
        return html.Div([
            html.H1(dashboard_config["name"], className="dashboard-title"),
            html.Div(
                [
                    html.Div(
                        [create_component(component_id) for component_id in column["components"]],
                        className=f"column column-{{i+1}}",
                        style={{"width": f"{{column_width}}%"}}
                    )
                    for i, (column, column_width) in enumerate(zip(
                        layout_config["columns"],
                        layout_config["column_widths"]
                    ))
                ],
                className="columns-container"
            )
        ])
    
    elif layout_type == "sidebar":
        return html.Div([
            html.H1(dashboard_config["name"], className="dashboard-title"),
            html.Div([
                html.Div(
                    [create_component(component_id) for component_id in layout_config["sidebar_components"]],
                    className="sidebar"
                ),
                html.Div(
                    [create_component(component_id) for component_id in layout_config["main_components"]],
                    className="main-content"
                )
            ], className="sidebar-layout")
        ])
    
    else:
        # Default layout: render all components sequentially
        return html.Div([
            html.H1(dashboard_config["name"], className="dashboard-title"),
            html.Div(
                [create_component(component["id"]) for component in dashboard_config["components"]],
                className="default-layout"
            )
        ])

# Function to create a component
def create_component(component_id):
    # Find component by ID
    component = next((comp for comp in dashboard_config["components"] if comp["id"] == component_id), None)
    
    if component is None:
        return html.Div(f"Component with ID '{component_id}' not found.", className="error-message")
    
    component_type = component["type"]
    component_title = component["title"]
    component_config = component["config"]
    
    # Create component based on type
    if component_type == "text":
        return html.Div(component_config["text"], className="text-component")
    
    elif component_type == "header":
        level = component_config.get("level", 2)
        if level == 1:
            return html.H1(component_title, className="header-component")
        elif level == 2:
            return html.H2(component_title, className="header-component")
        elif level == 3:
            return html.H3(component_title, className="header-component")
        elif level == 4:
            return html.H4(component_title, className="header-component")
        elif level == 5:
            return html.H5(component_title, className="header-component")
        else:
            return html.H6(component_title, className="header-component")
    
    elif component_type == "data_table":
        data_source_id = component_config["data_source"]
        if data_source_id in data_sources:
            data = data_sources[data_source_id]
            return html.Div([
                html.H3(component_title, className="component-title"),
                dash_table.DataTable(
                    id=f"table-{{component_id}}",
                    columns=[{{"name": col, "id": col}} for col in data.columns],
                    data=data.to_dict("records"),
                    page_size=10,
                    style_table={{"overflowX": "auto"}},
                    style_cell={{"textAlign": "left", "padding": "10px"}},
                    style_header={{
                        "backgroundColor": "#f8f9fa",
                        "fontWeight": "bold"
                    }}
                )
            ], className="data-table-component")
        else:
            return html.Div(f"Data source '{data_source_id}' not found.", className="error-message")
    
    elif component_type == "chart":
        chart_type = component_config["chart_type"]
        data_source_id = component_config["data_source"]
        
        if data_source_id not in data_sources:
            return html.Div(f"Data source '{data_source_id}' not found.", className="error-message")
        
        data = data_sources[data_source_id]
        
        if chart_type == "bar":
            x = component_config["x"]
            y = component_config["y"]
            fig = px.bar(data, x=x, y=y, title=component_title)
        
        elif chart_type == "line":
            x = component_config["x"]
            y = component_config["y"]
            fig = px.line(data, x=x, y=y, title=component_title)
        
        elif chart_type == "area":
            x = component_config["x"]
            y = component_config["y"]
            fig = px.area(data, x=x, y=y, title=component_title)
        
        elif chart_type == "scatter":
            x = component_config["x"]
            y = component_config["y"]
            fig = px.scatter(data, x=x, y=y, title=component_title)
        
        elif chart_type == "histogram":
            column = component_config["column"]
            bins = component_config.get("bins", 10)
            fig = px.histogram(data, x=column, nbins=bins, title=component_title)
        
        elif chart_type == "boxplot":
            column = component_config["column"]
            fig = px.box(data, y=column, title=component_title)
        
        elif chart_type == "heatmap":
            fig = px.imshow(data.corr(), title=component_title)
        
        else:
            return html.Div(f"Chart type '{chart_type}' not supported.", className="error-message")
        
        return html.Div([
            dcc.Graph(
                id=f"chart-{{component_id}}",
                figure=fig
            )
        ], className="chart-component")
    
    elif component_type == "metric":
        data_source_id = component_config["data_source"]
        metric_name = component_config["metric"]
        
        if data_source_id not in data_sources:
            return html.Div(f"Data source '{data_source_id}' not found.", className="error-message")
        
        data = data_sources[data_source_id]
        
        if metric_name == "count":
            value = len(data)
        elif metric_name == "mean":
            column = component_config["column"]
            value = data[column].mean()
        elif metric_name == "sum":
            column = component_config["column"]
            value = data[column].sum()
        elif metric_name == "min":
            column = component_config["column"]
            value = data[column].min()
        elif metric_name == "max":
            column = component_config["column"]
            value = data[column].max()
        else:
            value = "Unknown metric"
        
        return html.Div([
            html.Div(component_title, className="metric-title"),
            html.Div(str(value), className="metric-value")
        ], className="metric-component")
    
    elif component_type == "input":
        input_type = component_config["input_type"]
        
        if input_type == "text":
            return html.Div([
                html.Label(component_title, className="input-label"),
                dcc.Input(
                    id=f"input-{{component_id}}",
                    type="text",
                    placeholder=component_config.get("placeholder", ""),
                    value=component_config.get("value", ""),
                    className="text-input"
                )
            ], className="input-component")
        
        elif input_type == "number":
            return html.Div([
                html.Label(component_title, className="input-label"),
                dcc.Input(
                    id=f"input-{{component_id}}",
                    type="number",
                    placeholder=component_config.get("placeholder", ""),
                    value=component_config.get("value", 0),
                    min=component_config.get("min", None),
                    max=component_config.get("max", None),
                    className="number-input"
                )
            ], className="input-component")
        
        elif input_type == "slider":
            return html.Div([
                html.Label(component_title, className="input-label"),
                dcc.Slider(
                    id=f"input-{{component_id}}",
                    min=component_config.get("min_value", 0),
                    max=component_config.get("max_value", 100),
                    value=component_config.get("value", 0),
                    marks={{i: str(i) for i in range(
                        component_config.get("min_value", 0),
                        component_config.get("max_value", 100) + 1,
                        (component_config.get("max_value", 100) - component_config.get("min_value", 0)) // 5
                    )}},
                    className="slider-input"
                )
            ], className="input-component")
        
        elif input_type == "select":
            options = component_config["options"]
            return html.Div([
                html.Label(component_title, className="input-label"),
                dcc.Dropdown(
                    id=f"input-{{component_id}}",
                    options=[{{"label": opt, "value": opt}} for opt in options],
                    value=options[0] if options else None,
                    className="select-input"
                )
            ], className="input-component")
        
        elif input_type == "multiselect":
            options = component_config["options"]
            return html.Div([
                html.Label(component_title, className="input-label"),
                dcc.Dropdown(
                    id=f"input-{{component_id}}",
                    options=[{{"label": opt, "value": opt}} for opt in options],
                    multi=True,
                    className="multiselect-input"
                )
            ], className="input-component")
        
        elif input_type == "checkbox":
            return html.Div([
                dcc.Checklist(
                    id=f"input-{{component_id}}",
                    options=[{{"label": component_title, "value": "checked"}}],
                    value=["checked"] if component_config.get("value", False) else [],
                    className="checkbox-input"
                )
            ], className="input-component")
        
        elif input_type == "date":
            return html.Div([
                html.Label(component_title, className="input-label"),
                dcc.DatePickerSingle(
                    id=f"input-{{component_id}}",
                    className="date-input"
                )
            ], className="input-component")
        
        elif input_type == "file":
            return html.Div([
                html.Label(component_title, className="input-label"),
                dcc.Upload(
                    id=f"input-{{component_id}}",
                    children=html.Div([
                        "Drag and Drop or ",
                        html.A("Select a File")
                    ]),
                    className="file-input"
                )
            ], className="input-component")
    
    elif component_type == "button":
        return html.Div([
            html.Button(
                component_title,
                id=f"button-{{component_id}}",
                className="button-component"
            )
        ])
    
    elif component_type == "divider":
        return html.Hr(className="divider-component")
    
    elif component_type == "image":
        image_path = component_config["path"]
        caption = component_config.get("caption", "")
        
        if os.path.exists(image_path):
            return html.Div([
                html.Img(src=image_path, className="image"),
                html.Div(caption, className="caption") if caption else None
            ], className="image-component")
        else:
            return html.Div(f"Image file '{image_path}' not found.", className="error-message")
    
    elif component_type == "model_prediction":
        model_source_id = component_config["model_source"]
        
        if model_source_id not in data_sources:
            return html.Div(f"Model source '{model_source_id}' not found.", className="error-message")
        
        model = data_sources[model_source_id]
        
        # Get feature names
        if hasattr(model, "feature_names_in_"):
            feature_names = model.feature_names_in_
        else:
            feature_names = component_config.get("feature_names", [])
        
        # Create input fields
        input_fields = []
        for feature in feature_names:
            input_fields.append(
                html.Div([
                    html.Label(feature, className="input-label"),
                    dcc.Input(
                        id=f"model-input-{{component_id}}-{{feature}}",
                        type="number",
                        value=0,
                        className="model-input"
                    )
                ], className="model-input-field")
            )
        
        return html.Div([
            html.H3(component_title, className="component-title"),
            html.Div(input_fields, className="model-inputs"),
            html.Button("Predict", id=f"predict-button-{{component_id}}", className="predict-button"),
            html.Div(id=f"prediction-output-{{component_id}}", className="prediction-output")
        ], className="model-prediction-component")
    
    # Default: return empty div
    return html.Div()

# Set app layout
app.layout = create_layout()

# Define callbacks
for callback_id, callback_config in dashboard_config["callbacks"].items():
    inputs = callback_config["inputs"]
    outputs = callback_config["outputs"]
    function_code = callback_config["function"]
    
    # Create callback function
    exec(f"""
@app.callback(
    [Output(output_id, 'children') for output_id in {outputs}],
    [Input(input_id, 'value') for input_id in {inputs}]
)
def {callback_id}(*args):
    {function_code}
""")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
"""
        
        return content
    
    def _generate_dash_requirements(self) -> str:
        """
        Generate Dash requirements.txt content.
        
        Returns:
            Content of requirements.txt.
        """
        return """
dash>=2.0.0
pandas>=1.3.0
numpy>=1.20.0
plotly>=5.0.0
scikit-learn>=0.24.0
openpyxl>=3.0.0
"""
    
    def _generate_dash_readme(self, dashboard_name: str) -> str:
        """
        Generate Dash README.md content.
        
        Args:
            dashboard_name: Name of the dashboard.
            
        Returns:
            Content of README.md.
        """
        return f"""
# {dashboard_name}

This is a Dash dashboard generated by SBYB UI Generator.

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Dashboard

```
python app.py
```

The dashboard will be available at http://localhost:8050

## Features

- Interactive visualizations
- Data exploration
- Model predictions
- Customizable layout

## Configuration

The dashboard is configured using the `dashboard_config.json` file. You can modify this file to customize the dashboard.
"""
    
    def _generate_dash_css(self) -> str:
        """
        Generate Dash custom.css content.
        
        Returns:
            Content of custom.css.
        """
        return """
/* Dashboard styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f8f9fa;
}

.dashboard-title {
    text-align: center;
    padding: 20px;
    background-color: #1E88E5;
    color: white;
    margin: 0;
}

/* Layout styles */
.columns-container {
    display: flex;
    flex-wrap: wrap;
}

.column {
    padding: 10px;
    box-sizing: border-box;
}

.sidebar-layout {
    display: flex;
}

.sidebar {
    width: 250px;
    padding: 10px;
    background-color: #f0f2f6;
    min-height: calc(100vh - 80px);
}

.main-content {
    flex: 1;
    padding: 10px;
}

.tab-content {
    padding: 15px;
}

/* Component styles */
.component-title {
    margin-top: 0;
    margin-bottom: 10px;
    color: #333;
}

.text-component {
    margin-bottom: 15px;
}

.header-component {
    margin-top: 10px;
    margin-bottom: 15px;
    color: #333;
}

.data-table-component {
    margin-bottom: 20px;
    background-color: white;
    padding: 15px;
    border-radius: 5px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.chart-component {
    margin-bottom: 20px;
    background-color: white;
    padding: 15px;
    border-radius: 5px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.metric-component {
    background-color: white;
    padding: 15px;
    border-radius: 5px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin-bottom: 15px;
    text-align: center;
}

.metric-title {
    font-size: 14px;
    color: #666;
}

.metric-value {
    font-size: 24px;
    font-weight: bold;
    color: #1E88E5;
}

.input-component {
    margin-bottom: 15px;
}

.input-label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
}

.button-component {
    background-color: #1E88E5;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.button-component:hover {
    background-color: #1976D2;
}

.divider-component {
    margin: 20px 0;
    border: 0;
    border-top: 1px solid #ddd;
}

.image-component {
    margin-bottom: 15px;
    text-align: center;
}

.image {
    max-width: 100%;
    height: auto;
}

.caption {
    margin-top: 5px;
    font-style: italic;
    color: #666;
}

.model-prediction-component {
    background-color: white;
    padding: 15px;
    border-radius: 5px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.model-inputs {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 15px;
}

.model-input-field {
    flex: 1;
    min-width: 150px;
}

.predict-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    margin-bottom: 10px;
}

.predict-button:hover {
    background-color: #45a049;
}

.prediction-output {
    padding: 10px;
    background-color: #f8f9fa;
    border-radius: 4px;
    min-height: 30px;
}

.error-message {
    color: #d32f2f;
    padding: 10px;
    background-color: #ffebee;
    border-radius: 4px;
    margin-bottom: 15px;
}
"""
    
    def _generate_gradio_app(self, dashboard_name: str) -> str:
        """
        Generate Gradio app.py content.
        
        Args:
            dashboard_name: Name of the dashboard.
            
        Returns:
            Content of app.py.
        """
        content = f"""
import os
import json
import pandas as pd
import numpy as np
import gradio as gr
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Load dashboard configuration
with open("dashboard_config.json", "r") as f:
    dashboard_config = json.load(f)

# Load data sources
def load_data_sources():
    data_sources = {{}}
    
    for source_id, source_config in dashboard_config["data_sources"].items():
        source_type = source_config["type"]
        config = source_config["config"]
        
        if source_type == "csv":
            data_sources[source_id] = pd.read_csv(config["path"])
        elif source_type == "excel":
            data_sources[source_id] = pd.read_excel(config["path"])
        elif source_type == "json":
            data_sources[source_id] = pd.read_json(config["path"])
        elif source_type == "pickle":
            with open(config["path"], "rb") as f:
                data_sources[source_id] = pickle.load(f)
        elif source_type == "model":
            with open(config["path"], "rb") as f:
                data_sources[source_id] = pickle.load(f)
    
    return data_sources

data_sources = load_data_sources()

# Create Gradio interface
def create_interface():
    layout_type = dashboard_config["layout"]["type"]
    layout_config = dashboard_config["layout"]["config"]
    
    with gr.Blocks(title=dashboard_config["name"]) as interface:
        gr.Markdown(f"# {dashboard_config['name']}")
        
        if layout_type == "tabs":
            with gr.Tabs():
                for tab in layout_config["tabs"]:
                    with gr.Tab(tab["title"]):
                        for component_id in tab["components"]:
                            create_component(component_id)
        
        elif layout_type == "columns":
            with gr.Row():
                for i, column in enumerate(layout_config["columns"]):
                    with gr.Column(scale=layout_config["column_widths"][i]):
                        for component_id in column["components"]:
                            create_component(component_id)
        
        elif layout_type == "sidebar":
            with gr.Row():
                with gr.Column(scale=1):
                    for component_id in layout_config["sidebar_components"]:
                        create_component(component_id)
                
                with gr.Column(scale=3):
                    for component_id in layout_config["main_components"]:
                        create_component(component_id)
        
        else:
            # Default layout: render all components sequentially
            for component in dashboard_config["components"]:
                create_component(component["id"])
    
    return interface

# Function to create a component
def create_component(component_id):
    # Find component by ID
    component = next((comp for comp in dashboard_config["components"] if comp["id"] == component_id), None)
    
    if component is None:
        gr.Markdown(f"Component with ID '{component_id}' not found.")
        return
    
    component_type = component["type"]
    component_title = component["title"]
    component_config = component["config"]
    
    # Create component based on type
    if component_type == "text":
        gr.Markdown(component_config["text"])
    
    elif component_type == "header":
        level = component_config.get("level", 2)
        gr.Markdown("#" * level + f" {{component_title}}")
    
    elif component_type == "data_table":
        data_source_id = component_config["data_source"]
        if data_source_id in data_sources:
            data = data_sources[data_source_id]
            gr.Markdown(f"### {{component_title}}")
            gr.DataFrame(data)
        else:
            gr.Markdown(f"Data source '{data_source_id}' not found.")
    
    elif component_type == "chart":
        chart_type = component_config["chart_type"]
        data_source_id = component_config["data_source"]
        
        if data_source_id not in data_sources:
            gr.Markdown(f"Data source '{data_source_id}' not found.")
            return
        
        data = data_sources[data_source_id]
        
        gr.Markdown(f"### {{component_title}}")
        
        if chart_type == "bar":
            x = component_config["x"]
            y = component_config["y"]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=data, x=x, y=y, ax=ax)
            ax.set_title(component_title)
            gr.Plot(fig)
        
        elif chart_type == "line":
            x = component_config["x"]
            y = component_config["y"]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(data=data, x=x, y=y, ax=ax)
            ax.set_title(component_title)
            gr.Plot(fig)
        
        elif chart_type == "scatter":
            x = component_config["x"]
            y = component_config["y"]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.scatterplot(data=data, x=x, y=y, ax=ax)
            ax.set_title(component_title)
            gr.Plot(fig)
        
        elif chart_type == "histogram":
            column = component_config["column"]
            bins = component_config.get("bins", 10)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=data, x=column, bins=bins, ax=ax)
            ax.set_title(component_title)
            gr.Plot(fig)
        
        elif chart_type == "boxplot":
            column = component_config["column"]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=data, y=column, ax=ax)
            ax.set_title(component_title)
            gr.Plot(fig)
        
        elif chart_type == "heatmap":
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(data.corr(), annot=True, cmap="coolwarm", ax=ax)
            ax.set_title(component_title)
            gr.Plot(fig)
    
    elif component_type == "metric":
        data_source_id = component_config["data_source"]
        metric_name = component_config["metric"]
        
        if data_source_id not in data_sources:
            gr.Markdown(f"Data source '{data_source_id}' not found.")
            return
        
        data = data_sources[data_source_id]
        
        if metric_name == "count":
            value = len(data)
        elif metric_name == "mean":
            column = component_config["column"]
            value = data[column].mean()
        elif metric_name == "sum":
            column = component_config["column"]
            value = data[column].sum()
        elif metric_name == "min":
            column = component_config["column"]
            value = data[column].min()
        elif metric_name == "max":
            column = component_config["column"]
            value = data[column].max()
        else:
            value = "Unknown metric"
        
        gr.Markdown(f"### {{component_title}}")
        gr.Number(value=value, label=metric_name)
    
    elif component_type == "input":
        input_type = component_config["input_type"]
        
        if input_type == "text":
            gr.Textbox(label=component_title)
        elif input_type == "number":
            gr.Number(label=component_title)
        elif input_type == "slider":
            min_value = component_config.get("min_value", 0)
            max_value = component_config.get("max_value", 100)
            value = component_config.get("value", min_value)
            gr.Slider(minimum=min_value, maximum=max_value, value=value, label=component_title)
        elif input_type == "select":
            options = component_config["options"]
            gr.Dropdown(choices=options, label=component_title)
        elif input_type == "multiselect":
            options = component_config["options"]
            gr.Dropdown(choices=options, multiselect=True, label=component_title)
        elif input_type == "checkbox":
            value = component_config.get("value", False)
            gr.Checkbox(value=value, label=component_title)
        elif input_type == "date":
            gr.Textbox(label=component_title, placeholder="YYYY-MM-DD")
        elif input_type == "file":
            gr.File(label=component_title)
    
    elif component_type == "button":
        gr.Button(component_title)
    
    elif component_type == "divider":
        gr.Markdown("---")
    
    elif component_type == "image":
        image_path = component_config["path"]
        caption = component_config.get("caption", "")
        
        if os.path.exists(image_path):
            gr.Image(image_path, label=caption if caption else None)
        else:
            gr.Markdown(f"Image file '{image_path}' not found.")
    
    elif component_type == "model_prediction":
        model_source_id = component_config["model_source"]
        
        if model_source_id not in data_sources:
            gr.Markdown(f"Model source '{model_source_id}' not found.")
            return
        
        model = data_sources[model_source_id]
        
        gr.Markdown(f"### {{component_title}}")
        
        # Get feature names
        if hasattr(model, "feature_names_in_"):
            feature_names = model.feature_names_in_
        else:
            feature_names = component_config.get("feature_names", [])
        
        # Create prediction function
        def predict(*feature_values):
            input_data = {{name: value for name, value in zip(feature_names, feature_values)}}
            input_df = pd.DataFrame([input_data])
            
            try:
                prediction = model.predict(input_df)
                result = f"Prediction: {{prediction[0]}}"
                
                # Add probabilities if available
                if hasattr(model, "predict_proba"):
                    probabilities = model.predict_proba(input_df)[0]
                    
                    if hasattr(model, "classes_"):
                        class_names = model.classes_
                        prob_str = ", ".join([f"{{class_names[i]}}: {{prob:.4f}}" for i, prob in enumerate(probabilities)])
                    else:
                        prob_str = ", ".join([f"Class {{i}}: {{prob:.4f}}" for i, prob in enumerate(probabilities)])
                    
                    result += f"\\nProbabilities: {{prob_str}}"
                
                return result
            except Exception as e:
                return f"Error: {{str(e)}}"
        
        # Create input components
        input_components = []
        for feature in feature_names:
            input_components.append(gr.Number(label=feature))
        
        # Create output component
        output_component = gr.Textbox(label="Prediction Result")
        
        # Create interface
        gr.Interface(
            fn=predict,
            inputs=input_components,
            outputs=output_component,
            title="",
            description="Enter feature values and click Submit to get a prediction."
        )

# Create and launch the interface
interface = create_interface()

if __name__ == "__main__":
    interface.launch()
"""
        
        return content
    
    def _generate_gradio_requirements(self) -> str:
        """
        Generate Gradio requirements.txt content.
        
        Returns:
            Content of requirements.txt.
        """
        return """
gradio>=3.0.0
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.4.0
seaborn>=0.11.0
scikit-learn>=0.24.0
openpyxl>=3.0.0
"""
    
    def _generate_gradio_readme(self, dashboard_name: str) -> str:
        """
        Generate Gradio README.md content.
        
        Args:
            dashboard_name: Name of the dashboard.
            
        Returns:
            Content of README.md.
        """
        return f"""
# {dashboard_name}

This is a Gradio dashboard generated by SBYB UI Generator.

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Dashboard

```
python app.py
```

The dashboard will be available at http://localhost:7860

## Features

- Interactive visualizations
- Data exploration
- Model predictions
- Customizable layout

## Configuration

The dashboard is configured using the `dashboard_config.json` file. You can modify this file to customize the dashboard.
"""
