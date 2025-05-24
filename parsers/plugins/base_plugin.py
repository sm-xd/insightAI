"""
Base plugin interface for custom code analysis plugins.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..base_parser import ParsedContent

class BasePlugin(ABC):
    """Base class for code analysis plugins."""
    
    @property
    @abstractmethod
    def plugin_id(self) -> str:
        """Get unique identifier for this plugin."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get human-readable name of this plugin."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Get plugin description."""
        pass
    
    @property
    @abstractmethod
    def supported_languages(self) -> List[str]:
        """Get list of supported programming languages."""
        pass
    
    @abstractmethod
    def analyze(self, content: ParsedContent) -> Dict[str, Any]:
        """
        Analyze parsed code content.
        
        Args:
            content: Parsed code content
            
        Returns:
            Analysis results as dictionary
        """
        pass