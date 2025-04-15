"""
Plugin manager for SBYB.

This module provides the core functionality for managing plugins,
including registration, discovery, loading, and execution.
"""

from typing import Any, Dict, List, Optional, Union, Tuple, Callable, Type
import os
import sys
import importlib
import inspect
import pkgutil
import logging
import json
from pathlib import Path
import traceback

from sbyb.core.base import SBYBComponent
from sbyb.core.config import Config
from sbyb.core.registry import Registry
from sbyb.core.exceptions import PluginError


class PluginManager(SBYBComponent):
    """
    Plugin manager for SBYB.
    
    This component provides functionality for managing plugins,
    including registration, discovery, loading, and execution.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the plugin manager.
        
        Args:
            config: Configuration dictionary for the plugin manager.
        """
        super().__init__(config)
        
        # Initialize plugin registry
        self.registry = Registry()
        
        # Set up logging
        self.logger = logging.getLogger("sbyb.plugins")
        
        # Plugin directories
        self.plugin_dirs = []
        
        # Add default plugin directory
        default_plugin_dir = os.path.join(os.path.dirname(__file__), "builtin")
        self.plugin_dirs.append(default_plugin_dir)
        
        # Add user plugin directory
        user_plugin_dir = os.path.expanduser("~/.sbyb/plugins")
        if not os.path.exists(user_plugin_dir):
            os.makedirs(user_plugin_dir, exist_ok=True)
        self.plugin_dirs.append(user_plugin_dir)
        
        # Add custom plugin directories from config
        if config and "plugin_dirs" in config:
            custom_dirs = config["plugin_dirs"]
            if isinstance(custom_dirs, list):
                for directory in custom_dirs:
                    if os.path.exists(directory):
                        self.plugin_dirs.append(directory)
                    else:
                        self.logger.warning(f"Plugin directory not found: {directory}")
        
        # Initialize plugin categories
        self.categories = {
            "preprocessor": [],
            "model": [],
            "evaluator": [],
            "visualizer": [],
            "deployer": [],
            "connector": [],
            "transformer": [],
            "custom": []
        }
        
        # Load plugins
        self.discover_plugins()
    
    def discover_plugins(self) -> Dict[str, List[str]]:
        """
        Discover available plugins in all plugin directories.
        
        Returns:
            Dictionary of plugin categories and their available plugins.
        """
        discovered_plugins = {category: [] for category in self.categories}
        
        for plugin_dir in self.plugin_dirs:
            if not os.path.exists(plugin_dir):
                continue
            
            # Add plugin directory to path temporarily
            sys.path.insert(0, plugin_dir)
            
            try:
                # Walk through all subdirectories
                for root, dirs, files in os.walk(plugin_dir):
                    # Check for plugin manifest
                    manifest_path = os.path.join(root, "plugin.json")
                    if os.path.exists(manifest_path):
                        try:
                            with open(manifest_path, "r") as f:
                                manifest = json.load(f)
                            
                            # Validate manifest
                            if self._validate_manifest(manifest):
                                plugin_name = manifest.get("name")
                                plugin_category = manifest.get("category", "custom")
                                
                                # Add to discovered plugins
                                if plugin_category in discovered_plugins:
                                    discovered_plugins[plugin_category].append(plugin_name)
                                else:
                                    discovered_plugins["custom"].append(plugin_name)
                                
                                # Register plugin
                                self._register_plugin_from_manifest(manifest, root)
                        except Exception as e:
                            self.logger.error(f"Error loading plugin manifest {manifest_path}: {str(e)}")
                    
                    # Check for Python modules
                    for file in files:
                        if file.endswith(".py") and file != "__init__.py":
                            module_name = file[:-3]
                            module_path = os.path.join(root, file)
                            rel_path = os.path.relpath(module_path, plugin_dir)
                            import_path = rel_path.replace(os.path.sep, ".")[:-3]
                            
                            try:
                                # Try to import the module
                                module = importlib.import_module(import_path)
                                
                                # Look for plugin classes
                                for name, obj in inspect.getmembers(module):
                                    if inspect.isclass(obj) and hasattr(obj, "__plugin_info__"):
                                        plugin_info = getattr(obj, "__plugin_info__")
                                        
                                        if isinstance(plugin_info, dict):
                                            plugin_name = plugin_info.get("name", name)
                                            plugin_category = plugin_info.get("category", "custom")
                                            
                                            # Add to discovered plugins
                                            if plugin_category in discovered_plugins:
                                                discovered_plugins[plugin_category].append(plugin_name)
                                            else:
                                                discovered_plugins["custom"].append(plugin_name)
                                            
                                            # Register plugin
                                            self._register_plugin_from_class(obj, plugin_info)
                            except Exception as e:
                                self.logger.error(f"Error importing plugin module {import_path}: {str(e)}")
            finally:
                # Remove plugin directory from path
                if plugin_dir in sys.path:
                    sys.path.remove(plugin_dir)
        
        return discovered_plugins
    
    def _validate_manifest(self, manifest: Dict[str, Any]) -> bool:
        """
        Validate a plugin manifest.
        
        Args:
            manifest: Plugin manifest dictionary.
            
        Returns:
            True if the manifest is valid, False otherwise.
        """
        required_fields = ["name", "version", "entry_point"]
        
        for field in required_fields:
            if field not in manifest:
                self.logger.error(f"Plugin manifest missing required field: {field}")
                return False
        
        return True
    
    def _register_plugin_from_manifest(self, manifest: Dict[str, Any], plugin_dir: str) -> None:
        """
        Register a plugin from its manifest.
        
        Args:
            manifest: Plugin manifest dictionary.
            plugin_dir: Directory containing the plugin.
        """
        plugin_name = manifest.get("name")
        plugin_version = manifest.get("version")
        plugin_category = manifest.get("category", "custom")
        entry_point = manifest.get("entry_point")
        
        # Add plugin directory to path temporarily
        sys.path.insert(0, plugin_dir)
        
        try:
            # Import the entry point
            module_path, class_name = entry_point.rsplit(".", 1)
            module = importlib.import_module(module_path)
            plugin_class = getattr(module, class_name)
            
            # Register the plugin
            self.registry.register(
                category=plugin_category,
                name=plugin_name,
                obj=plugin_class,
                metadata={
                    "version": plugin_version,
                    "description": manifest.get("description", ""),
                    "author": manifest.get("author", ""),
                    "source": "manifest",
                    "path": plugin_dir
                }
            )
            
            # Add to category list
            if plugin_category in self.categories:
                self.categories[plugin_category].append(plugin_name)
            else:
                self.categories["custom"].append(plugin_name)
            
            self.logger.info(f"Registered plugin {plugin_name} (version {plugin_version}) from manifest")
        except Exception as e:
            self.logger.error(f"Error registering plugin {plugin_name}: {str(e)}")
            traceback.print_exc()
        finally:
            # Remove plugin directory from path
            if plugin_dir in sys.path:
                sys.path.remove(plugin_dir)
    
    def _register_plugin_from_class(self, plugin_class: Type, plugin_info: Dict[str, Any]) -> None:
        """
        Register a plugin from its class.
        
        Args:
            plugin_class: Plugin class.
            plugin_info: Plugin information dictionary.
        """
        plugin_name = plugin_info.get("name", plugin_class.__name__)
        plugin_version = plugin_info.get("version", "0.1.0")
        plugin_category = plugin_info.get("category", "custom")
        
        # Register the plugin
        self.registry.register(
            category=plugin_category,
            name=plugin_name,
            obj=plugin_class,
            metadata={
                "version": plugin_version,
                "description": plugin_info.get("description", ""),
                "author": plugin_info.get("author", ""),
                "source": "class",
                "path": inspect.getfile(plugin_class)
            }
        )
        
        # Add to category list
        if plugin_category in self.categories:
            self.categories[plugin_category].append(plugin_name)
        else:
            self.categories["custom"].append(plugin_name)
        
        self.logger.info(f"Registered plugin {plugin_name} (version {plugin_version}) from class")
    
    def get_plugin(self, name: str, category: Optional[str] = None) -> Optional[Type]:
        """
        Get a plugin by name and optional category.
        
        Args:
            name: Name of the plugin.
            category: Category of the plugin. If None, search all categories.
            
        Returns:
            Plugin class if found, None otherwise.
        """
        if category:
            return self.registry.get(category, name)
        else:
            # Search all categories
            for cat in self.categories:
                plugin = self.registry.get(cat, name)
                if plugin:
                    return plugin
        
        return None
    
    def get_plugin_metadata(self, name: str, category: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a plugin.
        
        Args:
            name: Name of the plugin.
            category: Category of the plugin. If None, search all categories.
            
        Returns:
            Plugin metadata if found, None otherwise.
        """
        if category:
            return self.registry.get_metadata(category, name)
        else:
            # Search all categories
            for cat in self.categories:
                metadata = self.registry.get_metadata(cat, name)
                if metadata:
                    return metadata
        
        return None
    
    def list_plugins(self, category: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        List available plugins.
        
        Args:
            category: Category of plugins to list. If None, list all categories.
            
        Returns:
            Dictionary of plugin categories and their available plugins with metadata.
        """
        result = {}
        
        if category:
            if category in self.categories:
                result[category] = []
                for plugin_name in self.categories[category]:
                    metadata = self.registry.get_metadata(category, plugin_name)
                    if metadata:
                        result[category].append({
                            "name": plugin_name,
                            **metadata
                        })
        else:
            for cat in self.categories:
                result[cat] = []
                for plugin_name in self.categories[cat]:
                    metadata = self.registry.get_metadata(cat, plugin_name)
                    if metadata:
                        result[cat].append({
                            "name": plugin_name,
                            **metadata
                        })
        
        return result
    
    def create_plugin_instance(self, name: str, category: Optional[str] = None, 
                              config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Create an instance of a plugin.
        
        Args:
            name: Name of the plugin.
            category: Category of the plugin. If None, search all categories.
            config: Configuration dictionary for the plugin.
            
        Returns:
            Plugin instance.
            
        Raises:
            PluginError: If the plugin cannot be found or instantiated.
        """
        plugin_class = self.get_plugin(name, category)
        
        if not plugin_class:
            raise PluginError(f"Plugin not found: {name}")
        
        try:
            if config:
                return plugin_class(config=config)
            else:
                return plugin_class()
        except Exception as e:
            raise PluginError(f"Error instantiating plugin {name}: {str(e)}")
    
    def install_plugin(self, source: str, force: bool = False) -> bool:
        """
        Install a plugin from a source.
        
        Args:
            source: Source of the plugin. Can be a local path, a git URL, or a pip package.
            force: Whether to force installation if the plugin already exists.
            
        Returns:
            True if the plugin was installed successfully, False otherwise.
        """
        # Determine the type of source
        if os.path.exists(source):
            # Local path
            return self._install_from_path(source, force)
        elif source.startswith(("http://", "https://", "git://", "git+")):
            # Git URL
            return self._install_from_git(source, force)
        else:
            # Pip package
            return self._install_from_pip(source, force)
    
    def _install_from_path(self, path: str, force: bool = False) -> bool:
        """
        Install a plugin from a local path.
        
        Args:
            path: Path to the plugin directory or file.
            force: Whether to force installation if the plugin already exists.
            
        Returns:
            True if the plugin was installed successfully, False otherwise.
        """
        try:
            # Check if the path is a directory or file
            if os.path.isdir(path):
                # Directory
                manifest_path = os.path.join(path, "plugin.json")
                if not os.path.exists(manifest_path):
                    self.logger.error(f"Plugin manifest not found: {manifest_path}")
                    return False
                
                # Load manifest
                with open(manifest_path, "r") as f:
                    manifest = json.load(f)
                
                # Validate manifest
                if not self._validate_manifest(manifest):
                    return False
                
                # Check if plugin already exists
                plugin_name = manifest.get("name")
                plugin_category = manifest.get("category", "custom")
                existing_plugin = self.get_plugin(plugin_name, plugin_category)
                
                if existing_plugin and not force:
                    self.logger.warning(f"Plugin {plugin_name} already exists. Use force=True to overwrite.")
                    return False
                
                # Copy plugin to user plugin directory
                user_plugin_dir = os.path.expanduser("~/.sbyb/plugins")
                plugin_dir = os.path.join(user_plugin_dir, plugin_name)
                
                if os.path.exists(plugin_dir):
                    if force:
                        import shutil
                        shutil.rmtree(plugin_dir)
                    else:
                        self.logger.warning(f"Plugin directory already exists: {plugin_dir}")
                        return False
                
                # Create plugin directory
                os.makedirs(plugin_dir, exist_ok=True)
                
                # Copy files
                import shutil
                for item in os.listdir(path):
                    s = os.path.join(path, item)
                    d = os.path.join(plugin_dir, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)
                
                # Register plugin
                self._register_plugin_from_manifest(manifest, plugin_dir)
                
                self.logger.info(f"Installed plugin {plugin_name} from {path}")
                return True
            else:
                # File
                if not path.endswith(".py"):
                    self.logger.error(f"Plugin file must be a Python file: {path}")
                    return False
                
                # Copy plugin to user plugin directory
                user_plugin_dir = os.path.expanduser("~/.sbyb/plugins")
                plugin_file = os.path.basename(path)
                plugin_name = plugin_file[:-3]
                
                dest_file = os.path.join(user_plugin_dir, plugin_file)
                
                if os.path.exists(dest_file):
                    if force:
                        import shutil
                        shutil.copy2(path, dest_file)
                    else:
                        self.logger.warning(f"Plugin file already exists: {dest_file}")
                        return False
                else:
                    import shutil
                    shutil.copy2(path, dest_file)
                
                # Import the module to register plugins
                sys.path.insert(0, user_plugin_dir)
                try:
                    importlib.import_module(plugin_name)
                    self.logger.info(f"Installed plugin from {path}")
                    return True
                except Exception as e:
                    self.logger.error(f"Error importing plugin {plugin_name}: {str(e)}")
                    return False
                finally:
                    if user_plugin_dir in sys.path:
                        sys.path.remove(user_plugin_dir)
        except Exception as e:
            self.logger.error(f"Error installing plugin from {path}: {str(e)}")
            return False
    
    def _install_from_git(self, url: str, force: bool = False) -> bool:
        """
        Install a plugin from a git repository.
        
        Args:
            url: URL of the git repository.
            force: Whether to force installation if the plugin already exists.
            
        Returns:
            True if the plugin was installed successfully, False otherwise.
        """
        try:
            import tempfile
            import subprocess
            
            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Clone repository
                subprocess.check_call(["git", "clone", url, temp_dir])
                
                # Install from path
                return self._install_from_path(temp_dir, force)
        except Exception as e:
            self.logger.error(f"Error installing plugin from {url}: {str(e)}")
            return False
    
    def _install_from_pip(self, package: str, force: bool = False) -> bool:
        """
        Install a plugin from a pip package.
        
        Args:
            package: Name of the pip package.
            force: Whether to force installation if the plugin already exists.
            
        Returns:
            True if the plugin was installed successfully, False otherwise.
        """
        try:
            import subprocess
            
            # Install package
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            
            # Try to import the package
            try:
                module = importlib.import_module(package)
                
                # Check if the package has a plugin entry point
                if hasattr(module, "__plugin_entry_point__"):
                    entry_point = getattr(module, "__plugin_entry_point__")
                    
                    if isinstance(entry_point, str):
                        # Import the entry point
                        module_path, class_name = entry_point.rsplit(".", 1)
                        plugin_module = importlib.import_module(module_path)
                        plugin_class = getattr(plugin_module, class_name)
                        
                        # Check if the class has plugin info
                        if hasattr(plugin_class, "__plugin_info__"):
                            plugin_info = getattr(plugin_class, "__plugin_info__")
                            
                            if isinstance(plugin_info, dict):
                                # Register the plugin
                                self._register_plugin_from_class(plugin_class, plugin_info)
                                return True
                
                # Look for plugin classes
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and hasattr(obj, "__plugin_info__"):
                        plugin_info = getattr(obj, "__plugin_info__")
                        
                        if isinstance(plugin_info, dict):
                            # Register the plugin
                            self._register_plugin_from_class(obj, plugin_info)
                            return True
                
                self.logger.error(f"No plugin found in package {package}")
                return False
            except Exception as e:
                self.logger.error(f"Error importing package {package}: {str(e)}")
                return False
        except Exception as e:
            self.logger.error(f"Error installing package {package}: {str(e)}")
            return False
    
    def uninstall_plugin(self, name: str, category: Optional[str] = None) -> bool:
        """
        Uninstall a plugin.
        
        Args:
            name: Name of the plugin.
            category: Category of the plugin. If None, search all categories.
            
        Returns:
            True if the plugin was uninstalled successfully, False otherwise.
        """
        # Get plugin metadata
        metadata = self.get_plugin_metadata(name, category)
        
        if not metadata:
            self.logger.error(f"Plugin not found: {name}")
            return False
        
        try:
            # Determine plugin source
            source = metadata.get("source")
            path = metadata.get("path")
            
            if source == "manifest":
                # Remove plugin directory
                if os.path.exists(path):
                    import shutil
                    shutil.rmtree(path)
            elif source == "class" and path:
                # Remove plugin file
                if os.path.exists(path):
                    os.remove(path)
            
            # Unregister plugin
            if category:
                self.registry.unregister(category, name)
                if name in self.categories.get(category, []):
                    self.categories[category].remove(name)
            else:
                # Search all categories
                for cat in self.categories:
                    if name in self.categories.get(cat, []):
                        self.registry.unregister(cat, name)
                        self.categories[cat].remove(name)
            
            self.logger.info(f"Uninstalled plugin {name}")
            return True
        except Exception as e:
            self.logger.error(f"Error uninstalling plugin {name}: {str(e)}")
            return False
    
    def create_plugin_template(self, output_dir: str, name: str, category: str = "custom",
                              description: str = "", author: str = "") -> bool:
        """
        Create a template for a new plugin.
        
        Args:
            output_dir: Directory to create the plugin template in.
            name: Name of the plugin.
            category: Category of the plugin.
            description: Description of the plugin.
            author: Author of the plugin.
            
        Returns:
            True if the template was created successfully, False otherwise.
        """
        try:
            # Create output directory
            plugin_dir = os.path.join(output_dir, name)
            os.makedirs(plugin_dir, exist_ok=True)
            
            # Create manifest
            manifest = {
                "name": name,
                "version": "0.1.0",
                "category": category,
                "description": description,
                "author": author,
                "entry_point": f"{name}.{name}Plugin"
            }
            
            with open(os.path.join(plugin_dir, "plugin.json"), "w") as f:
                json.dump(manifest, f, indent=4)
            
            # Create plugin module
            plugin_module = f"""
"""
            plugin_module = f"""
import logging
from typing import Any, Dict, Optional

from sbyb.core.base import SBYBComponent


class {name}Plugin(SBYBComponent):
    \"\"\"
    {description}
    \"\"\"
    
    # Plugin information
    __plugin_info__ = {{
        "name": "{name}",
        "version": "0.1.0",
        "category": "{category}",
        "description": "{description}",
        "author": "{author}"
    }}
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        \"\"\"
        Initialize the plugin.
        
        Args:
            config: Configuration dictionary for the plugin.
        \"\"\"
        super().__init__(config)
        self.logger = logging.getLogger(f"sbyb.plugins.{name}")
    
    def run(self, *args, **kwargs) -> Any:
        \"\"\"
        Run the plugin.
        
        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
            
        Returns:
            Plugin result.
        \"\"\"
        self.logger.info(f"Running {name} plugin")
        
        # TODO: Implement plugin functionality
        
        return {{"status": "success", "message": f"{name} plugin executed successfully"}}
"""
            
            with open(os.path.join(plugin_dir, f"{name}.py"), "w") as f:
                f.write(plugin_module)
            
            # Create __init__.py
            init_module = f"""
from .{name} import {name}Plugin

__all__ = ["{name}Plugin"]
"""
            
            with open(os.path.join(plugin_dir, "__init__.py"), "w") as f:
                f.write(init_module)
            
            # Create README.md
            readme = f"""
# {name} Plugin

{description}

## Installation

```bash
# Install from local directory
sbyb plugin install /path/to/{name}

# Or install directly from this repository
sbyb plugin install git+https://github.com/username/{name}.git
```

## Usage

```python
from sbyb.plugins import PluginManager

# Initialize plugin manager
plugin_manager = PluginManager()

# Create plugin instance
plugin = plugin_manager.create_plugin_instance("{name}", "{category}")

# Run plugin
result = plugin.run()
print(result)
```

## Configuration

```python
config = {{
    # Plugin configuration options
}}

plugin = plugin_manager.create_plugin_instance("{name}", "{category}", config=config)
```

## License

MIT
"""
            
            with open(os.path.join(plugin_dir, "README.md"), "w") as f:
                f.write(readme)
            
            self.logger.info(f"Created plugin template at {plugin_dir}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating plugin template: {str(e)}")
            return False
