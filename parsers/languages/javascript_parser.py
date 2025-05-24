"""
JavaScript/TypeScript parser implementation for InsightAI.

This module uses Tree-sitter to parse JavaScript and TypeScript code and extract
structured information about classes, functions, imports, and variables.
"""

import os
import re
from typing import Dict, List, Any

from ..base_parser import BaseParser, ParsedContent
from ..parser_registry import register_parser

class JavaScriptParser(BaseParser):
    """Parser for JavaScript and TypeScript code."""
    
    def __init__(self):
        """Initialize the JavaScript parser."""
        # TODO: Initialize Tree-sitter with JavaScript/TypeScript grammar
        self._parser = None
        self._init_parser()
    
    def _init_parser(self):
        """Initialize the Tree-sitter parser with JavaScript grammar."""
        try:
            # Path to the compiled grammar file
            # TODO: Update this path once Tree-sitter grammar is built
            grammar_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "grammars",
                "tree-sitter-javascript.so"
            )
            
            # For now, we'll work without Tree-sitter for this placeholder
            self._parser = None
        except Exception as e:
            print(f"Error initializing JavaScript parser: {str(e)}")
            self._parser = None
    
    @property
    def language(self) -> str:
        """Get the language supported by this parser."""
        return "javascript"
    
    @property
    def file_extensions(self) -> List[str]:
        """Get the file extensions supported by this parser."""
        return ["js", "jsx", "ts", "tsx"]
    
    def parse(self, file_path: str) -> ParsedContent:
        """Parse a JavaScript/TypeScript source code file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Placeholder implementation without Tree-sitter
        # In a real implementation, we would parse the AST here
        
        imports = self._extract_imports(content)
        classes = self._extract_classes(content)
        functions = self._extract_functions(content)
        variables = self._extract_variables(content)
        
        return ParsedContent(
            file_path=file_path,
            language=self.language,
            imports=imports,
            classes=classes,
            functions=functions,
            variables=variables,
            raw_content=content
        )
    
    def _extract_imports(self, content: str) -> List[Dict[str, Any]]:
        """Extract imports from JavaScript code."""
        imports = []
        
        # Match ES6 imports
        import_pattern = r'import\s+(?:{[^}]+}|\*\s+as\s+\w+|\w+)?\s*(?:,\s*{[^}]+})?\s*from\s+[\'"]([^\'"]+)[\'"]'
        matches = re.finditer(import_pattern, content)
        
        for match in matches:
            statement = match.group(0)
            module = match.group(1)
            
            imports.append({
                'statement': statement,
                'module': module,
                'type': 'es6'
            })
        
        # Match require statements
        require_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*require\([\'"]([^\'"]+)[\'"]\)'
        matches = re.finditer(require_pattern, content)
        
        for match in matches:
            variable = match.group(1)
            module = match.group(2)
            
            imports.append({
                'statement': match.group(0),
                'variable': variable,
                'module': module,
                'type': 'require'
            })
        
        return imports
    
    def _extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract classes from JavaScript code."""
        classes = []
        
        # Match class declarations
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*{'
        matches = re.finditer(class_pattern, content)
        
        for match in matches:
            class_name = match.group(1)
            parent_class = match.group(2)
            
            # Get class content
            start = match.end()
            bracket_count = 1
            end = start
            
            while bracket_count > 0 and end < len(content):
                if content[end] == '{':
                    bracket_count += 1
                elif content[end] == '}':
                    bracket_count -= 1
                end += 1
            
            class_content = content[start:end-1]
            
            # Extract methods
            methods = self._extract_methods(class_content)
            
            classes.append({
                'name': class_name,
                'parent': parent_class,
                'methods': methods
            })
        
        return classes
    
    def _extract_methods(self, class_content: str) -> List[Dict[str, Any]]:
        """Extract methods from a class definition."""
        methods = []
        
        # Match method declarations
        method_pattern = r'(?:async\s+)?(\w+)\s*\((.*?)\)\s*{(?:{[^}]*}|[^}])*}'
        matches = re.finditer(method_pattern, class_content)
        
        for match in matches:
            method_name = match.group(1)
            params = match.group(2)
            
            # Parse parameters
            param_list = []
            if params.strip():
                for param in params.split(','):
                    param = param.strip()
                    if '=' in param:
                        name, default = param.split('=')
                        param_list.append({
                            'name': name.strip(),
                            'default': default.strip()
                        })
                    else:
                        param_list.append({'name': param})
            
            methods.append({
                'name': method_name,
                'params': param_list,
                'is_async': 'async' in match.group(0)
            })
        
        return methods
    
    def _extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """Extract functions from JavaScript code."""
        functions = []
        
        # Match function declarations and arrow functions
        patterns = [
            # Regular functions
            r'function\s+(\w+)\s*\((.*?)\)\s*{',
            # Arrow functions with explicit name
            r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\((.*?)\)\s*=>'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            
            for match in matches:
                func_name = match.group(1)
                params = match.group(2)
                
                # Parse parameters
                param_list = []
                if params.strip():
                    for param in params.split(','):
                        param = param.strip()
                        if '=' in param:
                            name, default = param.split('=')
                            param_list.append({
                                'name': name.strip(),
                                'default': default.strip()
                            })
                        else:
                            param_list.append({'name': param})
                
                functions.append({
                    'name': func_name,
                    'params': param_list,
                    'is_async': 'async' in match.group(0)
                })
        
        return functions
    
    def _extract_variables(self, content: str) -> List[Dict[str, Any]]:
        """Extract variables from JavaScript code."""
        variables = []
        
        # Match variable declarations
        var_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*([^;]+)'
        matches = re.finditer(var_pattern, content)
        
        for match in matches:
            var_name = match.group(1)
            value = match.group(2).strip()
            
            # Skip function/class assignments
            if value.startswith('function') or value.startswith('class'):
                continue
            
            variables.append({
                'name': var_name,
                'value': value,
                'kind': content[match.start():].split()[0]  # const/let/var
            })
        
        return variables

# Register the parser
register_parser(JavaScriptParser)