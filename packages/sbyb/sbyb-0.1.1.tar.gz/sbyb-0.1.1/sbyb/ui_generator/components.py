"""
Component library for SBYB UI Generator.

This module provides a library of reusable UI components
for building dashboards and forms.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import shutil
import tempfile

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import UIGenerationError


class ComponentLibrary(SBYBComponent):
    """
    Component library for UI Generator.
    
    This component provides a library of reusable UI components
    for building dashboards and forms.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the component library.
        
        Args:
            config: Configuration dictionary for the library.
        """
        super().__init__(config)
        self.components = {}
        self.categories = {}
        self._load_default_components()
    
    def _load_default_components(self) -> None:
        """
        Load default components.
        """
        # Data visualization components
        self.add_category("data_visualization", "Data Visualization")
        
        self.register_component(
            "bar_chart",
            "Bar Chart",
            "data_visualization",
            {
                "description": "A bar chart component for visualizing categorical data.",
                "properties": {
                    "data_source": {"type": "string", "required": True},
                    "x_axis": {"type": "string", "required": True},
                    "y_axis": {"type": "string", "required": True},
                    "title": {"type": "string", "required": False},
                    "color": {"type": "string", "required": False},
                    "orientation": {"type": "string", "enum": ["vertical", "horizontal"], "default": "vertical"}
                },
                "frameworks": {
                    "streamlit": "st.bar_chart",
                    "dash": "px.bar",
                    "plotly": "go.Bar",
                    "matplotlib": "plt.bar"
                }
            }
        )
        
        self.register_component(
            "line_chart",
            "Line Chart",
            "data_visualization",
            {
                "description": "A line chart component for visualizing trends over time.",
                "properties": {
                    "data_source": {"type": "string", "required": True},
                    "x_axis": {"type": "string", "required": True},
                    "y_axis": {"type": "string", "required": True},
                    "title": {"type": "string", "required": False},
                    "color": {"type": "string", "required": False},
                    "markers": {"type": "boolean", "default": False}
                },
                "frameworks": {
                    "streamlit": "st.line_chart",
                    "dash": "px.line",
                    "plotly": "go.Scatter",
                    "matplotlib": "plt.plot"
                }
            }
        )
        
        self.register_component(
            "scatter_plot",
            "Scatter Plot",
            "data_visualization",
            {
                "description": "A scatter plot component for visualizing relationships between variables.",
                "properties": {
                    "data_source": {"type": "string", "required": True},
                    "x_axis": {"type": "string", "required": True},
                    "y_axis": {"type": "string", "required": True},
                    "title": {"type": "string", "required": False},
                    "color": {"type": "string", "required": False},
                    "size": {"type": "string", "required": False},
                    "hover_data": {"type": "array", "items": {"type": "string"}, "required": False}
                },
                "frameworks": {
                    "streamlit": "st.scatter_chart",
                    "dash": "px.scatter",
                    "plotly": "go.Scatter",
                    "matplotlib": "plt.scatter"
                }
            }
        )
        
        self.register_component(
            "pie_chart",
            "Pie Chart",
            "data_visualization",
            {
                "description": "A pie chart component for visualizing proportions.",
                "properties": {
                    "data_source": {"type": "string", "required": True},
                    "names": {"type": "string", "required": True},
                    "values": {"type": "string", "required": True},
                    "title": {"type": "string", "required": False},
                    "hole": {"type": "number", "default": 0}
                },
                "frameworks": {
                    "streamlit": "st.pyplot",
                    "dash": "px.pie",
                    "plotly": "go.Pie",
                    "matplotlib": "plt.pie"
                }
            }
        )
        
        self.register_component(
            "histogram",
            "Histogram",
            "data_visualization",
            {
                "description": "A histogram component for visualizing distributions.",
                "properties": {
                    "data_source": {"type": "string", "required": True},
                    "x": {"type": "string", "required": True},
                    "bins": {"type": "integer", "default": 10},
                    "title": {"type": "string", "required": False},
                    "color": {"type": "string", "required": False}
                },
                "frameworks": {
                    "streamlit": "st.pyplot",
                    "dash": "px.histogram",
                    "plotly": "go.Histogram",
                    "matplotlib": "plt.hist"
                }
            }
        )
        
        self.register_component(
            "heatmap",
            "Heatmap",
            "data_visualization",
            {
                "description": "A heatmap component for visualizing correlations or 2D distributions.",
                "properties": {
                    "data_source": {"type": "string", "required": True},
                    "title": {"type": "string", "required": False},
                    "color_scale": {"type": "string", "default": "viridis"},
                    "annotations": {"type": "boolean", "default": True}
                },
                "frameworks": {
                    "streamlit": "st.pyplot",
                    "dash": "px.imshow",
                    "plotly": "go.Heatmap",
                    "matplotlib": "plt.imshow"
                }
            }
        )
        
        self.register_component(
            "box_plot",
            "Box Plot",
            "data_visualization",
            {
                "description": "A box plot component for visualizing distributions and outliers.",
                "properties": {
                    "data_source": {"type": "string", "required": True},
                    "x": {"type": "string", "required": False},
                    "y": {"type": "string", "required": True},
                    "title": {"type": "string", "required": False},
                    "color": {"type": "string", "required": False},
                    "notched": {"type": "boolean", "default": False}
                },
                "frameworks": {
                    "streamlit": "st.pyplot",
                    "dash": "px.box",
                    "plotly": "go.Box",
                    "matplotlib": "plt.boxplot"
                }
            }
        )
        
        # Input components
        self.add_category("input", "Input Components")
        
        self.register_component(
            "text_input",
            "Text Input",
            "input",
            {
                "description": "A text input component for collecting string data.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "default": {"type": "string", "required": False},
                    "placeholder": {"type": "string", "required": False},
                    "help_text": {"type": "string", "required": False},
                    "required": {"type": "boolean", "default": False},
                    "max_length": {"type": "integer", "required": False}
                },
                "frameworks": {
                    "streamlit": "st.text_input",
                    "dash": "dcc.Input",
                    "html": "input[type='text']",
                    "react": "TextInput",
                    "vue": "TextInput"
                }
            }
        )
        
        self.register_component(
            "number_input",
            "Number Input",
            "input",
            {
                "description": "A number input component for collecting numeric data.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "default": {"type": "number", "required": False},
                    "min": {"type": "number", "required": False},
                    "max": {"type": "number", "required": False},
                    "step": {"type": "number", "default": 1},
                    "help_text": {"type": "string", "required": False},
                    "required": {"type": "boolean", "default": False}
                },
                "frameworks": {
                    "streamlit": "st.number_input",
                    "dash": "dcc.Input",
                    "html": "input[type='number']",
                    "react": "NumberInput",
                    "vue": "NumberInput"
                }
            }
        )
        
        self.register_component(
            "slider",
            "Slider",
            "input",
            {
                "description": "A slider component for selecting a value from a range.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "min": {"type": "number", "default": 0},
                    "max": {"type": "number", "default": 100},
                    "default": {"type": "number", "required": False},
                    "step": {"type": "number", "default": 1},
                    "help_text": {"type": "string", "required": False}
                },
                "frameworks": {
                    "streamlit": "st.slider",
                    "dash": "dcc.Slider",
                    "html": "input[type='range']",
                    "react": "Slider",
                    "vue": "Slider"
                }
            }
        )
        
        self.register_component(
            "select",
            "Select",
            "input",
            {
                "description": "A select component for choosing from a list of options.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "options": {"type": "array", "items": {"type": "string"}, "required": True},
                    "default": {"type": "string", "required": False},
                    "help_text": {"type": "string", "required": False},
                    "required": {"type": "boolean", "default": False}
                },
                "frameworks": {
                    "streamlit": "st.selectbox",
                    "dash": "dcc.Dropdown",
                    "html": "select",
                    "react": "Select",
                    "vue": "Select"
                }
            }
        )
        
        self.register_component(
            "multiselect",
            "Multi-Select",
            "input",
            {
                "description": "A multi-select component for choosing multiple options from a list.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "options": {"type": "array", "items": {"type": "string"}, "required": True},
                    "default": {"type": "array", "items": {"type": "string"}, "required": False},
                    "help_text": {"type": "string", "required": False}
                },
                "frameworks": {
                    "streamlit": "st.multiselect",
                    "dash": "dcc.Dropdown",
                    "html": "select[multiple]",
                    "react": "MultiSelect",
                    "vue": "MultiSelect"
                }
            }
        )
        
        self.register_component(
            "checkbox",
            "Checkbox",
            "input",
            {
                "description": "A checkbox component for boolean input.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "default": {"type": "boolean", "default": False},
                    "help_text": {"type": "string", "required": False}
                },
                "frameworks": {
                    "streamlit": "st.checkbox",
                    "dash": "dcc.Checklist",
                    "html": "input[type='checkbox']",
                    "react": "Checkbox",
                    "vue": "Checkbox"
                }
            }
        )
        
        self.register_component(
            "radio",
            "Radio Buttons",
            "input",
            {
                "description": "A radio button component for selecting one option from a list.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "options": {"type": "array", "items": {"type": "string"}, "required": True},
                    "default": {"type": "string", "required": False},
                    "help_text": {"type": "string", "required": False},
                    "required": {"type": "boolean", "default": False}
                },
                "frameworks": {
                    "streamlit": "st.radio",
                    "dash": "dcc.RadioItems",
                    "html": "input[type='radio']",
                    "react": "RadioGroup",
                    "vue": "RadioGroup"
                }
            }
        )
        
        self.register_component(
            "date_input",
            "Date Input",
            "input",
            {
                "description": "A date input component for selecting dates.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "default": {"type": "string", "required": False},
                    "min": {"type": "string", "required": False},
                    "max": {"type": "string", "required": False},
                    "help_text": {"type": "string", "required": False},
                    "required": {"type": "boolean", "default": False}
                },
                "frameworks": {
                    "streamlit": "st.date_input",
                    "dash": "dcc.DatePickerSingle",
                    "html": "input[type='date']",
                    "react": "DatePicker",
                    "vue": "DatePicker"
                }
            }
        )
        
        self.register_component(
            "file_upload",
            "File Upload",
            "input",
            {
                "description": "A file upload component for uploading files.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "accept": {"type": "string", "required": False},
                    "multiple": {"type": "boolean", "default": False},
                    "help_text": {"type": "string", "required": False}
                },
                "frameworks": {
                    "streamlit": "st.file_uploader",
                    "dash": "dcc.Upload",
                    "html": "input[type='file']",
                    "react": "FileUpload",
                    "vue": "FileUpload"
                }
            }
        )
        
        # Layout components
        self.add_category("layout", "Layout Components")
        
        self.register_component(
            "tabs",
            "Tabs",
            "layout",
            {
                "description": "A tabs component for organizing content into tabs.",
                "properties": {
                    "tabs": {"type": "array", "items": {"type": "object"}, "required": True}
                },
                "frameworks": {
                    "streamlit": "st.tabs",
                    "dash": "dcc.Tabs",
                    "html": "div.tabs",
                    "react": "Tabs",
                    "vue": "Tabs"
                }
            }
        )
        
        self.register_component(
            "columns",
            "Columns",
            "layout",
            {
                "description": "A columns component for creating multi-column layouts.",
                "properties": {
                    "columns": {"type": "array", "items": {"type": "object"}, "required": True},
                    "widths": {"type": "array", "items": {"type": "number"}, "required": False}
                },
                "frameworks": {
                    "streamlit": "st.columns",
                    "dash": "html.Div",
                    "html": "div.columns",
                    "react": "Grid",
                    "vue": "Grid"
                }
            }
        )
        
        self.register_component(
            "expander",
            "Expander",
            "layout",
            {
                "description": "An expander component for collapsible content.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "expanded": {"type": "boolean", "default": False}
                },
                "frameworks": {
                    "streamlit": "st.expander",
                    "dash": "html.Details",
                    "html": "details",
                    "react": "Accordion",
                    "vue": "Accordion"
                }
            }
        )
        
        self.register_component(
            "container",
            "Container",
            "layout",
            {
                "description": "A container component for grouping content.",
                "properties": {
                    "border": {"type": "boolean", "default": False},
                    "padding": {"type": "string", "default": "1rem"},
                    "background_color": {"type": "string", "required": False}
                },
                "frameworks": {
                    "streamlit": "st.container",
                    "dash": "html.Div",
                    "html": "div.container",
                    "react": "Container",
                    "vue": "Container"
                }
            }
        )
        
        self.register_component(
            "divider",
            "Divider",
            "layout",
            {
                "description": "A divider component for separating content.",
                "properties": {
                    "style": {"type": "string", "enum": ["solid", "dashed", "dotted"], "default": "solid"},
                    "color": {"type": "string", "required": False},
                    "thickness": {"type": "number", "default": 1}
                },
                "frameworks": {
                    "streamlit": "st.divider",
                    "dash": "html.Hr",
                    "html": "hr",
                    "react": "Divider",
                    "vue": "Divider"
                }
            }
        )
        
        # Display components
        self.add_category("display", "Display Components")
        
        self.register_component(
            "text",
            "Text",
            "display",
            {
                "description": "A text component for displaying text.",
                "properties": {
                    "text": {"type": "string", "required": True},
                    "size": {"type": "string", "enum": ["small", "medium", "large"], "default": "medium"},
                    "color": {"type": "string", "required": False},
                    "align": {"type": "string", "enum": ["left", "center", "right"], "default": "left"}
                },
                "frameworks": {
                    "streamlit": "st.text",
                    "dash": "html.P",
                    "html": "p",
                    "react": "Text",
                    "vue": "Text"
                }
            }
        )
        
        self.register_component(
            "header",
            "Header",
            "display",
            {
                "description": "A header component for displaying headings.",
                "properties": {
                    "text": {"type": "string", "required": True},
                    "level": {"type": "integer", "enum": [1, 2, 3, 4, 5, 6], "default": 2},
                    "color": {"type": "string", "required": False},
                    "align": {"type": "string", "enum": ["left", "center", "right"], "default": "left"}
                },
                "frameworks": {
                    "streamlit": "st.header",
                    "dash": "html.H2",
                    "html": "h2",
                    "react": "Heading",
                    "vue": "Heading"
                }
            }
        )
        
        self.register_component(
            "image",
            "Image",
            "display",
            {
                "description": "An image component for displaying images.",
                "properties": {
                    "src": {"type": "string", "required": True},
                    "alt": {"type": "string", "required": False},
                    "width": {"type": "string", "required": False},
                    "height": {"type": "string", "required": False},
                    "caption": {"type": "string", "required": False}
                },
                "frameworks": {
                    "streamlit": "st.image",
                    "dash": "html.Img",
                    "html": "img",
                    "react": "Image",
                    "vue": "Image"
                }
            }
        )
        
        self.register_component(
            "data_table",
            "Data Table",
            "display",
            {
                "description": "A data table component for displaying tabular data.",
                "properties": {
                    "data_source": {"type": "string", "required": True},
                    "columns": {"type": "array", "items": {"type": "string"}, "required": False},
                    "pagination": {"type": "boolean", "default": True},
                    "page_size": {"type": "integer", "default": 10},
                    "sortable": {"type": "boolean", "default": True},
                    "filterable": {"type": "boolean", "default": False}
                },
                "frameworks": {
                    "streamlit": "st.dataframe",
                    "dash": "dash_table.DataTable",
                    "html": "table",
                    "react": "DataTable",
                    "vue": "DataTable"
                }
            }
        )
        
        self.register_component(
            "metric",
            "Metric",
            "display",
            {
                "description": "A metric component for displaying key metrics.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "value": {"type": "string", "required": True},
                    "delta": {"type": "string", "required": False},
                    "color": {"type": "string", "required": False}
                },
                "frameworks": {
                    "streamlit": "st.metric",
                    "dash": "html.Div",
                    "html": "div.metric",
                    "react": "Metric",
                    "vue": "Metric"
                }
            }
        )
        
        self.register_component(
            "code",
            "Code",
            "display",
            {
                "description": "A code component for displaying code snippets.",
                "properties": {
                    "code": {"type": "string", "required": True},
                    "language": {"type": "string", "default": "python"},
                    "line_numbers": {"type": "boolean", "default": False}
                },
                "frameworks": {
                    "streamlit": "st.code",
                    "dash": "dcc.Markdown",
                    "html": "pre code",
                    "react": "CodeBlock",
                    "vue": "CodeBlock"
                }
            }
        )
        
        self.register_component(
            "markdown",
            "Markdown",
            "display",
            {
                "description": "A markdown component for displaying formatted text.",
                "properties": {
                    "content": {"type": "string", "required": True}
                },
                "frameworks": {
                    "streamlit": "st.markdown",
                    "dash": "dcc.Markdown",
                    "html": "div.markdown",
                    "react": "Markdown",
                    "vue": "Markdown"
                }
            }
        )
        
        # Interactive components
        self.add_category("interactive", "Interactive Components")
        
        self.register_component(
            "button",
            "Button",
            "interactive",
            {
                "description": "A button component for triggering actions.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "type": {"type": "string", "enum": ["primary", "secondary", "danger"], "default": "primary"},
                    "disabled": {"type": "boolean", "default": False},
                    "icon": {"type": "string", "required": False}
                },
                "frameworks": {
                    "streamlit": "st.button",
                    "dash": "html.Button",
                    "html": "button",
                    "react": "Button",
                    "vue": "Button"
                }
            }
        )
        
        self.register_component(
            "download_button",
            "Download Button",
            "interactive",
            {
                "description": "A download button component for downloading files.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "data": {"type": "string", "required": True},
                    "file_name": {"type": "string", "required": True},
                    "mime_type": {"type": "string", "required": False}
                },
                "frameworks": {
                    "streamlit": "st.download_button",
                    "dash": "html.A",
                    "html": "a[download]",
                    "react": "DownloadButton",
                    "vue": "DownloadButton"
                }
            }
        )
        
        self.register_component(
            "toggle",
            "Toggle",
            "interactive",
            {
                "description": "A toggle component for switching between two states.",
                "properties": {
                    "label": {"type": "string", "required": True},
                    "default": {"type": "boolean", "default": False},
                    "disabled": {"type": "boolean", "default": False}
                },
                "frameworks": {
                    "streamlit": "st.toggle",
                    "dash": "dcc.Checklist",
                    "html": "label.toggle",
                    "react": "Toggle",
                    "vue": "Toggle"
                }
            }
        )
        
        # ML-specific components
        self.add_category("ml", "Machine Learning Components")
        
        self.register_component(
            "model_prediction",
            "Model Prediction",
            "ml",
            {
                "description": "A component for making predictions with a machine learning model.",
                "properties": {
                    "model_source": {"type": "string", "required": True},
                    "feature_names": {"type": "array", "items": {"type": "string"}, "required": False},
                    "show_probabilities": {"type": "boolean", "default": True}
                },
                "frameworks": {
                    "streamlit": "custom",
                    "dash": "custom",
                    "html": "custom",
                    "react": "custom",
                    "vue": "custom"
                }
            }
        )
        
        self.register_component(
            "feature_importance",
            "Feature Importance",
            "ml",
            {
                "description": "A component for displaying feature importance of a machine learning model.",
                "properties": {
                    "model_source": {"type": "string", "required": True},
                    "top_n": {"type": "integer", "default": 10},
                    "orientation": {"type": "string", "enum": ["vertical", "horizontal"], "default": "horizontal"}
                },
                "frameworks": {
                    "streamlit": "custom",
                    "dash": "custom",
                    "html": "custom",
                    "react": "custom",
                    "vue": "custom"
                }
            }
        )
        
        self.register_component(
            "confusion_matrix",
            "Confusion Matrix",
            "ml",
            {
                "description": "A component for displaying a confusion matrix for classification models.",
                "properties": {
                    "data_source": {"type": "string", "required": True},
                    "true_labels": {"type": "string", "required": True},
                    "predicted_labels": {"type": "string", "required": True},
                    "normalize": {"type": "boolean", "default": False},
                    "color_map": {"type": "string", "default": "Blues"}
                },
                "frameworks": {
                    "streamlit": "custom",
                    "dash": "custom",
                    "html": "custom",
                    "react": "custom",
                    "vue": "custom"
                }
            }
        )
        
        self.register_component(
            "roc_curve",
            "ROC Curve",
            "ml",
            {
                "description": "A component for displaying a ROC curve for binary classification models.",
                "properties": {
                    "data_source": {"type": "string", "required": True},
                    "true_labels": {"type": "string", "required": True},
                    "predicted_probs": {"type": "string", "required": True},
                    "show_auc": {"type": "boolean", "default": True}
                },
                "frameworks": {
                    "streamlit": "custom",
                    "dash": "custom",
                    "html": "custom",
                    "react": "custom",
                    "vue": "custom"
                }
            }
        )
        
        self.register_component(
            "precision_recall_curve",
            "Precision-Recall Curve",
            "ml",
            {
                "description": "A component for displaying a precision-recall curve for binary classification models.",
                "properties": {
                    "data_source": {"type": "string", "required": True},
                    "true_labels": {"type": "string", "required": True},
                    "predicted_probs": {"type": "string", "required": True},
                    "show_auc": {"type": "boolean", "default": True}
                },
                "frameworks": {
                    "streamlit": "custom",
                    "dash": "custom",
                    "html": "custom",
                    "react": "custom",
                    "vue": "custom"
                }
            }
        )
        
        self.register_component(
            "residual_plot",
            "Residual Plot",
            "ml",
            {
                "description": "A component for displaying residuals of a regression model.",
                "properties": {
                    "data_source": {"type": "string", "required": True},
                    "true_values": {"type": "string", "required": True},
                    "predicted_values": {"type": "string", "required": True}
                },
                "frameworks": {
                    "streamlit": "custom",
                    "dash": "custom",
                    "html": "custom",
                    "react": "custom",
                    "vue": "custom"
                }
            }
        )
    
    def add_category(self, category_id: str, category_name: str) -> None:
        """
        Add a component category.
        
        Args:
            category_id: Unique identifier for the category.
            category_name: Display name for the category.
        """
        if category_id in self.categories:
            raise UIGenerationError(f"Category ID '{category_id}' already exists.")
        
        self.categories[category_id] = {
            "name": category_name,
            "components": []
        }
    
    def register_component(self, component_id: str, component_name: str,
                          category_id: str, config: Dict[str, Any]) -> None:
        """
        Register a component in the library.
        
        Args:
            component_id: Unique identifier for the component.
            component_name: Display name for the component.
            category_id: Category to which the component belongs.
            config: Configuration for the component.
        """
        if component_id in self.components:
            raise UIGenerationError(f"Component ID '{component_id}' already exists.")
        
        if category_id not in self.categories:
            raise UIGenerationError(f"Category ID '{category_id}' does not exist.")
        
        component = {
            "id": component_id,
            "name": component_name,
            "category": category_id,
            "config": config
        }
        
        self.components[component_id] = component
        self.categories[category_id]["components"].append(component_id)
    
    def get_component(self, component_id: str) -> Dict[str, Any]:
        """
        Get a component by ID.
        
        Args:
            component_id: ID of the component to get.
            
        Returns:
            Component configuration.
        """
        if component_id not in self.components:
            raise UIGenerationError(f"Component ID '{component_id}' does not exist.")
        
        return self.components[component_id]
    
    def get_components_by_category(self, category_id: str) -> List[Dict[str, Any]]:
        """
        Get all components in a category.
        
        Args:
            category_id: ID of the category.
            
        Returns:
            List of components in the category.
        """
        if category_id not in self.categories:
            raise UIGenerationError(f"Category ID '{category_id}' does not exist.")
        
        return [self.components[component_id] for component_id in self.categories[category_id]["components"]]
    
    def get_all_components(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all components.
        
        Returns:
            Dictionary of all components.
        """
        return self.components
    
    def get_all_categories(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all categories.
        
        Returns:
            Dictionary of all categories.
        """
        return self.categories
    
    def get_component_code(self, component_id: str, framework: str,
                          props: Dict[str, Any]) -> str:
        """
        Get the code for a component in a specific framework.
        
        Args:
            component_id: ID of the component.
            framework: Framework to generate code for.
            props: Properties for the component.
            
        Returns:
            Code for the component.
        """
        component = self.get_component(component_id)
        
        if framework not in component["config"]["frameworks"]:
            raise UIGenerationError(f"Framework '{framework}' not supported for component '{component_id}'.")
        
        # Validate required properties
        for prop_name, prop_config in component["config"]["properties"].items():
            if prop_config.get("required", False) and prop_name not in props:
                raise UIGenerationError(f"Required property '{prop_name}' missing for component '{component_id}'.")
        
        # Generate code based on framework
        if framework == "streamlit":
            return self._generate_streamlit_code(component, props)
        elif framework == "dash":
            return self._generate_dash_code(component, props)
        elif framework == "html":
            return self._generate_html_code(component, props)
        elif framework == "react":
            return self._generate_react_code(component, props)
        elif framework == "vue":
            return self._generate_vue_code(component, props)
        else:
            raise UIGenerationError(f"Unsupported framework: {framework}")
    
    def _generate_streamlit_code(self, component: Dict[str, Any], props: Dict[str, Any]) -> str:
        """
        Generate Streamlit code for a component.
        
        Args:
            component: Component configuration.
            props: Properties for the component.
            
        Returns:
            Streamlit code for the component.
        """
        component_type = component["id"]
        framework_func = component["config"]["frameworks"]["streamlit"]
        
        # Handle custom components
        if framework_func == "custom":
            if component_type == "model_prediction":
                return self._generate_streamlit_model_prediction(props)
            elif component_type == "feature_importance":
                return self._generate_streamlit_feature_importance(props)
            elif component_type == "confusion_matrix":
                return self._generate_streamlit_confusion_matrix(props)
            elif component_type == "roc_curve":
                return self._generate_streamlit_roc_curve(props)
            elif component_type == "precision_recall_curve":
                return self._generate_streamlit_precision_recall_curve(props)
            elif component_type == "residual_plot":
                return self._generate_streamlit_residual_plot(props)
            else:
                raise UIGenerationError(f"Custom component '{component_type}' not implemented for Streamlit.")
        
        # Generate code for standard components
        props_str = ", ".join([f"{k}={repr(v)}" for k, v in props.items()])
        return f"{framework_func}({props_str})"
    
    def _generate_dash_code(self, component: Dict[str, Any], props: Dict[str, Any]) -> str:
        """
        Generate Dash code for a component.
        
        Args:
            component: Component configuration.
            props: Properties for the component.
            
        Returns:
            Dash code for the component.
        """
        component_type = component["id"]
        framework_func = component["config"]["frameworks"]["dash"]
        
        # Handle custom components
        if framework_func == "custom":
            if component_type == "model_prediction":
                return self._generate_dash_model_prediction(props)
            elif component_type == "feature_importance":
                return self._generate_dash_feature_importance(props)
            elif component_type == "confusion_matrix":
                return self._generate_dash_confusion_matrix(props)
            elif component_type == "roc_curve":
                return self._generate_dash_roc_curve(props)
            elif component_type == "precision_recall_curve":
                return self._generate_dash_precision_recall_curve(props)
            elif component_type == "residual_plot":
                return self._generate_dash_residual_plot(props)
            else:
                raise UIGenerationError(f"Custom component '{component_type}' not implemented for Dash.")
        
        # Generate code for standard components
        props_str = ", ".join([f"{k}={repr(v)}" for k, v in props.items()])
        return f"{framework_func}({props_str})"
    
    def _generate_html_code(self, component: Dict[str, Any], props: Dict[str, Any]) -> str:
        """
        Generate HTML code for a component.
        
        Args:
            component: Component configuration.
            props: Properties for the component.
            
        Returns:
            HTML code for the component.
        """
        component_type = component["id"]
        framework_element = component["config"]["frameworks"]["html"]
        
        # Handle custom components
        if framework_element == "custom":
            if component_type == "model_prediction":
                return self._generate_html_model_prediction(props)
            elif component_type == "feature_importance":
                return self._generate_html_feature_importance(props)
            elif component_type == "confusion_matrix":
                return self._generate_html_confusion_matrix(props)
            elif component_type == "roc_curve":
                return self._generate_html_roc_curve(props)
            elif component_type == "precision_recall_curve":
                return self._generate_html_precision_recall_curve(props)
            elif component_type == "residual_plot":
                return self._generate_html_residual_plot(props)
            else:
                raise UIGenerationError(f"Custom component '{component_type}' not implemented for HTML.")
        
        # Parse element and class
        element_parts = framework_element.split(".")
        element_tag = element_parts[0]
        element_class = element_parts[1] if len(element_parts) > 1 else None
        
        # Generate attributes string
        attributes = []
        for k, v in props.items():
            if k == "text" or k == "content":
                continue
            
            if isinstance(v, bool):
                if v:
                    attributes.append(k)
            else:
                attributes.append(f'{k}="{v}"')
        
        if element_class:
            attributes.append(f'class="{element_class}"')
        
        attributes_str = " ".join(attributes)
        
        # Generate content
        content = ""
        if "text" in props:
            content = props["text"]
        elif "content" in props:
            content = props["content"]
        
        # Generate HTML
        if content:
            return f"<{element_tag} {attributes_str}>{content}</{element_tag}>"
        else:
            return f"<{element_tag} {attributes_str} />"
    
    def _generate_react_code(self, component: Dict[str, Any], props: Dict[str, Any]) -> str:
        """
        Generate React code for a component.
        
        Args:
            component: Component configuration.
            props: Properties for the component.
            
        Returns:
            React code for the component.
        """
        component_type = component["id"]
        framework_component = component["config"]["frameworks"]["react"]
        
        # Handle custom components
        if framework_component == "custom":
            if component_type == "model_prediction":
                return self._generate_react_model_prediction(props)
            elif component_type == "feature_importance":
                return self._generate_react_feature_importance(props)
            elif component_type == "confusion_matrix":
                return self._generate_react_confusion_matrix(props)
            elif component_type == "roc_curve":
                return self._generate_react_roc_curve(props)
            elif component_type == "precision_recall_curve":
                return self._generate_react_precision_recall_curve(props)
            elif component_type == "residual_plot":
                return self._generate_react_residual_plot(props)
            else:
                raise UIGenerationError(f"Custom component '{component_type}' not implemented for React.")
        
        # Generate props string
        props_parts = []
        for k, v in props.items():
            if isinstance(v, bool):
                if v:
                    props_parts.append(f"{k}")
                else:
                    props_parts.append(f"{k}={{{v}}}")
            elif isinstance(v, (int, float)):
                props_parts.append(f"{k}={{{v}}}")
            elif isinstance(v, str):
                props_parts.append(f'{k}="{v}"')
            else:
                props_parts.append(f"{k}={{{repr(v)}}}")
        
        props_str = " ".join(props_parts)
        
        # Generate React component
        return f"<{framework_component} {props_str} />"
    
    def _generate_vue_code(self, component: Dict[str, Any], props: Dict[str, Any]) -> str:
        """
        Generate Vue code for a component.
        
        Args:
            component: Component configuration.
            props: Properties for the component.
            
        Returns:
            Vue code for the component.
        """
        component_type = component["id"]
        framework_component = component["config"]["frameworks"]["vue"]
        
        # Handle custom components
        if framework_component == "custom":
            if component_type == "model_prediction":
                return self._generate_vue_model_prediction(props)
            elif component_type == "feature_importance":
                return self._generate_vue_feature_importance(props)
            elif component_type == "confusion_matrix":
                return self._generate_vue_confusion_matrix(props)
            elif component_type == "roc_curve":
                return self._generate_vue_roc_curve(props)
            elif component_type == "precision_recall_curve":
                return self._generate_vue_precision_recall_curve(props)
            elif component_type == "residual_plot":
                return self._generate_vue_residual_plot(props)
            else:
                raise UIGenerationError(f"Custom component '{component_type}' not implemented for Vue.")
        
        # Generate props string
        props_parts = []
        for k, v in props.items():
            if isinstance(v, bool):
                if v:
                    props_parts.append(f"{k}")
                else:
                    props_parts.append(f":{k}=\"{str(v).lower()}\"")
            elif isinstance(v, (int, float)):
                props_parts.append(f":{k}=\"{v}\"")
            elif isinstance(v, str):
                props_parts.append(f'{k}="{v}"')
            else:
                props_parts.append(f":{k}=\"{repr(v)}\"")
        
        props_str = " ".join(props_parts)
        
        # Generate Vue component
        return f"<{framework_component} {props_str} />"
    
    # Custom component generators for Streamlit
    def _generate_streamlit_model_prediction(self, props: Dict[str, Any]) -> str:
        """
        Generate Streamlit code for model prediction component.
        
        Args:
            props: Properties for the component.
            
        Returns:
            Streamlit code for the component.
        """
        model_source = props["model_source"]
        feature_names = props.get("feature_names", [])
        show_probabilities = props.get("show_probabilities", True)
        
        code = f"""
# Model Prediction Component
st.subheader("Model Prediction")

# Get model
model = data_sources["{model_source}"]

# Create input fields
input_values = {{}}
"""
        
        if feature_names:
            code += """
# Use provided feature names
feature_names = {feature_names}
""".format(feature_names=repr(feature_names))
        else:
            code += """
# Try to get feature names from model
if hasattr(model, "feature_names_in_"):
    feature_names = model.feature_names_in_
else:
    st.error("No feature names provided and model does not have feature_names_in_ attribute.")
    feature_names = []
"""
        
        code += """
# Create input fields for each feature
for feature in feature_names:
    input_values[feature] = st.number_input(f"{feature}")

# Add prediction button
if st.button("Predict"):
    try:
        # Create input DataFrame
        input_df = pd.DataFrame([input_values])
        
        # Make prediction
        prediction = model.predict(input_df)
        
        st.success(f"Prediction: {prediction[0]}")
"""
        
        if show_probabilities:
            code += """        
        # Show probability if available
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)
            st.write("Prediction probabilities:")
            
            # Get class names if available
            if hasattr(model, "classes_"):
                class_names = model.classes_
                prob_df = pd.DataFrame([probabilities[0]], columns=class_names)
            else:
                prob_df = pd.DataFrame([probabilities[0]], columns=[f"Class {i}" for i in range(probabilities.shape[1])])
            
            st.dataframe(prob_df)
"""
        
        code += """
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
"""
        
        return code
    
    def _generate_streamlit_feature_importance(self, props: Dict[str, Any]) -> str:
        """
        Generate Streamlit code for feature importance component.
        
        Args:
            props: Properties for the component.
            
        Returns:
            Streamlit code for the component.
        """
        model_source = props["model_source"]
        top_n = props.get("top_n", 10)
        orientation = props.get("orientation", "horizontal")
        
        code = f"""
# Feature Importance Component
st.subheader("Feature Importance")

# Get model
model = data_sources["{model_source}"]

try:
    # Get feature importance
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_[0]) if len(model.coef_.shape) > 1 else np.abs(model.coef_)
    else:
        st.error("Model does not have feature_importances_ or coef_ attribute.")
        importances = []
    
    # Get feature names
    if hasattr(model, "feature_names_in_"):
        feature_names = model.feature_names_in_
    else:
        feature_names = [f"Feature {{i}}" for i in range(len(importances))]
    
    # Create DataFrame
    importance_df = pd.DataFrame({{"Feature": feature_names, "Importance": importances}})
    importance_df = importance_df.sort_values("Importance", ascending=False).head({top_n})
    
    # Plot feature importance
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if "{orientation}" == "horizontal":
        sns.barplot(x="Importance", y="Feature", data=importance_df, ax=ax)
        ax.set_xlabel("Importance")
        ax.set_ylabel("Feature")
    else:
        sns.barplot(x="Feature", y="Importance", data=importance_df, ax=ax)
        ax.set_xlabel("Feature")
        ax.set_ylabel("Importance")
        plt.xticks(rotation=45, ha="right")
    
    ax.set_title("Feature Importance")
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # Show importance table
    st.dataframe(importance_df)
except Exception as e:
    st.error(f"Error displaying feature importance: {{str(e)}}")
"""
        
        return code
    
    def _generate_streamlit_confusion_matrix(self, props: Dict[str, Any]) -> str:
        """
        Generate Streamlit code for confusion matrix component.
        
        Args:
            props: Properties for the component.
            
        Returns:
            Streamlit code for the component.
        """
        data_source = props["data_source"]
        true_labels = props["true_labels"]
        predicted_labels = props["predicted_labels"]
        normalize = props.get("normalize", False)
        color_map = props.get("color_map", "Blues")
        
        code = f"""
# Confusion Matrix Component
st.subheader("Confusion Matrix")

# Get data
data = data_sources["{data_source}"]
y_true = data["{true_labels}"]
y_pred = data["{predicted_labels}"]

try:
    from sklearn.metrics import confusion_matrix
    import seaborn as sns
    
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Normalize if requested
    if {normalize}:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    # Get class names if available
    if hasattr(data, "classes_"):
        class_names = data.classes_
    else:
        class_names = sorted(set(y_true) | set(y_pred))
    
    # Plot confusion matrix
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='.2f' if {normalize} else 'd', cmap='{color_map}',
                xticklabels=class_names, yticklabels=class_names, ax=ax)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('True')
    ax.set_title('Confusion Matrix')
    plt.tight_layout()
    
    st.pyplot(fig)
except Exception as e:
    st.error(f"Error displaying confusion matrix: {{str(e)}}")
"""
        
        return code
    
    def _generate_streamlit_roc_curve(self, props: Dict[str, Any]) -> str:
        """
        Generate Streamlit code for ROC curve component.
        
        Args:
            props: Properties for the component.
            
        Returns:
            Streamlit code for the component.
        """
        data_source = props["data_source"]
        true_labels = props["true_labels"]
        predicted_probs = props["predicted_probs"]
        show_auc = props.get("show_auc", True)
        
        code = f"""
# ROC Curve Component
st.subheader("ROC Curve")

# Get data
data = data_sources["{data_source}"]
y_true = data["{true_labels}"]
y_score = data["{predicted_probs}"]

try:
    from sklearn.metrics import roc_curve, auc
    
    # Compute ROC curve and ROC area
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    
    # Plot ROC curve
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(fpr, tpr, label=f'ROC curve (area = {{roc_auc:.2f}})' if {show_auc} else 'ROC curve')
    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('Receiver Operating Characteristic (ROC)')
    ax.legend(loc="lower right")
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # Show AUC value
    if {show_auc}:
        st.metric("Area Under the Curve (AUC)", f"{{roc_auc:.4f}}")
except Exception as e:
    st.error(f"Error displaying ROC curve: {{str(e)}}")
"""
        
        return code
    
    def _generate_streamlit_precision_recall_curve(self, props: Dict[str, Any]) -> str:
        """
        Generate Streamlit code for precision-recall curve component.
        
        Args:
            props: Properties for the component.
            
        Returns:
            Streamlit code for the component.
        """
        data_source = props["data_source"]
        true_labels = props["true_labels"]
        predicted_probs = props["predicted_probs"]
        show_auc = props.get("show_auc", True)
        
        code = f"""
# Precision-Recall Curve Component
st.subheader("Precision-Recall Curve")

# Get data
data = data_sources["{data_source}"]
y_true = data["{true_labels}"]
y_score = data["{predicted_probs}"]

try:
    from sklearn.metrics import precision_recall_curve, average_precision_score
    
    # Compute Precision-Recall curve and average precision
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)
    
    # Plot Precision-Recall curve
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(recall, precision, label=f'Precision-Recall curve (AP = {{ap:.2f}})' if {show_auc} else 'Precision-Recall curve')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.set_title('Precision-Recall Curve')
    ax.legend(loc="lower left")
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # Show AP value
    if {show_auc}:
        st.metric("Average Precision (AP)", f"{{ap:.4f}}")
except Exception as e:
    st.error(f"Error displaying Precision-Recall curve: {{str(e)}}")
"""
        
        return code
    
    def _generate_streamlit_residual_plot(self, props: Dict[str, Any]) -> str:
        """
        Generate Streamlit code for residual plot component.
        
        Args:
            props: Properties for the component.
            
        Returns:
            Streamlit code for the component.
        """
        data_source = props["data_source"]
        true_values = props["true_values"]
        predicted_values = props["predicted_values"]
        
        code = f"""
# Residual Plot Component
st.subheader("Residual Plot")

# Get data
data = data_sources["{data_source}"]
y_true = data["{true_values}"]
y_pred = data["{predicted_values}"]

try:
    # Compute residuals
    residuals = y_true - y_pred
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot residuals vs predicted values
    ax1.scatter(y_pred, residuals)
    ax1.axhline(y=0, color='r', linestyle='-')
    ax1.set_xlabel('Predicted Values')
    ax1.set_ylabel('Residuals')
    ax1.set_title('Residuals vs Predicted Values')
    
    # Plot histogram of residuals
    ax2.hist(residuals, bins=20, edgecolor='black')
    ax2.axvline(x=0, color='r', linestyle='-')
    ax2.set_xlabel('Residuals')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Histogram of Residuals')
    
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # Show residual statistics
    st.write("Residual Statistics:")
    stats_df = pd.DataFrame({{
        "Statistic": ["Mean", "Std Dev", "Min", "25%", "Median", "75%", "Max"],
        "Value": [
            residuals.mean(),
            residuals.std(),
            residuals.min(),
            np.percentile(residuals, 25),
            np.median(residuals),
            np.percentile(residuals, 75),
            residuals.max()
        ]
    }})
    st.dataframe(stats_df)
except Exception as e:
    st.error(f"Error displaying residual plot: {{str(e)}}")
"""
        
        return code
    
    # Custom component generators for other frameworks would be implemented similarly
    def _generate_dash_model_prediction(self, props: Dict[str, Any]) -> str:
        """Placeholder for Dash model prediction component"""
        return "# Dash model prediction component (implementation details omitted for brevity)"
    
    def _generate_dash_feature_importance(self, props: Dict[str, Any]) -> str:
        """Placeholder for Dash feature importance component"""
        return "# Dash feature importance component (implementation details omitted for brevity)"
    
    def _generate_dash_confusion_matrix(self, props: Dict[str, Any]) -> str:
        """Placeholder for Dash confusion matrix component"""
        return "# Dash confusion matrix component (implementation details omitted for brevity)"
    
    def _generate_dash_roc_curve(self, props: Dict[str, Any]) -> str:
        """Placeholder for Dash ROC curve component"""
        return "# Dash ROC curve component (implementation details omitted for brevity)"
    
    def _generate_dash_precision_recall_curve(self, props: Dict[str, Any]) -> str:
        """Placeholder for Dash precision-recall curve component"""
        return "# Dash precision-recall curve component (implementation details omitted for brevity)"
    
    def _generate_dash_residual_plot(self, props: Dict[str, Any]) -> str:
        """Placeholder for Dash residual plot component"""
        return "# Dash residual plot component (implementation details omitted for brevity)"
    
    def _generate_html_model_prediction(self, props: Dict[str, Any]) -> str:
        """Placeholder for HTML model prediction component"""
        return "<!-- HTML model prediction component (implementation details omitted for brevity) -->"
    
    def _generate_html_feature_importance(self, props: Dict[str, Any]) -> str:
        """Placeholder for HTML feature importance component"""
        return "<!-- HTML feature importance component (implementation details omitted for brevity) -->"
    
    def _generate_html_confusion_matrix(self, props: Dict[str, Any]) -> str:
        """Placeholder for HTML confusion matrix component"""
        return "<!-- HTML confusion matrix component (implementation details omitted for brevity) -->"
    
    def _generate_html_roc_curve(self, props: Dict[str, Any]) -> str:
        """Placeholder for HTML ROC curve component"""
        return "<!-- HTML ROC curve component (implementation details omitted for brevity) -->"
    
    def _generate_html_precision_recall_curve(self, props: Dict[str, Any]) -> str:
        """Placeholder for HTML precision-recall curve component"""
        return "<!-- HTML precision-recall curve component (implementation details omitted for brevity) -->"
    
    def _generate_html_residual_plot(self, props: Dict[str, Any]) -> str:
        """Placeholder for HTML residual plot component"""
        return "<!-- HTML residual plot component (implementation details omitted for brevity) -->"
    
    def _generate_react_model_prediction(self, props: Dict[str, Any]) -> str:
        """Placeholder for React model prediction component"""
        return "// React model prediction component (implementation details omitted for brevity)"
    
    def _generate_react_feature_importance(self, props: Dict[str, Any]) -> str:
        """Placeholder for React feature importance component"""
        return "// React feature importance component (implementation details omitted for brevity)"
    
    def _generate_react_confusion_matrix(self, props: Dict[str, Any]) -> str:
        """Placeholder for React confusion matrix component"""
        return "// React confusion matrix component (implementation details omitted for brevity)"
    
    def _generate_react_roc_curve(self, props: Dict[str, Any]) -> str:
        """Placeholder for React ROC curve component"""
        return "// React ROC curve component (implementation details omitted for brevity)"
    
    def _generate_react_precision_recall_curve(self, props: Dict[str, Any]) -> str:
        """Placeholder for React precision-recall curve component"""
        return "// React precision-recall curve component (implementation details omitted for brevity)"
    
    def _generate_react_residual_plot(self, props: Dict[str, Any]) -> str:
        """Placeholder for React residual plot component"""
        return "// React residual plot component (implementation details omitted for brevity)"
    
    def _generate_vue_model_prediction(self, props: Dict[str, Any]) -> str:
        """Placeholder for Vue model prediction component"""
        return "<!-- Vue model prediction component (implementation details omitted for brevity) -->"
    
    def _generate_vue_feature_importance(self, props: Dict[str, Any]) -> str:
        """Placeholder for Vue feature importance component"""
        return "<!-- Vue feature importance component (implementation details omitted for brevity) -->"
    
    def _generate_vue_confusion_matrix(self, props: Dict[str, Any]) -> str:
        """Placeholder for Vue confusion matrix component"""
        return "<!-- Vue confusion matrix component (implementation details omitted for brevity) -->"
    
    def _generate_vue_roc_curve(self, props: Dict[str, Any]) -> str:
        """Placeholder for Vue ROC curve component"""
        return "<!-- Vue ROC curve component (implementation details omitted for brevity) -->"
    
    def _generate_vue_precision_recall_curve(self, props: Dict[str, Any]) -> str:
        """Placeholder for Vue precision-recall curve component"""
        return "<!-- Vue precision-recall curve component (implementation details omitted for brevity) -->"
    
    def _generate_vue_residual_plot(self, props: Dict[str, Any]) -> str:
        """Placeholder for Vue residual plot component"""
        return "<!-- Vue residual plot component (implementation details omitted for brevity) -->"
