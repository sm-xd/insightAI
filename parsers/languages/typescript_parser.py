"""
TypeScript parser implementation for InsightAI.

This module uses Tree-sitter to parse TypeScript code and extract
structured information about interfaces, types, classes, etc.
"""

import os
from typing import Dict, List, Any

from ..base_parser import BaseParser, ParsedContent
from ..parser_registry import register_parser

class TypeScriptParser(BaseParser):
    """
    Parser for TypeScript code.
    """
    
    def __init__(self):
        """Initialize the TypeScript parser."""
        # TODO: Initialize Tree-sitter with TypeScript grammar
        self._parser = None
        self._init_parser()
    
    def _init_parser(self):
        """Initialize the Tree-sitter parser with TypeScript grammar."""
        try:
            # Path to the compiled grammar file
            # TODO: Update this path once Tree-sitter grammar is built
            grammar_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "grammars",
                "tree-sitter-typescript.so"
            )
            
            # For now, we'll work without Tree-sitter for this placeholder
            self._parser = None
        except Exception as e:
            print(f"Error initializing TypeScript parser: {str(e)}")
            self._parser = None
    
    @property
    def language(self) -> str:
        """
        Get the language supported by this parser.
        
        Returns:
            Language name as string
        """
        return "typescript"
    
    @property
    def file_extensions(self) -> List[str]:
        """
        Get the file extensions supported by this parser.
        
        Returns:
            List of file extensions (without dot)
        """
        return ["ts", "tsx"]
    
    def parse(self, file_path: str) -> ParsedContent:
        """
        Parse a TypeScript source code file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            ParsedContent: Structured content from the file
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Placeholder implementation without Tree-sitter
        # In a real implementation, we would parse the AST here
        
        imports = self._extract_imports(content)
        classes = self._extract_classes(content)
        functions = self._extract_functions(content)
        variables = self._extract_variables(content)
        interfaces = self._extract_interfaces(content)
        
        # Add interfaces to classes for now
        classes.extend(interfaces)
        
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
        """
        Extract imports from TypeScript code.
        
        Args:
            content: Source code content
            
        Returns:
            List of import dictionaries
        """
        # Simple placeholder implementation
        imports = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('import '):
                imports.append({
                    'statement': line,
                    'type': 'import'
                })
        
        return imports
    
    def _extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract classes from TypeScript code.
        
        Args:
            content: Source code content
            
        Returns:
            List of class dictionaries
        """
        # Simple placeholder implementation
        classes = []
        lines = content.split('\n')
        
        in_class = False
        current_class = None
        
        for line in lines:
            line_stripped = line.strip()
            
            # Look for class declarations
            if line_stripped.startswith('class '):
                class_name = line_stripped.replace('class ', '').split(' ')[0].split('{')[0].strip()
                current_class = {
                    'name': class_name,
                    'methods': [],
                    'properties': [],
                    'docstring': ''
                }
                classes.append(current_class)
                in_class = True
            
            # Look for methods in classes
            elif in_class and ') {' in line_stripped and not line_stripped.startswith('//'):
                method_name = line_stripped.split('(')[0].strip()
                if method_name and not method_name.startswith('if') and not method_name.startswith('for'):
                    current_class['methods'].append({
                        'name': method_name
                    })
            
            # Look for properties in classes
            elif in_class and ':' in line_stripped and not '(' in line_stripped and not line_stripped.startswith('//'):
                prop_parts = line_stripped.split(':')
                if len(prop_parts) > 1:
                    prop_name = prop_parts[0].strip()
                    prop_type = prop_parts[1].strip().rstrip(';')
                    if prop_name.isidentifier():
                        current_class['properties'].append({
                            'name': prop_name,
                            'type': prop_type
                        })
        
        return classes
    
    def _extract_interfaces(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract interfaces from TypeScript code.
        
        Args:
            content: Source code content
            
        Returns:
            List of interface dictionaries
        """
        # Simple placeholder implementation
        interfaces = []
        lines = content.split('\n')
        
        in_interface = False
        current_interface = None
        
        for line in lines:
            line_stripped = line.strip()
            
            # Look for interface declarations
            if line_stripped.startswith('interface '):
                interface_name = line_stripped.replace('interface ', '').split(' ')[0].split('{')[0].strip()
                current_interface = {
                    'name': interface_name,
                    'type': 'interface',
                    'properties': [],
                    'methods': [],
                    'docstring': ''
                }
                interfaces.append(current_interface)
                in_interface = True
            
            # Look for properties in interfaces
            elif in_interface and ':' in line_stripped and not '(' in line_stripped and not line_stripped.startswith('//'):
                prop_parts = line_stripped.split(':')
                if len(prop_parts) > 1:
                    prop_name = prop_parts[0].strip()
                    prop_type = prop_parts[1].strip().rstrip(';')
                    if prop_name.isidentifier():
                        current_interface['properties'].append({
                            'name': prop_name,
                            'type': prop_type
                        })
        
        return interfaces
    
    def _extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract top-level functions from TypeScript code.
        
        Args:
            content: Source code content
            
        Returns:
            List of function dictionaries
        """
        # Simple placeholder implementation
        functions = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Match function declarations
            if line_stripped.startswith('function '):
                function_name = line_stripped.replace('function ', '').split('(')[0].strip()
                functions.append({
                    'name': function_name
                })
            
            # Match arrow functions assigned to variables
            elif ' = (' in line_stripped and ') =>' in line_stripped:
                function_name = line_stripped.split(' = (')[0].strip()
                functions.append({
                    'name': function_name,
                    'type': 'arrow_function'
                })
        
        return functions
    
    def _extract_variables(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract top-level variables from TypeScript code.
        
        Args:
            content: Source code content
            
        Returns:
            List of variable dictionaries
        """
        # Simple placeholder implementation
        variables = []
        lines = content.split('\n')
        
        for line in lines:
            line_stripped = line.strip()
            
            # Look for variable declarations with types
            if (line_stripped.startswith('var ') or line_stripped.startswith('let ') or 
                line_stripped.startswith('const ')):
                
                # Handle variable with type definition
                if ':' in line_stripped:
                    var_parts = line_stripped.split(':')
                    var_decl = var_parts[0].replace('var ', '').replace('let ', '').replace('const ', '').strip()
                    var_name = var_decl.strip()
                    
                    # Extract type and value
                    type_value_parts = var_parts[1].split('=', 1)
                    var_type = type_value_parts[0].strip()
                    var_value = type_value_parts[1].strip().rstrip(';') if len(type_value_parts) > 1 else None
                    
                    if var_name.isidentifier():
                        variables.append({
                            'name': var_name,
                            'type': var_type,
                            'value': var_value,
                            'declaration_type': line_stripped.split(' ')[0]  # var, let, or const
                        })
                
                # Handle variable without explicit type
                elif '=' in line_stripped:
                    var_parts = line_stripped.split('=')
                    var_name = var_parts[0].replace('var ', '').replace('let ', '').replace('const ', '').strip()
                    
                    if var_name.isidentifier():
                        variables.append({
                            'name': var_name,
                            'declaration_type': line_stripped.split(' ')[0],  # var, let, or const
                            'value': var_parts[1].strip().rstrip(';')
                        })
        
        return variables

# Register the parser
register_parser(TypeScriptParser)