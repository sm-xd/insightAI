# Code Parsers

This package provides language-specific code parsers for analyzing source code using Tree-sitter.

## Structure

```
parsers/
├── languages/     # Language-specific parser implementations
├── plugins/       # Custom analysis plugins
├── grammars/     # Tree-sitter grammar files
├── base_parser.py # Base parser interface
└── parser_registry.py # Parser registration and management
```

## Adding a New Parser

1. Create a new parser class in `languages/` that extends `BaseParser`
2. Implement required methods:
   - `language` property: Returns language name
   - `file_extensions` property: Returns supported file extensions
   - `parse` method: Parses file content into structured data

Example:
```python
from ..base_parser import BaseParser, ParsedContent

class MyLanguageParser(BaseParser):
    @property
    def language(self) -> str:
        return "mylang"
    
    @property
    def file_extensions(self) -> List[str]:
        return ["ml"]
    
    def parse(self, file_path: str) -> ParsedContent:
        # Implement parsing logic
        pass
```

3. Register parser in `__init__.py`:
```python
from .languages.mylang_parser import MyLanguageParser
register_parser(MyLanguageParser)
```

## Plugin System

Plugins provide additional analysis capabilities:

1. Create plugin class in `plugins/` extending `BasePlugin`
2. Implement required methods:
   - `plugin_id`: Unique identifier
   - `name`: Human-readable name
   - `description`: Plugin description
   - `supported_languages`: List of supported languages
   - `analyze`: Analysis logic

Example:
```python
from .base_plugin import BasePlugin

class MyAnalyzerPlugin(BasePlugin):
    @property
    def plugin_id(self) -> str:
        return "my_analyzer"
    
    def analyze(self, content: ParsedContent) -> Dict[str, Any]:
        # Implement analysis logic
        pass
```

## Running Tests

```bash
# From project root
python -m pytest tests/test_parsers.py
python -m pytest tests/test_plugins.py
```