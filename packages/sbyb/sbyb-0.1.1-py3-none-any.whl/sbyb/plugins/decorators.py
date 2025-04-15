"""
Plugin decorator for SBYB.

This module provides decorators for creating plugins.
"""

from typing import Any, Dict, Optional, Type, Callable
import inspect
import functools


def plugin(name: str, category: str = "custom", version: str = "0.1.0",
          description: str = "", author: str = "") -> Callable:
    """
    Decorator to mark a class as a SBYB plugin.
    
    Args:
        name: Name of the plugin.
        category: Category of the plugin.
        version: Version of the plugin.
        description: Description of the plugin.
        author: Author of the plugin.
        
    Returns:
        Decorated class.
    """
    def decorator(cls: Type) -> Type:
        # Add plugin information to class
        cls.__plugin_info__ = {
            "name": name,
            "category": category,
            "version": version,
            "description": description,
            "author": author
        }
        
        return cls
    
    return decorator


def hook(hook_name: str, priority: int = 100) -> Callable:
    """
    Decorator to mark a method as a plugin hook.
    
    Args:
        hook_name: Name of the hook.
        priority: Priority of the hook (lower numbers run first).
        
    Returns:
        Decorated method.
    """
    def decorator(func: Callable) -> Callable:
        # Add hook information to function
        func.__hook_info__ = {
            "name": hook_name,
            "priority": priority
        }
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator
