"""
Form generator component for SBYB UI Generator.

This module provides functionality for generating interactive forms
for machine learning models without writing code.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import shutil
import tempfile

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import UIGenerationError


class FormGenerator(SBYBComponent):
    """
    Form generator component.
    
    This component generates interactive forms for machine learning models.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the form generator.
        
        Args:
            config: Configuration dictionary for the generator.
        """
        super().__init__(config)
        self.fields = []
        self.form_config = {
            "title": "ML Model Form",
            "description": "Enter data to make predictions",
            "submit_button_text": "Submit",
            "reset_button_text": "Reset",
            "success_message": "Form submitted successfully!",
            "error_message": "An error occurred. Please try again.",
            "theme": "default"
        }
        self.validation_rules = {}
        self.callbacks = {}
    
    def set_form_config(self, config: Dict[str, Any]) -> None:
        """
        Set form configuration.
        
        Args:
            config: Form configuration dictionary.
        """
        self.form_config.update(config)
    
    def add_field(self, field_id: str, field_type: str, label: str,
                 required: bool = False, default_value: Any = None,
                 placeholder: Optional[str] = None,
                 options: Optional[List[Any]] = None,
                 help_text: Optional[str] = None,
                 config: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a field to the form.
        
        Args:
            field_id: Unique identifier for the field.
            field_type: Type of field.
            label: Label for the field.
            required: Whether the field is required.
            default_value: Default value for the field.
            placeholder: Placeholder text for the field.
            options: Options for select fields.
            help_text: Help text for the field.
            config: Additional configuration for the field.
            
        Returns:
            ID of the added field.
        """
        # Check if field ID already exists
        if any(field["id"] == field_id for field in self.fields):
            raise UIGenerationError(f"Field ID '{field_id}' already exists.")
        
        # Create field
        field = {
            "id": field_id,
            "type": field_type,
            "label": label,
            "required": required,
            "default_value": default_value,
            "placeholder": placeholder,
            "options": options,
            "help_text": help_text,
            "config": config or {}
        }
        
        # Add field
        self.fields.append(field)
        
        return field_id
    
    def add_validation_rule(self, field_id: str, rule_type: str,
                           message: str, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a validation rule to a field.
        
        Args:
            field_id: ID of the field to validate.
            rule_type: Type of validation rule.
            message: Error message to display.
            config: Configuration for the validation rule.
        """
        # Check if field exists
        if not any(field["id"] == field_id for field in self.fields):
            raise UIGenerationError(f"Field ID '{field_id}' does not exist.")
        
        # Initialize validation rules for field if not exists
        if field_id not in self.validation_rules:
            self.validation_rules[field_id] = []
        
        # Add validation rule
        self.validation_rules[field_id].append({
            "type": rule_type,
            "message": message,
            "config": config or {}
        })
    
    def add_callback(self, callback_id: str, event_type: str,
                    field_ids: List[str], function: str) -> str:
        """
        Add a callback to the form.
        
        Args:
            callback_id: Unique identifier for the callback.
            event_type: Type of event to trigger the callback.
            field_ids: List of field IDs involved in the callback.
            function: JavaScript function code.
            
        Returns:
            ID of the added callback.
        """
        # Check if callback ID already exists
        if callback_id in self.callbacks:
            raise UIGenerationError(f"Callback ID '{callback_id}' already exists.")
        
        # Check if fields exist
        for field_id in field_ids:
            if not any(field["id"] == field_id for field in self.fields):
                raise UIGenerationError(f"Field ID '{field_id}' does not exist.")
        
        # Create callback
        callback = {
            "event_type": event_type,
            "field_ids": field_ids,
            "function": function
        }
        
        # Add callback
        self.callbacks[callback_id] = callback
        
        return callback_id
    
    def generate_form(self, output_dir: str, form_name: str = "ML Model Form",
                     framework: str = "html") -> str:
        """
        Generate a form.
        
        Args:
            output_dir: Directory to save the generated form.
            form_name: Name of the form.
            framework: Framework to use for the form.
            
        Returns:
            Path to the generated form.
        """
        if framework.lower() == "html":
            return self._generate_html_form(output_dir, form_name)
        elif framework.lower() == "react":
            return self._generate_react_form(output_dir, form_name)
        elif framework.lower() == "vue":
            return self._generate_vue_form(output_dir, form_name)
        else:
            raise UIGenerationError(f"Unsupported framework: {framework}")
    
    def _generate_html_form(self, output_dir: str, form_name: str) -> str:
        """
        Generate an HTML form.
        
        Args:
            output_dir: Directory to save the generated form.
            form_name: Name of the form.
            
        Returns:
            Path to the generated form.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate index.html
        html_content = self._generate_html_content(form_name)
        
        with open(os.path.join(output_dir, "index.html"), "w") as f:
            f.write(html_content)
        
        # Generate CSS
        css_content = self._generate_css_content()
        
        with open(os.path.join(output_dir, "styles.css"), "w") as f:
            f.write(css_content)
        
        # Generate JavaScript
        js_content = self._generate_js_content()
        
        with open(os.path.join(output_dir, "script.js"), "w") as f:
            f.write(js_content)
        
        # Generate form configuration
        form_config = {
            "name": form_name,
            "fields": self.fields,
            "validation_rules": self.validation_rules,
            "callbacks": self.callbacks,
            "form_config": self.form_config
        }
        
        with open(os.path.join(output_dir, "form_config.json"), "w") as f:
            json.dump(form_config, f, indent=2)
        
        # Generate README.md
        readme_content = self._generate_readme_content(form_name)
        
        with open(os.path.join(output_dir, "README.md"), "w") as f:
            f.write(readme_content)
        
        return output_dir
    
    def _generate_react_form(self, output_dir: str, form_name: str) -> str:
        """
        Generate a React form.
        
        Args:
            output_dir: Directory to save the generated form.
            form_name: Name of the form.
            
        Returns:
            Path to the generated form.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create src directory
        src_dir = os.path.join(output_dir, "src")
        os.makedirs(src_dir, exist_ok=True)
        
        # Create components directory
        components_dir = os.path.join(src_dir, "components")
        os.makedirs(components_dir, exist_ok=True)
        
        # Generate package.json
        package_json_content = self._generate_react_package_json(form_name)
        
        with open(os.path.join(output_dir, "package.json"), "w") as f:
            f.write(package_json_content)
        
        # Generate index.html
        index_html_content = self._generate_react_index_html(form_name)
        
        with open(os.path.join(output_dir, "public", "index.html"), "w") as f:
            f.write(index_html_content)
        
        # Generate App.js
        app_js_content = self._generate_react_app_js()
        
        with open(os.path.join(src_dir, "App.js"), "w") as f:
            f.write(app_js_content)
        
        # Generate index.js
        index_js_content = self._generate_react_index_js()
        
        with open(os.path.join(src_dir, "index.js"), "w") as f:
            f.write(index_js_content)
        
        # Generate Form.js
        form_js_content = self._generate_react_form_js()
        
        with open(os.path.join(components_dir, "Form.js"), "w") as f:
            f.write(form_js_content)
        
        # Generate FormField.js
        form_field_js_content = self._generate_react_form_field_js()
        
        with open(os.path.join(components_dir, "FormField.js"), "w") as f:
            f.write(form_field_js_content)
        
        # Generate App.css
        app_css_content = self._generate_react_app_css()
        
        with open(os.path.join(src_dir, "App.css"), "w") as f:
            f.write(app_css_content)
        
        # Generate form configuration
        form_config = {
            "name": form_name,
            "fields": self.fields,
            "validation_rules": self.validation_rules,
            "callbacks": self.callbacks,
            "form_config": self.form_config
        }
        
        with open(os.path.join(src_dir, "form_config.json"), "w") as f:
            json.dump(form_config, f, indent=2)
        
        # Generate README.md
        readme_content = self._generate_react_readme_content(form_name)
        
        with open(os.path.join(output_dir, "README.md"), "w") as f:
            f.write(readme_content)
        
        return output_dir
    
    def _generate_vue_form(self, output_dir: str, form_name: str) -> str:
        """
        Generate a Vue form.
        
        Args:
            output_dir: Directory to save the generated form.
            form_name: Name of the form.
            
        Returns:
            Path to the generated form.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create src directory
        src_dir = os.path.join(output_dir, "src")
        os.makedirs(src_dir, exist_ok=True)
        
        # Create components directory
        components_dir = os.path.join(src_dir, "components")
        os.makedirs(components_dir, exist_ok=True)
        
        # Generate package.json
        package_json_content = self._generate_vue_package_json(form_name)
        
        with open(os.path.join(output_dir, "package.json"), "w") as f:
            f.write(package_json_content)
        
        # Generate index.html
        index_html_content = self._generate_vue_index_html(form_name)
        
        with open(os.path.join(output_dir, "public", "index.html"), "w") as f:
            f.write(index_html_content)
        
        # Generate main.js
        main_js_content = self._generate_vue_main_js()
        
        with open(os.path.join(src_dir, "main.js"), "w") as f:
            f.write(main_js_content)
        
        # Generate App.vue
        app_vue_content = self._generate_vue_app_vue()
        
        with open(os.path.join(src_dir, "App.vue"), "w") as f:
            f.write(app_vue_content)
        
        # Generate Form.vue
        form_vue_content = self._generate_vue_form_vue()
        
        with open(os.path.join(components_dir, "Form.vue"), "w") as f:
            f.write(form_vue_content)
        
        # Generate FormField.vue
        form_field_vue_content = self._generate_vue_form_field_vue()
        
        with open(os.path.join(components_dir, "FormField.vue"), "w") as f:
            f.write(form_field_vue_content)
        
        # Generate form configuration
        form_config = {
            "name": form_name,
            "fields": self.fields,
            "validation_rules": self.validation_rules,
            "callbacks": self.callbacks,
            "form_config": self.form_config
        }
        
        with open(os.path.join(src_dir, "form_config.json"), "w") as f:
            json.dump(form_config, f, indent=2)
        
        # Generate README.md
        readme_content = self._generate_vue_readme_content(form_name)
        
        with open(os.path.join(output_dir, "README.md"), "w") as f:
            f.write(readme_content)
        
        return output_dir
    
    def _generate_html_content(self, form_name: str) -> str:
        """
        Generate HTML content for the form.
        
        Args:
            form_name: Name of the form.
            
        Returns:
            HTML content.
        """
        # Generate field HTML
        fields_html = ""
        for field in self.fields:
            field_id = field["id"]
            field_type = field["type"]
            label = field["label"]
            required = field["required"]
            default_value = field["default_value"]
            placeholder = field["placeholder"] or ""
            options = field["options"]
            help_text = field["help_text"] or ""
            
            required_attr = "required" if required else ""
            
            if field_type == "text":
                default_value_attr = f'value="{default_value}"' if default_value is not None else ""
                fields_html += f"""
                <div class="form-group">
                    <label for="{field_id}">{label}</label>
                    <input type="text" id="{field_id}" name="{field_id}" {default_value_attr} placeholder="{placeholder}" {required_attr}>
                    <small class="help-text">{help_text}</small>
                    <div class="error-message" id="{field_id}-error"></div>
                </div>
                """
            
            elif field_type == "number":
                default_value_attr = f'value="{default_value}"' if default_value is not None else ""
                min_attr = f'min="{field["config"].get("min")}"' if field["config"].get("min") is not None else ""
                max_attr = f'max="{field["config"].get("max")}"' if field["config"].get("max") is not None else ""
                step_attr = f'step="{field["config"].get("step")}"' if field["config"].get("step") is not None else ""
                
                fields_html += f"""
                <div class="form-group">
                    <label for="{field_id}">{label}</label>
                    <input type="number" id="{field_id}" name="{field_id}" {default_value_attr} {min_attr} {max_attr} {step_attr} placeholder="{placeholder}" {required_attr}>
                    <small class="help-text">{help_text}</small>
                    <div class="error-message" id="{field_id}-error"></div>
                </div>
                """
            
            elif field_type == "textarea":
                default_value = default_value or ""
                rows_attr = f'rows="{field["config"].get("rows", 4)}"'
                cols_attr = f'cols="{field["config"].get("cols", 50)}"'
                
                fields_html += f"""
                <div class="form-group">
                    <label for="{field_id}">{label}</label>
                    <textarea id="{field_id}" name="{field_id}" {rows_attr} {cols_attr} placeholder="{placeholder}" {required_attr}>{default_value}</textarea>
                    <small class="help-text">{help_text}</small>
                    <div class="error-message" id="{field_id}-error"></div>
                </div>
                """
            
            elif field_type == "select":
                options_html = ""
                if options:
                    for option in options:
                        selected = "selected" if option == default_value else ""
                        options_html += f'<option value="{option}" {selected}>{option}</option>'
                
                fields_html += f"""
                <div class="form-group">
                    <label for="{field_id}">{label}</label>
                    <select id="{field_id}" name="{field_id}" {required_attr}>
                        {options_html}
                    </select>
                    <small class="help-text">{help_text}</small>
                    <div class="error-message" id="{field_id}-error"></div>
                </div>
                """
            
            elif field_type == "checkbox":
                checked = "checked" if default_value else ""
                
                fields_html += f"""
                <div class="form-group checkbox-group">
                    <input type="checkbox" id="{field_id}" name="{field_id}" {checked} {required_attr}>
                    <label for="{field_id}">{label}</label>
                    <small class="help-text">{help_text}</small>
                    <div class="error-message" id="{field_id}-error"></div>
                </div>
                """
            
            elif field_type == "radio":
                options_html = ""
                if options:
                    for i, option in enumerate(options):
                        option_id = f"{field_id}_{i}"
                        checked = "checked" if option == default_value else ""
                        options_html += f"""
                        <div class="radio-option">
                            <input type="radio" id="{option_id}" name="{field_id}" value="{option}" {checked} {required_attr}>
                            <label for="{option_id}">{option}</label>
                        </div>
                        """
                
                fields_html += f"""
                <div class="form-group radio-group">
                    <label class="group-label">{label}</label>
                    <div class="radio-options">
                        {options_html}
                    </div>
                    <small class="help-text">{help_text}</small>
                    <div class="error-message" id="{field_id}-error"></div>
                </div>
                """
            
            elif field_type == "date":
                default_value_attr = f'value="{default_value}"' if default_value is not None else ""
                min_attr = f'min="{field["config"].get("min")}"' if field["config"].get("min") is not None else ""
                max_attr = f'max="{field["config"].get("max")}"' if field["config"].get("max") is not None else ""
                
                fields_html += f"""
                <div class="form-group">
                    <label for="{field_id}">{label}</label>
                    <input type="date" id="{field_id}" name="{field_id}" {default_value_attr} {min_attr} {max_attr} {required_attr}>
                    <small class="help-text">{help_text}</small>
                    <div class="error-message" id="{field_id}-error"></div>
                </div>
                """
            
            elif field_type == "file":
                accept_attr = f'accept="{field["config"].get("accept", "")}"' if field["config"].get("accept") is not None else ""
                multiple_attr = "multiple" if field["config"].get("multiple") else ""
                
                fields_html += f"""
                <div class="form-group">
                    <label for="{field_id}">{label}</label>
                    <input type="file" id="{field_id}" name="{field_id}" {accept_attr} {multiple_attr} {required_attr}>
                    <small class="help-text">{help_text}</small>
                    <div class="error-message" id="{field_id}-error"></div>
                </div>
                """
            
            elif field_type == "range":
                default_value_attr = f'value="{default_value}"' if default_value is not None else ""
                min_attr = f'min="{field["config"].get("min", 0)}"'
                max_attr = f'max="{field["config"].get("max", 100)}"'
                step_attr = f'step="{field["config"].get("step", 1)}"'
                
                fields_html += f"""
                <div class="form-group">
                    <label for="{field_id}">{label}</label>
                    <div class="range-container">
                        <input type="range" id="{field_id}" name="{field_id}" {default_value_attr} {min_attr} {max_attr} {step_attr} {required_attr}>
                        <span class="range-value" id="{field_id}-value">{default_value or field["config"].get("min", 0)}</span>
                    </div>
                    <small class="help-text">{help_text}</small>
                    <div class="error-message" id="{field_id}-error"></div>
                </div>
                """
        
        # Generate HTML content
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{form_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>{self.form_config["title"]}</h1>
        <p class="form-description">{self.form_config["description"]}</p>
        
        <form id="ml-form">
            {fields_html}
            
            <div class="form-actions">
                <button type="submit" class="submit-button">{self.form_config["submit_button_text"]}</button>
                <button type="reset" class="reset-button">{self.form_config["reset_button_text"]}</button>
            </div>
        </form>
        
        <div id="form-result" class="form-result"></div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>
"""
        
        return html_content
    
    def _generate_css_content(self) -> str:
        """
        Generate CSS content for the form.
        
        Returns:
            CSS content.
        """
        css_content = """
/* Form Styles */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f8f9fa;
}

.container {
    max-width: 800px;
    margin: 40px auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
    margin-bottom: 20px;
    color: #2c3e50;
    text-align: center;
}

.form-description {
    margin-bottom: 30px;
    text-align: center;
    color: #666;
}

.form-group {
    margin-bottom: 20px;
}

label, .group-label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #2c3e50;
}

input[type="text"],
input[type="number"],
input[type="date"],
textarea,
select {
    width: 100%;
    padding: 10px 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
    transition: border-color 0.3s;
}

input[type="text"]:focus,
input[type="number"]:focus,
input[type="date"]:focus,
textarea:focus,
select:focus {
    border-color: #3498db;
    outline: none;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.checkbox-group, .radio-group {
    display: flex;
    flex-direction: column;
}

.checkbox-group label {
    margin-left: 10px;
    display: inline;
}

.radio-options {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.radio-option {
    display: flex;
    align-items: center;
}

.radio-option label {
    margin-left: 10px;
    margin-bottom: 0;
    font-weight: normal;
}

.range-container {
    display: flex;
    align-items: center;
    gap: 15px;
}

input[type="range"] {
    flex: 1;
}

.range-value {
    min-width: 40px;
    text-align: center;
    font-weight: bold;
    color: #3498db;
}

.help-text {
    display: block;
    margin-top: 5px;
    color: #666;
    font-size: 14px;
}

.error-message {
    color: #e74c3c;
    font-size: 14px;
    margin-top: 5px;
    min-height: 20px;
}

.form-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
}

.submit-button, .reset-button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.submit-button {
    background-color: #3498db;
    color: white;
}

.submit-button:hover {
    background-color: #2980b9;
}

.reset-button {
    background-color: #e74c3c;
    color: white;
}

.reset-button:hover {
    background-color: #c0392b;
}

.form-result {
    margin-top: 30px;
    padding: 15px;
    border-radius: 4px;
    display: none;
}

.form-result.success {
    display: block;
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.form-result.error {
    display: block;
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

/* Responsive styles */
@media (max-width: 768px) {
    .container {
        margin: 20px;
        padding: 15px;
    }
    
    .form-actions {
        flex-direction: column;
        gap: 10px;
    }
    
    .submit-button, .reset-button {
        width: 100%;
    }
}
"""
        
        return css_content
    
    def _generate_js_content(self) -> str:
        """
        Generate JavaScript content for the form.
        
        Returns:
            JavaScript content.
        """
        # Generate validation rules
        validation_js = ""
        for field_id, rules in self.validation_rules.items():
            for rule in rules:
                rule_type = rule["type"]
                message = rule["message"]
                config = rule["config"]
                
                if rule_type == "required":
                    validation_js += f"""
    // Required validation for {field_id}
    if (formData.get('{field_id}') === '' || formData.get('{field_id}') === null) {{
        valid = false;
        document.getElementById('{field_id}-error').textContent = '{message}';
    }}
"""
                
                elif rule_type == "min_length":
                    min_length = config.get("min_length", 1)
                    validation_js += f"""
    // Min length validation for {field_id}
    if (formData.get('{field_id}') && formData.get('{field_id}').length < {min_length}) {{
        valid = false;
        document.getElementById('{field_id}-error').textContent = '{message}';
    }}
"""
                
                elif rule_type == "max_length":
                    max_length = config.get("max_length", 100)
                    validation_js += f"""
    // Max length validation for {field_id}
    if (formData.get('{field_id}') && formData.get('{field_id}').length > {max_length}) {{
        valid = false;
        document.getElementById('{field_id}-error').textContent = '{message}';
    }}
"""
                
                elif rule_type == "pattern":
                    pattern = config.get("pattern", "")
                    validation_js += f"""
    // Pattern validation for {field_id}
    if (formData.get('{field_id}') && !new RegExp('{pattern}').test(formData.get('{field_id}'))) {{
        valid = false;
        document.getElementById('{field_id}-error').textContent = '{message}';
    }}
"""
                
                elif rule_type == "min_value":
                    min_value = config.get("min_value", 0)
                    validation_js += f"""
    // Min value validation for {field_id}
    if (formData.get('{field_id}') && parseFloat(formData.get('{field_id}')) < {min_value}) {{
        valid = false;
        document.getElementById('{field_id}-error').textContent = '{message}';
    }}
"""
                
                elif rule_type == "max_value":
                    max_value = config.get("max_value", 100)
                    validation_js += f"""
    // Max value validation for {field_id}
    if (formData.get('{field_id}') && parseFloat(formData.get('{field_id}')) > {max_value}) {{
        valid = false;
        document.getElementById('{field_id}-error').textContent = '{message}';
    }}
"""
                
                elif rule_type == "email":
                    validation_js += f"""
    // Email validation for {field_id}
    if (formData.get('{field_id}') && !/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{{2,}}$/.test(formData.get('{field_id}'))) {{
        valid = false;
        document.getElementById('{field_id}-error').textContent = '{message}';
    }}
"""
        
        # Generate range input handlers
        range_handlers = ""
        for field in self.fields:
            if field["type"] == "range":
                field_id = field["id"]
                range_handlers += f"""
    // Range input handler for {field_id}
    const {field_id}Input = document.getElementById('{field_id}');
    const {field_id}Value = document.getElementById('{field_id}-value');
    
    if ({field_id}Input && {field_id}Value) {{
        {field_id}Input.addEventListener('input', function() {{
            {field_id}Value.textContent = this.value;
        }});
    }}
"""
        
        # Generate callbacks
        callbacks_js = ""
        for callback_id, callback in self.callbacks.items():
            event_type = callback["event_type"]
            field_ids = callback["field_ids"]
            function_code = callback["function"]
            
            for field_id in field_ids:
                callbacks_js += f"""
    // {callback_id} callback for {field_id}
    document.getElementById('{field_id}').addEventListener('{event_type}', function(event) {{
        {function_code}
    }});
"""
        
        # Generate JavaScript content
        js_content = f"""
document.addEventListener('DOMContentLoaded', function() {{
    const form = document.getElementById('ml-form');
    const formResult = document.getElementById('form-result');
    
    // Clear error messages when input changes
    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {{
        input.addEventListener('input', function() {{
            const errorElement = document.getElementById(`${{this.id}}-error`);
            if (errorElement) {{
                errorElement.textContent = '';
            }}
        }});
    }});
    
    // Range input handlers
    {range_handlers}
    
    // Custom callbacks
    {callbacks_js}
    
    // Form submission
    form.addEventListener('submit', function(event) {{
        event.preventDefault();
        
        // Clear previous error messages
        const errorElements = document.querySelectorAll('.error-message');
        errorElements.forEach(element => {{
            element.textContent = '';
        }});
        
        // Hide result message
        formResult.style.display = 'none';
        formResult.classList.remove('success', 'error');
        
        // Get form data
        const formData = new FormData(form);
        
        // Validate form
        let valid = true;
        
        {validation_js}
        
        if (valid) {{
            // Convert FormData to object
            const formDataObj = Object.fromEntries(formData.entries());
            
            // Here you would typically send the data to a server
            // For demonstration, we'll just show a success message
            console.log('Form data:', formDataObj);
            
            // Show success message
            formResult.textContent = '{self.form_config["success_message"]}';
            formResult.classList.add('success');
            formResult.style.display = 'block';
            
            // Optional: Reset form after successful submission
            // form.reset();
        }} else {{
            // Show error message
            formResult.textContent = '{self.form_config["error_message"]}';
            formResult.classList.add('error');
            formResult.style.display = 'block';
        }}
    }});
    
    // Form reset
    form.addEventListener('reset', function() {{
        // Clear error messages
        const errorElements = document.querySelectorAll('.error-message');
        errorElements.forEach(element => {{
            element.textContent = '';
        }});
        
        // Hide result message
        formResult.style.display = 'none';
        formResult.classList.remove('success', 'error');
        
        // Reset range value displays
        const rangeInputs = form.querySelectorAll('input[type="range"]');
        rangeInputs.forEach(input => {{
            const valueElement = document.getElementById(`${{input.id}}-value`);
            if (valueElement) {{
                valueElement.textContent = input.value;
            }}
        }});
    }});
}});
"""
        
        return js_content
    
    def _generate_readme_content(self, form_name: str) -> str:
        """
        Generate README.md content for the form.
        
        Args:
            form_name: Name of the form.
            
        Returns:
            README.md content.
        """
        readme_content = f"""
# {form_name}

This is an HTML form generated by SBYB UI Generator.

## Usage

Simply open the `index.html` file in a web browser to view and interact with the form.

## Features

- Responsive design that works on desktop and mobile devices
- Client-side form validation
- Interactive form elements
- Customizable styling

## Structure

- `index.html`: The main HTML file containing the form
- `styles.css`: CSS styles for the form
- `script.js`: JavaScript for form validation and interactivity
- `form_config.json`: Configuration file for the form

## Customization

You can customize the form by editing the HTML, CSS, and JavaScript files. The form configuration is stored in `form_config.json`.

## Integration

To integrate this form with a backend:

1. Modify the form submission handler in `script.js` to send the form data to your server
2. Implement server-side validation and processing
3. Update the success and error messages accordingly
"""
        
        return readme_content
    
    def _generate_react_package_json(self, form_name: str) -> str:
        """
        Generate package.json content for React form.
        
        Args:
            form_name: Name of the form.
            
        Returns:
            package.json content.
        """
        package_name = form_name.lower().replace(" ", "-")
        
        return f"""{{
  "name": "{package_name}",
  "version": "0.1.0",
  "private": true,
  "dependencies": {{
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4"
  }},
  "scripts": {{
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }},
  "eslintConfig": {{
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  }},
  "browserslist": {{
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
  }}
}}
"""
    
    def _generate_react_index_html(self, form_name: str) -> str:
        """
        Generate index.html content for React form.
        
        Args:
            form_name: Name of the form.
            
        Returns:
            index.html content.
        """
        return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="{form_name} - Generated by SBYB UI Generator"
    />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <title>{form_name}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
"""
    
    def _generate_react_app_js(self) -> str:
        """
        Generate App.js content for React form.
        
        Returns:
            App.js content.
        """
        return """import React from 'react';
import './App.css';
import Form from './components/Form';
import formConfig from './form_config.json';

function App() {
  return (
    <div className="App">
      <div className="container">
        <h1>{formConfig.form_config.title}</h1>
        <p className="form-description">{formConfig.form_config.description}</p>
        <Form />
      </div>
    </div>
  );
}

export default App;
"""
    
    def _generate_react_index_js(self) -> str:
        """
        Generate index.js content for React form.
        
        Returns:
            index.js content.
        """
        return """import React from 'react';
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

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
"""
    
    def _generate_react_form_js(self) -> str:
        """
        Generate Form.js content for React form.
        
        Returns:
            Form.js content.
        """
        return """import React, { useState } from 'react';
import FormField from './FormField';
import formConfig from '../form_config.json';

const Form = () => {
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});
  const [formResult, setFormResult] = useState({ message: '', type: '' });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    // Handle different input types
    const inputValue = type === 'checkbox' ? checked : value;
    
    setFormData({
      ...formData,
      [name]: inputValue
    });
    
    // Clear error when field is changed
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: ''
      });
    }
  };

  const validateForm = () => {
    const newErrors = {};
    let isValid = true;
    
    // Process validation rules
    Object.entries(formConfig.validation_rules).forEach(([fieldId, rules]) => {
      rules.forEach(rule => {
        const value = formData[fieldId];
        
        switch (rule.type) {
          case 'required':
            if (!value || value === '') {
              newErrors[fieldId] = rule.message;
              isValid = false;
            }
            break;
            
          case 'min_length':
            if (value && value.length < rule.config.min_length) {
              newErrors[fieldId] = rule.message;
              isValid = false;
            }
            break;
            
          case 'max_length':
            if (value && value.length > rule.config.max_length) {
              newErrors[fieldId] = rule.message;
              isValid = false;
            }
            break;
            
          case 'pattern':
            if (value && !new RegExp(rule.config.pattern).test(value)) {
              newErrors[fieldId] = rule.message;
              isValid = false;
            }
            break;
            
          case 'min_value':
            if (value && parseFloat(value) < rule.config.min_value) {
              newErrors[fieldId] = rule.message;
              isValid = false;
            }
            break;
            
          case 'max_value':
            if (value && parseFloat(value) > rule.config.max_value) {
              newErrors[fieldId] = rule.message;
              isValid = false;
            }
            break;
            
          case 'email':
            if (value && !/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value)) {
              newErrors[fieldId] = rule.message;
              isValid = false;
            }
            break;
            
          default:
            break;
        }
      });
    });
    
    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Reset form result
    setFormResult({ message: '', type: '' });
    
    // Validate form
    if (validateForm()) {
      // Here you would typically send the data to a server
      console.log('Form data:', formData);
      
      // Show success message
      setFormResult({
        message: formConfig.form_config.success_message,
        type: 'success'
      });
      
      // Optional: Reset form after successful submission
      // setFormData({});
    } else {
      // Show error message
      setFormResult({
        message: formConfig.form_config.error_message,
        type: 'error'
      });
    }
  };

  const handleReset = () => {
    setFormData({});
    setErrors({});
    setFormResult({ message: '', type: '' });
  };

  return (
    <div>
      <form onSubmit={handleSubmit} onReset={handleReset}>
        {formConfig.fields.map(field => (
          <FormField
            key={field.id}
            field={field}
            value={formData[field.id] || ''}
            error={errors[field.id] || ''}
            onChange={handleChange}
          />
        ))}
        
        <div className="form-actions">
          <button type="submit" className="submit-button">
            {formConfig.form_config.submit_button_text}
          </button>
          <button type="reset" className="reset-button">
            {formConfig.form_config.reset_button_text}
          </button>
        </div>
      </form>
      
      {formResult.message && (
        <div className={`form-result ${formResult.type}`}>
          {formResult.message}
        </div>
      )}
    </div>
  );
};

export default Form;
"""
    
    def _generate_react_form_field_js(self) -> str:
        """
        Generate FormField.js content for React form.
        
        Returns:
            FormField.js content.
        """
        return """import React from 'react';

const FormField = ({ field, value, error, onChange }) => {
  const {
    id,
    type,
    label,
    required,
    placeholder,
    options,
    help_text,
    config
  } = field;

  const renderField = () => {
    switch (type) {
      case 'text':
        return (
          <input
            type="text"
            id={id}
            name={id}
            value={value}
            placeholder={placeholder || ''}
            required={required}
            onChange={onChange}
          />
        );
        
      case 'number':
        return (
          <input
            type="number"
            id={id}
            name={id}
            value={value}
            placeholder={placeholder || ''}
            min={config?.min}
            max={config?.max}
            step={config?.step}
            required={required}
            onChange={onChange}
          />
        );
        
      case 'textarea':
        return (
          <textarea
            id={id}
            name={id}
            value={value}
            placeholder={placeholder || ''}
            rows={config?.rows || 4}
            cols={config?.cols || 50}
            required={required}
            onChange={onChange}
          />
        );
        
      case 'select':
        return (
          <select
            id={id}
            name={id}
            value={value}
            required={required}
            onChange={onChange}
          >
            {options && options.map((option, index) => (
              <option key={index} value={option}>
                {option}
              </option>
            ))}
          </select>
        );
        
      case 'checkbox':
        return (
          <div className="checkbox-group">
            <input
              type="checkbox"
              id={id}
              name={id}
              checked={value === true}
              required={required}
              onChange={onChange}
            />
            <label htmlFor={id}>{label}</label>
          </div>
        );
        
      case 'radio':
        return (
          <div className="radio-group">
            <label className="group-label">{label}</label>
            <div className="radio-options">
              {options && options.map((option, index) => (
                <div key={index} className="radio-option">
                  <input
                    type="radio"
                    id={`${id}_${index}`}
                    name={id}
                    value={option}
                    checked={value === option}
                    required={required}
                    onChange={onChange}
                  />
                  <label htmlFor={`${id}_${index}`}>{option}</label>
                </div>
              ))}
            </div>
          </div>
        );
        
      case 'date':
        return (
          <input
            type="date"
            id={id}
            name={id}
            value={value}
            min={config?.min}
            max={config?.max}
            required={required}
            onChange={onChange}
          />
        );
        
      case 'file':
        return (
          <input
            type="file"
            id={id}
            name={id}
            accept={config?.accept}
            multiple={config?.multiple}
            required={required}
            onChange={onChange}
          />
        );
        
      case 'range':
        return (
          <div className="range-container">
            <input
              type="range"
              id={id}
              name={id}
              value={value}
              min={config?.min || 0}
              max={config?.max || 100}
              step={config?.step || 1}
              required={required}
              onChange={onChange}
            />
            <span className="range-value">{value || config?.min || 0}</span>
          </div>
        );
        
      default:
        return <div>Unsupported field type: {type}</div>;
    }
  };

  return (
    <div className="form-group">
      {type !== 'checkbox' && <label htmlFor={id}>{label}</label>}
      {renderField()}
      {help_text && <small className="help-text">{help_text}</small>}
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default FormField;
"""
    
    def _generate_react_app_css(self) -> str:
        """
        Generate App.css content for React form.
        
        Returns:
            App.css content.
        """
        return """/* Form Styles */
.App {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f8f9fa;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.container {
  max-width: 800px;
  width: 100%;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  margin-bottom: 20px;
  color: #2c3e50;
  text-align: center;
}

.form-description {
  margin-bottom: 30px;
  text-align: center;
  color: #666;
}

.form-group {
  margin-bottom: 20px;
}

label, .group-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
}

input[type="text"],
input[type="number"],
input[type="date"],
textarea,
select {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s;
}

input[type="text"]:focus,
input[type="number"]:focus,
input[type="date"]:focus,
textarea:focus,
select:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.checkbox-group, .radio-group {
  display: flex;
  flex-direction: column;
}

.checkbox-group label {
  margin-left: 10px;
  display: inline;
}

.radio-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.radio-option {
  display: flex;
  align-items: center;
}

.radio-option label {
  margin-left: 10px;
  margin-bottom: 0;
  font-weight: normal;
}

.range-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

input[type="range"] {
  flex: 1;
}

.range-value {
  min-width: 40px;
  text-align: center;
  font-weight: bold;
  color: #3498db;
}

.help-text {
  display: block;
  margin-top: 5px;
  color: #666;
  font-size: 14px;
}

.error-message {
  color: #e74c3c;
  font-size: 14px;
  margin-top: 5px;
  min-height: 20px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.submit-button, .reset-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button {
  background-color: #3498db;
  color: white;
}

.submit-button:hover {
  background-color: #2980b9;
}

.reset-button {
  background-color: #e74c3c;
  color: white;
}

.reset-button:hover {
  background-color: #c0392b;
}

.form-result {
  margin-top: 30px;
  padding: 15px;
  border-radius: 4px;
}

.form-result.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.form-result.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

/* Responsive styles */
@media (max-width: 768px) {
  .container {
    padding: 15px;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 10px;
  }
  
  .submit-button, .reset-button {
    width: 100%;
  }
}
"""
    
    def _generate_react_readme_content(self, form_name: str) -> str:
        """
        Generate README.md content for React form.
        
        Args:
            form_name: Name of the form.
            
        Returns:
            README.md content.
        """
        return f"""
# {form_name}

This is a React form application generated by SBYB UI Generator.

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   npm install
   ```

## Usage

### Development

```
npm start
```

The application will be available at http://localhost:3000

### Production Build

```
npm run build
```

This will create a production-ready build in the `build` folder.

## Features

- Responsive design that works on desktop and mobile devices
- Client-side form validation
- Interactive form elements
- Customizable styling

## Structure

- `src/App.js`: Main application component
- `src/components/Form.js`: Form component with validation logic
- `src/components/FormField.js`: Reusable form field component
- `src/form_config.json`: Configuration file for the form

## Customization

You can customize the form by editing the React components and CSS files. The form configuration is stored in `src/form_config.json`.

## Integration

To integrate this form with a backend:

1. Modify the form submission handler in `src/components/Form.js` to send the form data to your server
2. Implement server-side validation and processing
3. Update the success and error messages accordingly
"""
    
    def _generate_vue_package_json(self, form_name: str) -> str:
        """
        Generate package.json content for Vue form.
        
        Args:
            form_name: Name of the form.
            
        Returns:
            package.json content.
        """
        package_name = form_name.lower().replace(" ", "-")
        
        return f"""{{
  "name": "{package_name}",
  "version": "0.1.0",
  "private": true,
  "scripts": {{
    "serve": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "lint": "vue-cli-service lint"
  }},
  "dependencies": {{
    "core-js": "^3.8.3",
    "vue": "^3.2.13"
  }},
  "devDependencies": {{
    "@babel/core": "^7.12.16",
    "@babel/eslint-parser": "^7.12.16",
    "@vue/cli-plugin-babel": "~5.0.0",
    "@vue/cli-plugin-eslint": "~5.0.0",
    "@vue/cli-service": "~5.0.0",
    "eslint": "^7.32.0",
    "eslint-plugin-vue": "^8.0.3"
  }},
  "eslintConfig": {{
    "root": true,
    "env": {{
      "node": true
    }},
    "extends": [
      "plugin:vue/vue3-essential",
      "eslint:recommended"
    ]
  }},
  "browserslist": [
    "> 1%",
    "last 2 versions",
    "not dead",
    "not ie 11"
  ]
}}
"""
    
    def _generate_vue_index_html(self, form_name: str) -> str:
        """
        Generate index.html content for Vue form.
        
        Args:
            form_name: Name of the form.
            
        Returns:
            index.html content.
        """
        return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="icon" href="<%= BASE_URL %>favicon.ico">
    <title>{form_name}</title>
  </head>
  <body>
    <noscript>
      <strong>We're sorry but {form_name} doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>
    </noscript>
    <div id="app"></div>
    <!-- built files will be auto injected -->
  </body>
</html>
"""
    
    def _generate_vue_main_js(self) -> str:
        """
        Generate main.js content for Vue form.
        
        Returns:
            main.js content.
        """
        return """import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
"""
    
    def _generate_vue_app_vue(self) -> str:
        """
        Generate App.vue content for Vue form.
        
        Returns:
            App.vue content.
        """
        return """<template>
  <div class="app">
    <div class="container">
      <h1>{{ formConfig.form_config.title }}</h1>
      <p class="form-description">{{ formConfig.form_config.description }}</p>
      <Form />
    </div>
  </div>
</template>

<script>
import Form from './components/Form.vue'
import formConfig from './form_config.json'

export default {
  name: 'App',
  components: {
    Form
  },
  data() {
    return {
      formConfig
    }
  }
}
</script>

<style>
/* Form Styles */
.app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f8f9fa;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.container {
  max-width: 800px;
  width: 100%;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  margin-bottom: 20px;
  color: #2c3e50;
  text-align: center;
}

.form-description {
  margin-bottom: 30px;
  text-align: center;
  color: #666;
}

.form-group {
  margin-bottom: 20px;
}

label, .group-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
}

input[type="text"],
input[type="number"],
input[type="date"],
textarea,
select {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s;
}

input[type="text"]:focus,
input[type="number"]:focus,
input[type="date"]:focus,
textarea:focus,
select:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.checkbox-group, .radio-group {
  display: flex;
  flex-direction: column;
}

.checkbox-group label {
  margin-left: 10px;
  display: inline;
}

.radio-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.radio-option {
  display: flex;
  align-items: center;
}

.radio-option label {
  margin-left: 10px;
  margin-bottom: 0;
  font-weight: normal;
}

.range-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

input[type="range"] {
  flex: 1;
}

.range-value {
  min-width: 40px;
  text-align: center;
  font-weight: bold;
  color: #3498db;
}

.help-text {
  display: block;
  margin-top: 5px;
  color: #666;
  font-size: 14px;
}

.error-message {
  color: #e74c3c;
  font-size: 14px;
  margin-top: 5px;
  min-height: 20px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.submit-button, .reset-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button {
  background-color: #3498db;
  color: white;
}

.submit-button:hover {
  background-color: #2980b9;
}

.reset-button {
  background-color: #e74c3c;
  color: white;
}

.reset-button:hover {
  background-color: #c0392b;
}

.form-result {
  margin-top: 30px;
  padding: 15px;
  border-radius: 4px;
}

.form-result.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.form-result.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

/* Responsive styles */
@media (max-width: 768px) {
  .container {
    padding: 15px;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 10px;
  }
  
  .submit-button, .reset-button {
    width: 100%;
  }
}
</style>
"""
    
    def _generate_vue_form_vue(self) -> str:
        """
        Generate Form.vue content for Vue form.
        
        Returns:
            Form.vue content.
        """
        return """<template>
  <div>
    <form @submit.prevent="handleSubmit" @reset.prevent="handleReset">
      <FormField
        v-for="field in formConfig.fields"
        :key="field.id"
        :field="field"
        :value="formData[field.id]"
        :error="errors[field.id]"
        @update:value="updateField(field.id, $event)"
      />
      
      <div class="form-actions">
        <button type="submit" class="submit-button">
          {{ formConfig.form_config.submit_button_text }}
        </button>
        <button type="reset" class="reset-button">
          {{ formConfig.form_config.reset_button_text }}
        </button>
      </div>
    </form>
    
    <div v-if="formResult.message" :class="['form-result', formResult.type]">
      {{ formResult.message }}
    </div>
  </div>
</template>

<script>
import FormField from './FormField.vue'
import formConfig from '../form_config.json'

export default {
  name: 'Form',
  components: {
    FormField
  },
  data() {
    return {
      formConfig,
      formData: {},
      errors: {},
      formResult: { message: '', type: '' }
    }
  },
  methods: {
    updateField(fieldId, value) {
      this.formData[fieldId] = value
      
      // Clear error when field is changed
      if (this.errors[fieldId]) {
        this.errors[fieldId] = ''
      }
    },
    
    validateForm() {
      const newErrors = {}
      let isValid = true
      
      // Process validation rules
      Object.entries(this.formConfig.validation_rules).forEach(([fieldId, rules]) => {
        rules.forEach(rule => {
          const value = this.formData[fieldId]
          
          switch (rule.type) {
            case 'required':
              if (!value && value !== false) {
                newErrors[fieldId] = rule.message
                isValid = false
              }
              break
              
            case 'min_length':
              if (value && value.length < rule.config.min_length) {
                newErrors[fieldId] = rule.message
                isValid = false
              }
              break
              
            case 'max_length':
              if (value && value.length > rule.config.max_length) {
                newErrors[fieldId] = rule.message
                isValid = false
              }
              break
              
            case 'pattern':
              if (value && !new RegExp(rule.config.pattern).test(value)) {
                newErrors[fieldId] = rule.message
                isValid = false
              }
              break
              
            case 'min_value':
              if (value && parseFloat(value) < rule.config.min_value) {
                newErrors[fieldId] = rule.message
                isValid = false
              }
              break
              
            case 'max_value':
              if (value && parseFloat(value) > rule.config.max_value) {
                newErrors[fieldId] = rule.message
                isValid = false
              }
              break
              
            case 'email':
              if (value && !/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value)) {
                newErrors[fieldId] = rule.message
                isValid = false
              }
              break
          }
        })
      })
      
      this.errors = newErrors
      return isValid
    },
    
    handleSubmit() {
      // Reset form result
      this.formResult = { message: '', type: '' }
      
      // Validate form
      if (this.validateForm()) {
        // Here you would typically send the data to a server
        console.log('Form data:', this.formData)
        
        // Show success message
        this.formResult = {
          message: this.formConfig.form_config.success_message,
          type: 'success'
        }
        
        // Optional: Reset form after successful submission
        // this.formData = {}
      } else {
        // Show error message
        this.formResult = {
          message: this.formConfig.form_config.error_message,
          type: 'error'
        }
      }
    },
    
    handleReset() {
      this.formData = {}
      this.errors = {}
      this.formResult = { message: '', type: '' }
    }
  }
}
</script>
"""
    
    def _generate_vue_form_field_vue(self) -> str:
        """
        Generate FormField.vue content for Vue form.
        
        Returns:
            FormField.vue content.
        """
        return """<template>
  <div class="form-group" :class="{ 'checkbox-group': field.type === 'checkbox' }">
    <label v-if="field.type !== 'checkbox'" :for="field.id">{{ field.label }}</label>
    
    <!-- Text input -->
    <input
      v-if="field.type === 'text'"
      type="text"
      :id="field.id"
      :name="field.id"
      :value="value"
      :placeholder="field.placeholder || ''"
      :required="field.required"
      @input="updateValue($event.target.value)"
    />
    
    <!-- Number input -->
    <input
      v-else-if="field.type === 'number'"
      type="number"
      :id="field.id"
      :name="field.id"
      :value="value"
      :placeholder="field.placeholder || ''"
      :min="field.config?.min"
      :max="field.config?.max"
      :step="field.config?.step"
      :required="field.required"
      @input="updateValue($event.target.value)"
    />
    
    <!-- Textarea -->
    <textarea
      v-else-if="field.type === 'textarea'"
      :id="field.id"
      :name="field.id"
      :value="value"
      :placeholder="field.placeholder || ''"
      :rows="field.config?.rows || 4"
      :cols="field.config?.cols || 50"
      :required="field.required"
      @input="updateValue($event.target.value)"
    ></textarea>
    
    <!-- Select -->
    <select
      v-else-if="field.type === 'select'"
      :id="field.id"
      :name="field.id"
      :value="value"
      :required="field.required"
      @change="updateValue($event.target.value)"
    >
      <option v-for="(option, index) in field.options" :key="index" :value="option">
        {{ option }}
      </option>
    </select>
    
    <!-- Checkbox -->
    <template v-else-if="field.type === 'checkbox'">
      <input
        type="checkbox"
        :id="field.id"
        :name="field.id"
        :checked="value === true"
        :required="field.required"
        @change="updateValue($event.target.checked)"
      />
      <label :for="field.id">{{ field.label }}</label>
    </template>
    
    <!-- Radio -->
    <div v-else-if="field.type === 'radio'" class="radio-group">
      <label class="group-label">{{ field.label }}</label>
      <div class="radio-options">
        <div v-for="(option, index) in field.options" :key="index" class="radio-option">
          <input
            type="radio"
            :id="`${field.id}_${index}`"
            :name="field.id"
            :value="option"
            :checked="value === option"
            :required="field.required"
            @change="updateValue(option)"
          />
          <label :for="`${field.id}_${index}`">{{ option }}</label>
        </div>
      </div>
    </div>
    
    <!-- Date -->
    <input
      v-else-if="field.type === 'date'"
      type="date"
      :id="field.id"
      :name="field.id"
      :value="value"
      :min="field.config?.min"
      :max="field.config?.max"
      :required="field.required"
      @input="updateValue($event.target.value)"
    />
    
    <!-- File -->
    <input
      v-else-if="field.type === 'file'"
      type="file"
      :id="field.id"
      :name="field.id"
      :accept="field.config?.accept"
      :multiple="field.config?.multiple"
      :required="field.required"
      @change="updateValue($event.target.files)"
    />
    
    <!-- Range -->
    <div v-else-if="field.type === 'range'" class="range-container">
      <input
        type="range"
        :id="field.id"
        :name="field.id"
        :value="value || field.config?.min || 0"
        :min="field.config?.min || 0"
        :max="field.config?.max || 100"
        :step="field.config?.step || 1"
        :required="field.required"
        @input="updateValue($event.target.value)"
      />
      <span class="range-value">{{ value || field.config?.min || 0 }}</span>
    </div>
    
    <!-- Unsupported field type -->
    <div v-else>Unsupported field type: {{ field.type }}</div>
    
    <!-- Help text and error message -->
    <small v-if="field.help_text" class="help-text">{{ field.help_text }}</small>
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script>
export default {
  name: 'FormField',
  props: {
    field: {
      type: Object,
      required: true
    },
    value: {
      type: [String, Number, Boolean, Array],
      default: ''
    },
    error: {
      type: String,
      default: ''
    }
  },
  methods: {
    updateValue(value) {
      this.$emit('update:value', value)
    }
  }
}
</script>
"""
    
    def _generate_vue_readme_content(self, form_name: str) -> str:
        """
        Generate README.md content for Vue form.
        
        Args:
            form_name: Name of the form.
            
        Returns:
            README.md content.
        """
        return f"""
# {form_name}

This is a Vue.js form application generated by SBYB UI Generator.

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   npm install
   ```

## Usage

### Development

```
npm run serve
```

The application will be available at http://localhost:8080

### Production Build

```
npm run build
```

This will create a production-ready build in the `dist` folder.

## Features

- Responsive design that works on desktop and mobile devices
- Client-side form validation
- Interactive form elements
- Customizable styling

## Structure

- `src/App.vue`: Main application component
- `src/components/Form.vue`: Form component with validation logic
- `src/components/FormField.vue`: Reusable form field component
- `src/form_config.json`: Configuration file for the form

## Customization

You can customize the form by editing the Vue components and CSS styles. The form configuration is stored in `src/form_config.json`.

## Integration

To integrate this form with a backend:

1. Modify the form submission handler in `src/components/Form.vue` to send the form data to your server
2. Implement server-side validation and processing
3. Update the success and error messages accordingly
"""
