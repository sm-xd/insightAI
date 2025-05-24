"""
Code parsers package for InsightAI.

This package provides language-specific parsers for analyzing source code
using Tree-sitter.
"""

__version__ = "0.1.0"

from .base_parser import BaseParser, ParsedContent
from .parser_registry import (
    register_parser,
    get_parser_for_language,
    get_parser_for_file,
    get_available_languages,
    get_supported_extensions
)

__all__ = [
    "BaseParser",
    "ParsedContent",
    "register_parser",
    "get_parser_for_language",
    "get_parser_for_file",
    "get_available_languages",
    "get_supported_extensions"
]