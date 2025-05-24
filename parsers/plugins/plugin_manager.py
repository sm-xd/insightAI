"""
Plugin manager for code analysis plugins.
"""

from typing import Dict, Type, List, Any, Optional
from .base_plugin import BasePlugin

class PluginManager:
    """Manager for code analysis plugins."""
    
    def __init__(self):
        """Initialize plugin manager."""
        self._plugins: Dict[str, Type[BasePlugin]] = {}
    
    def register_plugin(self, plugin_class: Type[BasePlugin]) -> None:
        """
        Register a plugin class.
        
        Args:
            plugin_class: Plugin class to register
        """
        plugin = plugin_class()
        self._plugins[plugin.plugin_id] = plugin_class
    
    def get_plugin(self, plugin_id: str) -> Optional[BasePlugin]:
        """
        Get a plugin instance by ID.
        
        Args:
            plugin_id: Plugin identifier
            
        Returns:
            Plugin instance or None if not found
        """
        plugin_class = self._plugins.get(plugin_id)
        return plugin_class() if plugin_class else None
    
    def get_plugins_for_language(self, language: str) -> List[BasePlugin]:
        """
        Get all plugins that support a language.
        
        Args:
            language: Programming language
            
        Returns:
            List of plugin instances
        """
        return [
            plugin_class()
            for plugin_class in self._plugins.values()
            if language in plugin_class().supported_languages
        ]
    
    def get_available_plugins(self) -> List[Dict[str, Any]]:
        """
        Get list of all available plugins.
        
        Returns:
            List of plugin metadata
        """
        plugins = []
        for plugin_class in self._plugins.values():
            plugin = plugin_class()
            plugins.append({
                'id': plugin.plugin_id,
                'name': plugin.name,
                'description': plugin.description,
                'supported_languages': plugin.supported_languages
            })
        return plugins
    
    def unregister_plugin(self, plugin_id: str) -> None:
        """
        Unregister a plugin.
        
        Args:
            plugin_id: Plugin identifier to remove
        """
        if plugin_id in self._plugins:
            del self._plugins[plugin_id]