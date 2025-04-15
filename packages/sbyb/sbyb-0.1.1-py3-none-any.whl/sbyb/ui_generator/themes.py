"""
Theme manager for SBYB UI Generator.

This module provides a theme manager for UI Generator
to manage and apply themes for different UI frameworks.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import shutil
import tempfile
import colorsys

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import UIGenerationError


class ThemeManager(SBYBComponent):
    """
    Theme manager for UI Generator.
    
    This component provides a theme manager for UI Generator
    to manage and apply themes for different UI frameworks.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the theme manager.
        
        Args:
            config: Configuration dictionary for the theme manager.
        """
        super().__init__(config)
        self.themes = {}
        self.theme_dirs = {}
        self._setup_theme_dirs()
        self._load_default_themes()
    
    def _setup_theme_dirs(self) -> None:
        """
        Set up theme directories.
        """
        # Default theme directory
        default_theme_dir = os.path.join(os.path.dirname(__file__), "themes")
        
        # Create theme directory if it doesn't exist
        if not os.path.exists(default_theme_dir):
            os.makedirs(default_theme_dir)
        
        # Set up theme directories for each framework
        for framework in ["streamlit", "dash", "flask", "html", "react", "vue"]:
            framework_dir = os.path.join(default_theme_dir, framework)
            if not os.path.exists(framework_dir):
                os.makedirs(framework_dir)
            self.theme_dirs[framework] = framework_dir
    
    def _load_default_themes(self) -> None:
        """
        Load default themes.
        """
        # Default themes for all frameworks
        self.register_theme(
            "light",
            "Light Theme",
            "all",
            {
                "description": "A light theme with blue accents.",
                "colors": {
                    "primary": "#1E88E5",
                    "secondary": "#26A69A",
                    "background": "#FFFFFF",
                    "surface": "#F5F5F5",
                    "text": "#212121",
                    "text_secondary": "#757575",
                    "success": "#4CAF50",
                    "warning": "#FFC107",
                    "error": "#F44336",
                    "info": "#2196F3"
                },
                "typography": {
                    "font_family": "'Roboto', 'Helvetica', 'Arial', sans-serif",
                    "font_size": "16px",
                    "heading_font_family": "'Roboto', 'Helvetica', 'Arial', sans-serif",
                    "heading_font_weight": "500",
                    "line_height": "1.5"
                },
                "spacing": {
                    "unit": "8px",
                    "small": "8px",
                    "medium": "16px",
                    "large": "24px",
                    "xlarge": "32px"
                },
                "border_radius": {
                    "small": "4px",
                    "medium": "8px",
                    "large": "16px",
                    "circle": "50%"
                },
                "shadows": {
                    "none": "none",
                    "small": "0 2px 4px rgba(0, 0, 0, 0.1)",
                    "medium": "0 4px 8px rgba(0, 0, 0, 0.1)",
                    "large": "0 8px 16px rgba(0, 0, 0, 0.1)"
                }
            }
        )
        
        self.register_theme(
            "dark",
            "Dark Theme",
            "all",
            {
                "description": "A dark theme with blue accents.",
                "colors": {
                    "primary": "#90CAF9",
                    "secondary": "#80CBC4",
                    "background": "#121212",
                    "surface": "#1E1E1E",
                    "text": "#FFFFFF",
                    "text_secondary": "#B0B0B0",
                    "success": "#81C784",
                    "warning": "#FFD54F",
                    "error": "#E57373",
                    "info": "#64B5F6"
                },
                "typography": {
                    "font_family": "'Roboto', 'Helvetica', 'Arial', sans-serif",
                    "font_size": "16px",
                    "heading_font_family": "'Roboto', 'Helvetica', 'Arial', sans-serif",
                    "heading_font_weight": "500",
                    "line_height": "1.5"
                },
                "spacing": {
                    "unit": "8px",
                    "small": "8px",
                    "medium": "16px",
                    "large": "24px",
                    "xlarge": "32px"
                },
                "border_radius": {
                    "small": "4px",
                    "medium": "8px",
                    "large": "16px",
                    "circle": "50%"
                },
                "shadows": {
                    "none": "none",
                    "small": "0 2px 4px rgba(0, 0, 0, 0.2)",
                    "medium": "0 4px 8px rgba(0, 0, 0, 0.2)",
                    "large": "0 8px 16px rgba(0, 0, 0, 0.2)"
                }
            }
        )
        
        self.register_theme(
            "material",
            "Material Design",
            "all",
            {
                "description": "A theme based on Material Design guidelines.",
                "colors": {
                    "primary": "#6200EE",
                    "secondary": "#03DAC6",
                    "background": "#FFFFFF",
                    "surface": "#FFFFFF",
                    "text": "#000000",
                    "text_secondary": "#666666",
                    "success": "#4CAF50",
                    "warning": "#FB8C00",
                    "error": "#B00020",
                    "info": "#2196F3"
                },
                "typography": {
                    "font_family": "'Roboto', 'Helvetica', 'Arial', sans-serif",
                    "font_size": "16px",
                    "heading_font_family": "'Roboto', 'Helvetica', 'Arial', sans-serif",
                    "heading_font_weight": "500",
                    "line_height": "1.5"
                },
                "spacing": {
                    "unit": "8px",
                    "small": "8px",
                    "medium": "16px",
                    "large": "24px",
                    "xlarge": "32px"
                },
                "border_radius": {
                    "small": "4px",
                    "medium": "8px",
                    "large": "16px",
                    "circle": "50%"
                },
                "shadows": {
                    "none": "none",
                    "small": "0 2px 1px -1px rgba(0,0,0,.2), 0 1px 1px 0 rgba(0,0,0,.14), 0 1px 3px 0 rgba(0,0,0,.12)",
                    "medium": "0 3px 3px -2px rgba(0,0,0,.2), 0 3px 4px 0 rgba(0,0,0,.14), 0 1px 8px 0 rgba(0,0,0,.12)",
                    "large": "0 5px 5px -3px rgba(0,0,0,.2), 0 8px 10px 1px rgba(0,0,0,.14), 0 3px 14px 2px rgba(0,0,0,.12)"
                }
            }
        )
        
        self.register_theme(
            "minimal",
            "Minimal",
            "all",
            {
                "description": "A minimal theme with clean aesthetics.",
                "colors": {
                    "primary": "#000000",
                    "secondary": "#666666",
                    "background": "#FFFFFF",
                    "surface": "#FAFAFA",
                    "text": "#000000",
                    "text_secondary": "#666666",
                    "success": "#4CAF50",
                    "warning": "#FFC107",
                    "error": "#F44336",
                    "info": "#2196F3"
                },
                "typography": {
                    "font_family": "'Inter', 'Helvetica', 'Arial', sans-serif",
                    "font_size": "16px",
                    "heading_font_family": "'Inter', 'Helvetica', 'Arial', sans-serif",
                    "heading_font_weight": "600",
                    "line_height": "1.5"
                },
                "spacing": {
                    "unit": "8px",
                    "small": "8px",
                    "medium": "16px",
                    "large": "24px",
                    "xlarge": "32px"
                },
                "border_radius": {
                    "small": "2px",
                    "medium": "4px",
                    "large": "8px",
                    "circle": "50%"
                },
                "shadows": {
                    "none": "none",
                    "small": "0 1px 2px rgba(0, 0, 0, 0.05)",
                    "medium": "0 2px 4px rgba(0, 0, 0, 0.05)",
                    "large": "0 4px 8px rgba(0, 0, 0, 0.05)"
                }
            }
        )
        
        # Streamlit-specific themes
        self.register_theme(
            "streamlit_default",
            "Streamlit Default",
            "streamlit",
            {
                "description": "The default Streamlit theme.",
                "config": {
                    "primaryColor": "#FF4B4B",
                    "backgroundColor": "#FFFFFF",
                    "secondaryBackgroundColor": "#F0F2F6",
                    "textColor": "#262730",
                    "font": "sans serif"
                }
            }
        )
        
        self.register_theme(
            "streamlit_dark",
            "Streamlit Dark",
            "streamlit",
            {
                "description": "A dark theme for Streamlit.",
                "config": {
                    "primaryColor": "#FF4B4B",
                    "backgroundColor": "#0E1117",
                    "secondaryBackgroundColor": "#262730",
                    "textColor": "#FAFAFA",
                    "font": "sans serif"
                }
            }
        )
        
        # Dash-specific themes
        self.register_theme(
            "dash_default",
            "Dash Default",
            "dash",
            {
                "description": "The default Dash theme.",
                "config": {
                    "external_stylesheets": ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
                }
            }
        )
        
        self.register_theme(
            "dash_bootstrap",
            "Dash Bootstrap",
            "dash",
            {
                "description": "A Bootstrap theme for Dash.",
                "config": {
                    "external_stylesheets": ["https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"]
                }
            }
        )
        
        # React-specific themes
        self.register_theme(
            "react_material_ui",
            "Material UI",
            "react",
            {
                "description": "Material UI theme for React.",
                "config": {
                    "palette": {
                        "primary": {
                            "main": "#1976d2"
                        },
                        "secondary": {
                            "main": "#dc004e"
                        }
                    },
                    "typography": {
                        "fontFamily": "'Roboto', 'Helvetica', 'Arial', sans-serif"
                    }
                }
            }
        )
        
        # Vue-specific themes
        self.register_theme(
            "vue_vuetify",
            "Vuetify",
            "vue",
            {
                "description": "Vuetify theme for Vue.",
                "config": {
                    "theme": {
                        "dark": False,
                        "themes": {
                            "light": {
                                "primary": "#1976D2",
                                "secondary": "#424242",
                                "accent": "#82B1FF",
                                "error": "#FF5252",
                                "info": "#2196F3",
                                "success": "#4CAF50",
                                "warning": "#FFC107"
                            }
                        }
                    }
                }
            }
        )
    
    def register_theme(self, theme_id: str, theme_name: str,
                      framework: str, config: Dict[str, Any]) -> None:
        """
        Register a theme in the manager.
        
        Args:
            theme_id: Unique identifier for the theme.
            theme_name: Display name for the theme.
            framework: Framework to which the theme belongs ('all' for universal themes).
            config: Configuration for the theme.
        """
        if theme_id in self.themes:
            raise UIGenerationError(f"Theme ID '{theme_id}' already exists.")
        
        if framework != "all" and framework not in self.theme_dirs:
            raise UIGenerationError(f"Framework '{framework}' is not supported.")
        
        theme = {
            "id": theme_id,
            "name": theme_name,
            "framework": framework,
            "config": config
        }
        
        self.themes[theme_id] = theme
    
    def get_theme(self, theme_id: str) -> Dict[str, Any]:
        """
        Get a theme by ID.
        
        Args:
            theme_id: ID of the theme to get.
            
        Returns:
            Theme configuration.
        """
        if theme_id not in self.themes:
            raise UIGenerationError(f"Theme ID '{theme_id}' does not exist.")
        
        return self.themes[theme_id]
    
    def get_themes_by_framework(self, framework: str) -> List[Dict[str, Any]]:
        """
        Get all themes for a framework.
        
        Args:
            framework: Framework to get themes for.
            
        Returns:
            List of themes for the framework.
        """
        if framework != "all" and framework not in self.theme_dirs:
            raise UIGenerationError(f"Framework '{framework}' is not supported.")
        
        # Include universal themes and framework-specific themes
        return [theme for theme in self.themes.values() 
                if theme["framework"] == framework or theme["framework"] == "all"]
    
    def get_all_themes(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all themes.
        
        Returns:
            Dictionary of all themes.
        """
        return self.themes
    
    def apply_theme_to_css(self, theme_id: str, css_content: str) -> str:
        """
        Apply a theme to CSS content.
        
        Args:
            theme_id: ID of the theme to apply.
            css_content: CSS content to apply the theme to.
            
        Returns:
            CSS content with theme applied.
        """
        theme = self.get_theme(theme_id)
        
        # Only apply universal themes
        if theme["framework"] != "all":
            return css_content
        
        # Get theme colors
        colors = theme["config"]["colors"]
        typography = theme["config"]["typography"]
        spacing = theme["config"]["spacing"]
        border_radius = theme["config"]["border_radius"]
        shadows = theme["config"]["shadows"]
        
        # Replace CSS variables
        css_with_vars = ":root {\n"
        
        # Add color variables
        for color_name, color_value in colors.items():
            css_with_vars += f"  --color-{color_name}: {color_value};\n"
        
        # Add typography variables
        for typo_name, typo_value in typography.items():
            css_with_vars += f"  --typography-{typo_name}: {typo_value};\n"
        
        # Add spacing variables
        for spacing_name, spacing_value in spacing.items():
            css_with_vars += f"  --spacing-{spacing_name}: {spacing_value};\n"
        
        # Add border radius variables
        for radius_name, radius_value in border_radius.items():
            css_with_vars += f"  --border-radius-{radius_name}: {radius_value};\n"
        
        # Add shadow variables
        for shadow_name, shadow_value in shadows.items():
            css_with_vars += f"  --shadow-{shadow_name}: {shadow_value};\n"
        
        css_with_vars += "}\n\n"
        
        # Add the original CSS content
        css_with_vars += css_content
        
        return css_with_vars
    
    def apply_theme_to_streamlit(self, theme_id: str) -> Dict[str, Any]:
        """
        Apply a theme to Streamlit.
        
        Args:
            theme_id: ID of the theme to apply.
            
        Returns:
            Streamlit theme configuration.
        """
        theme = self.get_theme(theme_id)
        
        # If it's a Streamlit-specific theme, return its config directly
        if theme["framework"] == "streamlit":
            return theme["config"]["config"]
        
        # If it's a universal theme, convert it to Streamlit format
        if theme["framework"] == "all":
            colors = theme["config"]["colors"]
            typography = theme["config"]["typography"]
            
            return {
                "primaryColor": colors["primary"],
                "backgroundColor": colors["background"],
                "secondaryBackgroundColor": colors["surface"],
                "textColor": colors["text"],
                "font": typography["font_family"].split(",")[0].strip("'\"")
            }
        
        # If it's not a Streamlit or universal theme, raise an error
        raise UIGenerationError(f"Theme '{theme_id}' is not compatible with Streamlit.")
    
    def apply_theme_to_dash(self, theme_id: str) -> Dict[str, Any]:
        """
        Apply a theme to Dash.
        
        Args:
            theme_id: ID of the theme to apply.
            
        Returns:
            Dash theme configuration.
        """
        theme = self.get_theme(theme_id)
        
        # If it's a Dash-specific theme, return its config directly
        if theme["framework"] == "dash":
            return theme["config"]["config"]
        
        # If it's a universal theme, convert it to Dash format
        if theme["framework"] == "all":
            colors = theme["config"]["colors"]
            
            return {
                "external_stylesheets": [],
                "colors": {
                    "primary": colors["primary"],
                    "secondary": colors["secondary"],
                    "background": colors["background"],
                    "surface": colors["surface"],
                    "text": colors["text"],
                    "text-secondary": colors["text_secondary"],
                    "success": colors["success"],
                    "warning": colors["warning"],
                    "error": colors["error"],
                    "info": colors["info"]
                }
            }
        
        # If it's not a Dash or universal theme, raise an error
        raise UIGenerationError(f"Theme '{theme_id}' is not compatible with Dash.")
    
    def apply_theme_to_react(self, theme_id: str) -> Dict[str, Any]:
        """
        Apply a theme to React.
        
        Args:
            theme_id: ID of the theme to apply.
            
        Returns:
            React theme configuration.
        """
        theme = self.get_theme(theme_id)
        
        # If it's a React-specific theme, return its config directly
        if theme["framework"] == "react":
            return theme["config"]["config"]
        
        # If it's a universal theme, convert it to React format
        if theme["framework"] == "all":
            colors = theme["config"]["colors"]
            typography = theme["config"]["typography"]
            spacing = theme["config"]["spacing"]
            border_radius = theme["config"]["border_radius"]
            shadows = theme["config"]["shadows"]
            
            return {
                "palette": {
                    "primary": {
                        "main": colors["primary"]
                    },
                    "secondary": {
                        "main": colors["secondary"]
                    },
                    "background": {
                        "default": colors["background"],
                        "paper": colors["surface"]
                    },
                    "text": {
                        "primary": colors["text"],
                        "secondary": colors["text_secondary"]
                    },
                    "success": {
                        "main": colors["success"]
                    },
                    "warning": {
                        "main": colors["warning"]
                    },
                    "error": {
                        "main": colors["error"]
                    },
                    "info": {
                        "main": colors["info"]
                    }
                },
                "typography": {
                    "fontFamily": typography["font_family"],
                    "fontSize": typography["font_size"],
                    "lineHeight": typography["line_height"]
                },
                "shape": {
                    "borderRadius": border_radius["medium"]
                },
                "spacing": spacing["unit"],
                "shadows": [
                    "none",
                    shadows["small"],
                    shadows["medium"],
                    shadows["large"]
                ]
            }
        
        # If it's not a React or universal theme, raise an error
        raise UIGenerationError(f"Theme '{theme_id}' is not compatible with React.")
    
    def apply_theme_to_vue(self, theme_id: str) -> Dict[str, Any]:
        """
        Apply a theme to Vue.
        
        Args:
            theme_id: ID of the theme to apply.
            
        Returns:
            Vue theme configuration.
        """
        theme = self.get_theme(theme_id)
        
        # If it's a Vue-specific theme, return its config directly
        if theme["framework"] == "vue":
            return theme["config"]["config"]
        
        # If it's a universal theme, convert it to Vue format
        if theme["framework"] == "all":
            colors = theme["config"]["colors"]
            
            return {
                "theme": {
                    "dark": colors["background"].lower() == "#121212",
                    "themes": {
                        "light": {
                            "primary": colors["primary"],
                            "secondary": colors["secondary"],
                            "accent": colors["info"],
                            "error": colors["error"],
                            "warning": colors["warning"],
                            "info": colors["info"],
                            "success": colors["success"]
                        },
                        "dark": {
                            "primary": colors["primary"],
                            "secondary": colors["secondary"],
                            "accent": colors["info"],
                            "error": colors["error"],
                            "warning": colors["warning"],
                            "info": colors["info"],
                            "success": colors["success"]
                        }
                    }
                }
            }
        
        # If it's not a Vue or universal theme, raise an error
        raise UIGenerationError(f"Theme '{theme_id}' is not compatible with Vue.")
    
    def generate_theme_from_color(self, primary_color: str, is_dark: bool = False) -> Dict[str, Any]:
        """
        Generate a theme from a primary color.
        
        Args:
            primary_color: Primary color in hex format.
            is_dark: Whether to generate a dark theme.
            
        Returns:
            Generated theme configuration.
        """
        # Convert hex to RGB
        primary_hex = primary_color.lstrip("#")
        primary_rgb = tuple(int(primary_hex[i:i+2], 16) for i in (0, 2, 4))
        
        # Convert RGB to HSL
        r, g, b = [x / 255.0 for x in primary_rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        
        # Generate secondary color (complementary)
        h_secondary = (h + 0.5) % 1.0
        r_s, g_s, b_s = colorsys.hls_to_rgb(h_secondary, l, s)
        secondary_rgb = tuple(int(x * 255) for x in (r_s, g_s, b_s))
        secondary_color = "#{:02x}{:02x}{:02x}".format(*secondary_rgb)
        
        # Generate success color (green hue)
        h_success = 0.33  # Green
        r_success, g_success, b_success = colorsys.hls_to_rgb(h_success, 0.5, 0.5)
        success_rgb = tuple(int(x * 255) for x in (r_success, g_success, b_success))
        success_color = "#{:02x}{:02x}{:02x}".format(*success_rgb)
        
        # Generate warning color (yellow/orange hue)
        h_warning = 0.12  # Yellow/Orange
        r_warning, g_warning, b_warning = colorsys.hls_to_rgb(h_warning, 0.5, 0.5)
        warning_rgb = tuple(int(x * 255) for x in (r_warning, g_warning, b_warning))
        warning_color = "#{:02x}{:02x}{:02x}".format(*warning_rgb)
        
        # Generate error color (red hue)
        h_error = 0.0  # Red
        r_error, g_error, b_error = colorsys.hls_to_rgb(h_error, 0.5, 0.5)
        error_rgb = tuple(int(x * 255) for x in (r_error, g_error, b_error))
        error_color = "#{:02x}{:02x}{:02x}".format(*error_rgb)
        
        # Generate info color (blue hue)
        h_info = 0.6  # Blue
        r_info, g_info, b_info = colorsys.hls_to_rgb(h_info, 0.5, 0.5)
        info_rgb = tuple(int(x * 255) for x in (r_info, g_info, b_info))
        info_color = "#{:02x}{:02x}{:02x}".format(*info_rgb)
        
        # Set background and text colors based on dark mode
        if is_dark:
            background_color = "#121212"
            surface_color = "#1E1E1E"
            text_color = "#FFFFFF"
            text_secondary_color = "#B0B0B0"
        else:
            background_color = "#FFFFFF"
            surface_color = "#F5F5F5"
            text_color = "#212121"
            text_secondary_color = "#757575"
        
        # Create theme configuration
        theme_config = {
            "colors": {
                "primary": primary_color,
                "secondary": secondary_color,
                "background": background_color,
                "surface": surface_color,
                "text": text_color,
                "text_secondary": text_secondary_color,
                "success": success_color,
                "warning": warning_color,
                "error": error_color,
                "info": info_color
            },
            "typography": {
                "font_family": "'Roboto', 'Helvetica', 'Arial', sans-serif",
                "font_size": "16px",
                "heading_font_family": "'Roboto', 'Helvetica', 'Arial', sans-serif",
                "heading_font_weight": "500",
                "line_height": "1.5"
            },
            "spacing": {
                "unit": "8px",
                "small": "8px",
                "medium": "16px",
                "large": "24px",
                "xlarge": "32px"
            },
            "border_radius": {
                "small": "4px",
                "medium": "8px",
                "large": "16px",
                "circle": "50%"
            },
            "shadows": {
                "none": "none",
                "small": "0 2px 4px rgba(0, 0, 0, 0.1)",
                "medium": "0 4px 8px rgba(0, 0, 0, 0.1)",
                "large": "0 8px 16px rgba(0, 0, 0, 0.1)"
            }
        }
        
        return theme_config
    
    def create_custom_theme(self, theme_id: str, theme_name: str,
                           framework: str, config: Dict[str, Any],
                           description: str = "") -> None:
        """
        Create a custom theme.
        
        Args:
            theme_id: Unique identifier for the theme.
            theme_name: Display name for the theme.
            framework: Framework to which the theme belongs.
            config: Theme configuration.
            description: Description of the theme.
        """
        theme_config = {
            "description": description,
        }
        
        if framework == "all":
            # Validate universal theme config
            required_keys = ["colors", "typography", "spacing", "border_radius", "shadows"]
            for key in required_keys:
                if key not in config:
                    raise UIGenerationError(f"Missing required key '{key}' in universal theme config.")
            
            theme_config.update(config)
        else:
            # Framework-specific theme
            theme_config["config"] = config
        
        self.register_theme(theme_id, theme_name, framework, theme_config)
    
    def save_theme(self, theme_id: str) -> None:
        """
        Save a theme to disk.
        
        Args:
            theme_id: ID of the theme to save.
        """
        theme = self.get_theme(theme_id)
        
        # Determine theme directory
        if theme["framework"] == "all":
            # Save universal theme to all framework directories
            for framework, framework_dir in self.theme_dirs.items():
                theme_dir = os.path.join(framework_dir, theme_id)
                if not os.path.exists(theme_dir):
                    os.makedirs(theme_dir)
                
                # Save theme metadata
                metadata = {
                    "id": theme["id"],
                    "name": theme["name"],
                    "framework": "all",
                    "description": theme["config"]["description"]
                }
                
                with open(os.path.join(theme_dir, "metadata.json"), "w") as f:
                    json.dump(metadata, f, indent=2)
                
                # Save theme config
                with open(os.path.join(theme_dir, "config.json"), "w") as f:
                    json.dump(theme["config"], f, indent=2)
        else:
            # Save framework-specific theme
            theme_dir = os.path.join(self.theme_dirs[theme["framework"]], theme_id)
            if not os.path.exists(theme_dir):
                os.makedirs(theme_dir)
            
            # Save theme metadata
            metadata = {
                "id": theme["id"],
                "name": theme["name"],
                "framework": theme["framework"],
                "description": theme["config"]["description"]
            }
            
            with open(os.path.join(theme_dir, "metadata.json"), "w") as f:
                json.dump(metadata, f, indent=2)
            
            # Save theme config
            with open(os.path.join(theme_dir, "config.json"), "w") as f:
                json.dump(theme["config"], f, indent=2)
    
    def load_theme_from_disk(self, framework: str, theme_id: str) -> None:
        """
        Load a theme from disk.
        
        Args:
            framework: Framework to which the theme belongs.
            theme_id: ID of the theme to load.
        """
        theme_dir = os.path.join(self.theme_dirs[framework], theme_id)
        
        if not os.path.exists(theme_dir):
            raise UIGenerationError(f"Theme directory '{theme_dir}' does not exist.")
        
        # Load theme metadata
        with open(os.path.join(theme_dir, "metadata.json"), "r") as f:
            metadata = json.load(f)
        
        # Load theme config
        with open(os.path.join(theme_dir, "config.json"), "r") as f:
            config = json.load(f)
        
        # Register theme
        self.register_theme(
            metadata["id"],
            metadata["name"],
            metadata["framework"],
            config
        )
    
    def export_theme(self, theme_id: str, output_path: str) -> str:
        """
        Export a theme to a JSON file.
        
        Args:
            theme_id: ID of the theme to export.
            output_path: Path to save the exported theme.
            
        Returns:
            Path to the exported theme.
        """
        theme = self.get_theme(theme_id)
        
        # Create theme export data
        export_data = {
            "id": theme["id"],
            "name": theme["name"],
            "framework": theme["framework"],
            "config": theme["config"]
        }
        
        # Save to JSON file
        json_path = output_path if output_path.endswith(".json") else f"{output_path}.json"
        with open(json_path, "w") as f:
            json.dump(export_data, f, indent=2)
        
        return json_path
    
    def import_theme(self, json_path: str) -> str:
        """
        Import a theme from a JSON file.
        
        Args:
            json_path: Path to the JSON file.
            
        Returns:
            ID of the imported theme.
        """
        # Load theme from JSON file
        with open(json_path, "r") as f:
            theme_data = json.load(f)
        
        # Validate theme data
        required_keys = ["id", "name", "framework", "config"]
        for key in required_keys:
            if key not in theme_data:
                raise UIGenerationError(f"Missing required key '{key}' in theme data.")
        
        # Register theme
        self.register_theme(
            theme_data["id"],
            theme_data["name"],
            theme_data["framework"],
            theme_data["config"]
        )
        
        return theme_data["id"]
    
    def generate_css_variables(self, theme_id: str) -> str:
        """
        Generate CSS variables for a theme.
        
        Args:
            theme_id: ID of the theme.
            
        Returns:
            CSS variables string.
        """
        theme = self.get_theme(theme_id)
        
        # Only generate variables for universal themes
        if theme["framework"] != "all":
            raise UIGenerationError(f"Theme '{theme_id}' is not a universal theme.")
        
        # Get theme config
        colors = theme["config"]["colors"]
        typography = theme["config"]["typography"]
        spacing = theme["config"]["spacing"]
        border_radius = theme["config"]["border_radius"]
        shadows = theme["config"]["shadows"]
        
        # Generate CSS variables
        css_vars = ":root {\n"
        
        # Add color variables
        for color_name, color_value in colors.items():
            css_vars += f"  --color-{color_name}: {color_value};\n"
        
        # Add typography variables
        for typo_name, typo_value in typography.items():
            css_vars += f"  --typography-{typo_name}: {typo_value};\n"
        
        # Add spacing variables
        for spacing_name, spacing_value in spacing.items():
            css_vars += f"  --spacing-{spacing_name}: {spacing_value};\n"
        
        # Add border radius variables
        for radius_name, radius_value in border_radius.items():
            css_vars += f"  --border-radius-{radius_name}: {radius_value};\n"
        
        # Add shadow variables
        for shadow_name, shadow_value in shadows.items():
            css_vars += f"  --shadow-{shadow_name}: {shadow_value};\n"
        
        css_vars += "}\n"
        
        return css_vars
    
    def generate_theme_preview(self, theme_id: str, output_path: str) -> str:
        """
        Generate a preview HTML file for a theme.
        
        Args:
            theme_id: ID of the theme.
            output_path: Path to save the preview file.
            
        Returns:
            Path to the preview file.
        """
        theme = self.get_theme(theme_id)
        
        # Only generate preview for universal themes
        if theme["framework"] != "all":
            raise UIGenerationError(f"Theme '{theme_id}' is not a universal theme.")
        
        # Get theme config
        colors = theme["config"]["colors"]
        typography = theme["config"]["typography"]
        spacing = theme["config"]["spacing"]
        border_radius = theme["config"]["border_radius"]
        shadows = theme["config"]["shadows"]
        
        # Generate CSS variables
        css_vars = self.generate_css_variables(theme_id)
        
        # Generate preview HTML
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Theme Preview: {theme["name"]}</title>
    <style>
        {css_vars}
        
        body {{
            font-family: var(--typography-font_family);
            font-size: var(--typography-font_size);
            line-height: var(--typography-line_height);
            color: var(--color-text);
            background-color: var(--color-background);
            margin: 0;
            padding: 0;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: var(--spacing-large);
        }}
        
        header {{
            background-color: var(--color-primary);
            color: white;
            padding: var(--spacing-large);
            margin-bottom: var(--spacing-large);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--typography-heading_font_family);
            font-weight: var(--typography-heading_font_weight);
        }}
        
        .color-palette {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: var(--spacing-medium);
            margin-bottom: var(--spacing-large);
        }}
        
        .color-swatch {{
            height: 100px;
            border-radius: var(--border-radius-medium);
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: var(--spacing-small);
            color: white;
            box-shadow: var(--shadow-small);
        }}
        
        .typography-sample {{
            margin-bottom: var(--spacing-large);
        }}
        
        .component-samples {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: var(--spacing-large);
            margin-bottom: var(--spacing-large);
        }}
        
        .component-sample {{
            background-color: var(--color-surface);
            border-radius: var(--border-radius-medium);
            padding: var(--spacing-medium);
            box-shadow: var(--shadow-medium);
        }}
        
        .button {{
            background-color: var(--color-primary);
            color: white;
            border: none;
            border-radius: var(--border-radius-small);
            padding: var(--spacing-small) var(--spacing-medium);
            font-family: var(--typography-font_family);
            font-size: var(--typography-font_size);
            cursor: pointer;
        }}
        
        .button.secondary {{
            background-color: var(--color-secondary);
        }}
        
        .button.success {{
            background-color: var(--color-success);
        }}
        
        .button.warning {{
            background-color: var(--color-warning);
        }}
        
        .button.error {{
            background-color: var(--color-error);
        }}
        
        .button.info {{
            background-color: var(--color-info);
        }}
        
        .input {{
            width: 100%;
            padding: var(--spacing-small);
            border: 1px solid var(--color-text_secondary);
            border-radius: var(--border-radius-small);
            font-family: var(--typography-font_family);
            font-size: var(--typography-font_size);
            margin-bottom: var(--spacing-small);
        }}
        
        .card {{
            background-color: var(--color-surface);
            border-radius: var(--border-radius-medium);
            padding: var(--spacing-medium);
            box-shadow: var(--shadow-medium);
        }}
        
        .shadow-samples {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: var(--spacing-medium);
            margin-bottom: var(--spacing-large);
        }}
        
        .shadow-sample {{
            height: 100px;
            background-color: var(--color-surface);
            border-radius: var(--border-radius-medium);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Theme Preview: {theme["name"]}</h1>
            <p>{theme["config"]["description"]}</p>
        </div>
    </header>
    
    <div class="container">
        <h2>Color Palette</h2>
        <div class="color-palette">
"""
        
        # Add color swatches
        for color_name, color_value in colors.items():
            html += f"""
            <div class="color-swatch" style="background-color: {color_value};">
                <div>{color_name}</div>
                <div>{color_value}</div>
            </div>
"""
        
        html += """
        </div>
        
        <h2>Typography</h2>
        <div class="typography-sample">
            <h1>Heading 1</h1>
            <h2>Heading 2</h2>
            <h3>Heading 3</h3>
            <h4>Heading 4</h4>
            <h5>Heading 5</h5>
            <h6>Heading 6</h6>
            <p>This is a paragraph of text. It demonstrates the body text styling of this theme.</p>
            <p><strong>Bold text</strong> and <em>italic text</em> are also styled appropriately.</p>
            <p><a href="#">This is a link</a> that demonstrates the link styling.</p>
        </div>
        
        <h2>Components</h2>
        <div class="component-samples">
            <div class="component-sample">
                <h3>Buttons</h3>
                <button class="button">Primary Button</button>
                <button class="button secondary">Secondary Button</button>
                <button class="button success">Success Button</button>
                <button class="button warning">Warning Button</button>
                <button class="button error">Error Button</button>
                <button class="button info">Info Button</button>
            </div>
            
            <div class="component-sample">
                <h3>Form Elements</h3>
                <input type="text" class="input" placeholder="Text input">
                <input type="number" class="input" placeholder="Number input">
                <input type="date" class="input">
                <select class="input">
                    <option>Option 1</option>
                    <option>Option 2</option>
                    <option>Option 3</option>
                </select>
            </div>
            
            <div class="component-sample">
                <h3>Card</h3>
                <div class="card">
                    <h4>Card Title</h4>
                    <p>This is a card component that demonstrates the card styling of this theme.</p>
                    <button class="button">Action</button>
                </div>
            </div>
        </div>
        
        <h2>Shadows</h2>
        <div class="shadow-samples">
            <div class="shadow-sample" style="box-shadow: var(--shadow-none);">
                <p>None</p>
            </div>
            <div class="shadow-sample" style="box-shadow: var(--shadow-small);">
                <p>Small</p>
            </div>
            <div class="shadow-sample" style="box-shadow: var(--shadow-medium);">
                <p>Medium</p>
            </div>
            <div class="shadow-sample" style="box-shadow: var(--shadow-large);">
                <p>Large</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
        
        # Save preview HTML
        html_path = output_path if output_path.endswith(".html") else f"{output_path}.html"
        with open(html_path, "w") as f:
            f.write(html)
        
        return html_path
