"""
Hook system for SBYB plugins.

This module provides functionality for registering and executing hooks,
which allow plugins to extend or modify the behavior of SBYB components.
"""

from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import inspect
import logging
from collections import defaultdict

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import HookError


class HookManager(SBYBComponent):
    """
    Hook manager for SBYB.
    
    This component provides functionality for registering and executing hooks,
    which allow plugins to extend or modify the behavior of SBYB components.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the hook manager.
        
        Args:
            config: Configuration dictionary for the hook manager.
        """
        super().__init__(config)
        
        # Set up logging
        self.logger = logging.getLogger("sbyb.plugins.hooks")
        
        # Initialize hooks registry
        self.hooks = defaultdict(list)
    
    def register_hook(self, hook_name: str, callback: Callable, priority: int = 100) -> None:
        """
        Register a hook.
        
        Args:
            hook_name: Name of the hook.
            callback: Callback function to execute when the hook is triggered.
            priority: Priority of the hook (lower numbers run first).
        """
        self.hooks[hook_name].append({
            "callback": callback,
            "priority": priority
        })
        
        # Sort hooks by priority
        self.hooks[hook_name] = sorted(self.hooks[hook_name], key=lambda x: x["priority"])
        
        self.logger.debug(f"Registered hook {hook_name} with priority {priority}")
    
    def register_hooks_from_instance(self, instance: Any) -> None:
        """
        Register all hooks from an instance.
        
        Args:
            instance: Instance to register hooks from.
        """
        for name, method in inspect.getmembers(instance, inspect.ismethod):
            if hasattr(method, "__hook_info__"):
                hook_info = getattr(method, "__hook_info__")
                hook_name = hook_info.get("name")
                priority = hook_info.get("priority", 100)
                
                self.register_hook(hook_name, method, priority)
    
    def unregister_hook(self, hook_name: str, callback: Optional[Callable] = None) -> None:
        """
        Unregister a hook.
        
        Args:
            hook_name: Name of the hook.
            callback: Callback function to unregister. If None, unregister all hooks with the given name.
        """
        if hook_name not in self.hooks:
            return
        
        if callback is None:
            # Unregister all hooks with the given name
            self.hooks[hook_name] = []
            self.logger.debug(f"Unregistered all hooks for {hook_name}")
        else:
            # Unregister specific callback
            self.hooks[hook_name] = [h for h in self.hooks[hook_name] if h["callback"] != callback]
            self.logger.debug(f"Unregistered hook {hook_name} for specific callback")
    
    def has_hooks(self, hook_name: str) -> bool:
        """
        Check if a hook has any registered callbacks.
        
        Args:
            hook_name: Name of the hook.
            
        Returns:
            True if the hook has registered callbacks, False otherwise.
        """
        return hook_name in self.hooks and len(self.hooks[hook_name]) > 0
    
    def execute_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """
        Execute a hook.
        
        Args:
            hook_name: Name of the hook.
            *args: Positional arguments to pass to the hook callbacks.
            **kwargs: Keyword arguments to pass to the hook callbacks.
            
        Returns:
            List of results from all hook callbacks.
        """
        if hook_name not in self.hooks:
            return []
        
        results = []
        
        for hook in self.hooks[hook_name]:
            try:
                result = hook["callback"](*args, **kwargs)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error executing hook {hook_name}: {str(e)}")
                results.append(None)
        
        return results
    
    def execute_hook_until_true(self, hook_name: str, *args, **kwargs) -> Tuple[bool, Any]:
        """
        Execute a hook until a callback returns a truthy value.
        
        Args:
            hook_name: Name of the hook.
            *args: Positional arguments to pass to the hook callbacks.
            **kwargs: Keyword arguments to pass to the hook callbacks.
            
        Returns:
            Tuple of (success, result) where success is True if any callback returned a truthy value,
            and result is the value returned by that callback.
        """
        if hook_name not in self.hooks:
            return False, None
        
        for hook in self.hooks[hook_name]:
            try:
                result = hook["callback"](*args, **kwargs)
                if result:
                    return True, result
            except Exception as e:
                self.logger.error(f"Error executing hook {hook_name}: {str(e)}")
        
        return False, None
    
    def execute_hook_until_false(self, hook_name: str, *args, **kwargs) -> Tuple[bool, Any]:
        """
        Execute a hook until a callback returns a falsy value.
        
        Args:
            hook_name: Name of the hook.
            *args: Positional arguments to pass to the hook callbacks.
            **kwargs: Keyword arguments to pass to the hook callbacks.
            
        Returns:
            Tuple of (success, result) where success is True if all callbacks returned truthy values,
            and result is the value returned by the last callback.
        """
        if hook_name not in self.hooks:
            return True, None
        
        last_result = None
        
        for hook in self.hooks[hook_name]:
            try:
                result = hook["callback"](*args, **kwargs)
                if not result:
                    return False, result
                last_result = result
            except Exception as e:
                self.logger.error(f"Error executing hook {hook_name}: {str(e)}")
                return False, None
        
        return True, last_result
    
    def execute_hook_waterfall(self, hook_name: str, initial_value: Any, *args, **kwargs) -> Any:
        """
        Execute a hook in waterfall mode, passing the result of each callback to the next.
        
        Args:
            hook_name: Name of the hook.
            initial_value: Initial value to pass to the first callback.
            *args: Positional arguments to pass to the hook callbacks.
            **kwargs: Keyword arguments to pass to the hook callbacks.
            
        Returns:
            Final result after all callbacks have been executed.
        """
        if hook_name not in self.hooks:
            return initial_value
        
        result = initial_value
        
        for hook in self.hooks[hook_name]:
            try:
                result = hook["callback"](result, *args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error executing hook {hook_name}: {str(e)}")
        
        return result
    
    def execute_hook_parallel(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """
        Execute a hook in parallel mode, running all callbacks concurrently.
        
        Args:
            hook_name: Name of the hook.
            *args: Positional arguments to pass to the hook callbacks.
            **kwargs: Keyword arguments to pass to the hook callbacks.
            
        Returns:
            List of results from all hook callbacks.
        """
        if hook_name not in self.hooks:
            return []
        
        import concurrent.futures
        
        results = []
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            
            for hook in self.hooks[hook_name]:
                future = executor.submit(hook["callback"], *args, **kwargs)
                futures.append(future)
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Error executing hook {hook_name}: {str(e)}")
                    results.append(None)
        
        return results
