"""Base parser interface for code analysis."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseParser(ABC):
    """Abstract base class for code parsers."""
    
    @abstractmethod
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a file and return its contents and metadata."""
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """Return list of file extensions this parser supports."""
        pass