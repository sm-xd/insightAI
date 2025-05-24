"""Simple text file parser."""
from typing import List, Dict, Any
from .base_parser import BaseParser

class TextParser(BaseParser):
    """Parser for plain text files."""
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a text file and return its contents."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return {
            'content': content,
            'type': 'text',
            'metadata': {
                'path': file_path,
                'size': len(content)
            }
        }
    
    def get_supported_extensions(self) -> List[str]:
        """Return supported file extensions."""
        return ['.txt', '.md', '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.json']