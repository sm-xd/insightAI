"""Code parsing package for InsightAI."""
from .parser_registry import get_parser_for_file
from .base_parser import BaseParser
from .text_parser import TextParser

__all__ = ['get_parser_for_file', 'BaseParser', 'TextParser']