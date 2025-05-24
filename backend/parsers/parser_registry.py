"""Registry for file type parsers."""
from pathlib import Path
from typing import Optional
from .base_parser import BaseParser
from .text_parser import TextParser
from .code_parser import CodeParser

_parsers = {}

def register_parser(parser: BaseParser):
    """Register a parser for specific file extensions."""
    for ext in parser.get_supported_extensions():
        _parsers[ext] = parser

def get_parser_for_file(file_path: str) -> Optional[BaseParser]:
    """Get appropriate parser for a file based on its extension."""
    ext = Path(file_path).suffix.lower()
    
    # Initialize default parsers
    if not _parsers:
        register_parser(CodeParser())
        register_parser(TextParser())
        
    return _parsers.get(ext, TextParser())