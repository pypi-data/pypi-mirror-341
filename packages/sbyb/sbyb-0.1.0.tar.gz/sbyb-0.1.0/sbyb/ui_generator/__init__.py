"""
UI Generator module for SBYB.

This module provides components for generating user interfaces
for machine learning models without writing code.
"""

from sbyb.ui_generator.dashboard import DashboardGenerator
from sbyb.ui_generator.form import FormGenerator
from sbyb.ui_generator.components import ComponentLibrary
from sbyb.ui_generator.templates import TemplateManager
from sbyb.ui_generator.theme import ThemeManager

__all__ = [
    'DashboardGenerator',
    'FormGenerator',
    'ComponentLibrary',
    'TemplateManager',
    'ThemeManager',
]
