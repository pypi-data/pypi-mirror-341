"""
Component registry for SBYB.

This module provides a registry system for managing and accessing components
throughout the SBYB library, enabling the plugin architecture.
"""

from typing import Any, Dict, List, Optional, Type

from sbyb.core.base import SBYBComponent, Plugin
from sbyb.core.exceptions import PluginError


class Registry:
    """Registry for SBYB components and plugins."""
    
    def __init__(self):
        """Initialize the registry."""
        self._components: Dict[str, Dict[str, Type[SBYBComponent]]] = {
            'preprocessor': {},
            'model': {},
            'evaluator': {},
            'deployer': {},
            'ui_generator': {},
            'task_detector': {},
            'plugin': {}
        }
    
    def register(self, component_type: str, name: str, component_class: Type[SBYBComponent]) -> None:
        """
        Register a component.
        
        Args:
            component_type: Type of the component (e.g., 'preprocessor', 'model').
            name: Name of the component.
            component_class: Component class.
            
        Raises:
            PluginError: If the component type is invalid or the name is already registered.
        """
        if component_type not in self._components:
            raise PluginError(f"Invalid component type: {component_type}")
        
        if name in self._components[component_type]:
            raise PluginError(f"Component '{name}' is already registered for type '{component_type}'")
        
        self._components[component_type][name] = component_class
    
    def unregister(self, component_type: str, name: str) -> None:
        """
        Unregister a component.
        
        Args:
            component_type: Type of the component.
            name: Name of the component.
            
        Raises:
            PluginError: If the component type is invalid or the name is not registered.
        """
        if component_type not in self._components:
            raise PluginError(f"Invalid component type: {component_type}")
        
        if name not in self._components[component_type]:
            raise PluginError(f"Component '{name}' is not registered for type '{component_type}'")
        
        del self._components[component_type][name]
    
    def get(self, component_type: str, name: str) -> Type[SBYBComponent]:
        """
        Get a component class by type and name.
        
        Args:
            component_type: Type of the component.
            name: Name of the component.
            
        Returns:
            Component class.
            
        Raises:
            PluginError: If the component type is invalid or the name is not registered.
        """
        if component_type not in self._components:
            raise PluginError(f"Invalid component type: {component_type}")
        
        if name not in self._components[component_type]:
            raise PluginError(f"Component '{name}' is not registered for type '{component_type}'")
        
        return self._components[component_type][name]
    
    def list(self, component_type: Optional[str] = None) -> Dict[str, List[str]]:
        """
        List registered components.
        
        Args:
            component_type: Type of components to list. If None, list all components.
            
        Returns:
            Dictionary mapping component types to lists of component names.
            
        Raises:
            PluginError: If the component type is invalid.
        """
        if component_type is not None:
            if component_type not in self._components:
                raise PluginError(f"Invalid component type: {component_type}")
            return {component_type: list(self._components[component_type].keys())}
        
        return {ct: list(components.keys()) for ct, components in self._components.items()}
    
    def create(self, component_type: str, name: str, *args: Any, **kwargs: Any) -> SBYBComponent:
        """
        Create an instance of a registered component.
        
        Args:
            component_type: Type of the component.
            name: Name of the component.
            *args: Positional arguments to pass to the component constructor.
            **kwargs: Keyword arguments to pass to the component constructor.
            
        Returns:
            Component instance.
            
        Raises:
            PluginError: If the component type is invalid or the name is not registered.
        """
        component_class = self.get(component_type, name)
        return component_class(*args, **kwargs)
    
    def register_plugin(self, plugin: Plugin) -> None:
        """
        Register a plugin.
        
        Args:
            plugin: Plugin instance.
            
        Raises:
            PluginError: If the plugin type is invalid or the plugin is already registered.
        """
        plugin_type = plugin.plugin_type
        plugin_name = plugin.name
        
        if plugin_type not in self._components:
            raise PluginError(f"Invalid plugin type: {plugin_type}")
        
        if plugin_name in self._components[plugin_type]:
            raise PluginError(f"Plugin '{plugin_name}' is already registered for type '{plugin_type}'")
        
        self._components[plugin_type][plugin_name] = plugin.__class__


# Global registry instance
registry = Registry()
