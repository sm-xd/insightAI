"""
Custom code analysis plugins package.
"""

from .base_plugin import BasePlugin
from .plugin_manager import PluginManager

# Create global plugin manager instance
plugin_manager = PluginManager()

__all__ = [
    "BasePlugin",
    "PluginManager",
    "plugin_manager"
]