"""
Parser registry for managing available language parsers.
"""

import os
from typing import Dict, Optional, Type
from .base_parser import BaseParser

# Global registry of available parsers
_parsers: Dict[str, Type[BaseParser]] = {}
_extension_map: Dict[str, str] = {}

def register_parser(parser_class: Type[BaseParser]) -> None:
    """
    Register a parser class.
    
    Args:
        parser_class: Parser class to register
    """
    # Create parser instance to get properties
    parser = parser_class()
    
    # Register parser by language
    _parsers[parser.language] = parser_class
    
    # Register file extensions
    for ext in parser.file_extensions:
        _extension_map[ext] = parser.language

def get_parser_for_language(language: str) -> Optional[BaseParser]:
    """
    Get parser for a specific language.
    
    Args:
        language: Language name
        
    Returns:
        Parser instance or None if not found
    """
    parser_class = _parsers.get(language)
    return parser_class() if parser_class else None

def get_parser_for_file(file_path: str) -> Optional[BaseParser]:
    """
    Get appropriate parser for a file based on extension.
    
    Args:
        file_path: Path to file
        
    Returns:
        Parser instance or None if no parser available
    """
    ext = os.path.splitext(file_path)[1].lstrip('.')
    language = _extension_map.get(ext)
    return get_parser_for_language(language) if language else None

def get_available_languages() -> list[str]:
    """
    Get list of languages with available parsers.
    
    Returns:
        List of language names
    """
    return list(_parsers.keys())

def get_supported_extensions() -> list[str]:
    """
    Get list of supported file extensions.
    
    Returns:
        List of file extensions
    """
    return list(_extension_map.keys())

# Note: Import specific parsers after they are implemented
# Parsers will be auto-registered when imported

# TODO: Uncomment these imports once parsers are implemented
# from .languages.python_parser import PythonParser
# from .languages.javascript_parser import JavaScriptParser
# from .languages.typescript_parser import TypeScriptParser