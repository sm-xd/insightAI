"""Parser for source code files."""
from typing import List, Dict, Any
from .base_parser import BaseParser

class CodeParser(BaseParser):
    """Parser for source code files."""
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a code file and return its contents with metadata."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        ext = file_path.split('.')[-1].lower()
        return {
            'content': content,
            'type': 'code',
            'language': ext,
            'metadata': {
                'path': file_path,
                'size': len(content),
                'extension': ext
            }
        }
    
    def get_supported_extensions(self) -> List[str]:
        """Return supported code file extensions."""
        return [
            '.py', '.js', '.ts', '.jsx', '.tsx', 
            '.java', '.cpp', '.c', '.h', '.hpp',
            '.go', '.rs', '.rb', '.php', '.cs'
        ]