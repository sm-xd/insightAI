"""
Language-specific parsers for InsightAI.
"""

from .python_parser import PythonParser
from .javascript_parser import JavaScriptParser

__all__ = [
    "PythonParser",
    "JavaScriptParser"
]