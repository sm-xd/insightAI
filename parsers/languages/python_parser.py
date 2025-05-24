"""
Python parser implementation for InsightAI.

This module uses Tree-sitter to parse Python code and extract
structured information about classes, functions, imports, and variables.
"""

import os
import re
from typing import Dict, List, Any

from ..base_parser import BaseParser, ParsedContent
from ..parser_registry import register_parser

class PythonParser(BaseParser):
    """
    Parser for Python code.
    """
    
    def __init__(self):
        """Initialize the Python parser."""
        # TODO: Initialize Tree-sitter with Python grammar
        self._parser = None
        self._init_parser()
    
    def _init_parser(self):
        """Initialize the Tree-sitter parser with Python grammar."""
        try:
            # Path to the compiled grammar file
            # TODO: Update this path once Tree-sitter grammar is built
            grammar_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "grammars",
                "tree-sitter-python.so"
            )
            
            # For now, we'll work without Tree-sitter for this placeholder
            self._parser = None
        except Exception as e:
            print(f"Error initializing Python parser: {str(e)}")
            self._parser = None
    
    @property
    def language(self) -> str:
        """
        Get the language supported by this parser.
        
        Returns:
            Language name as string
        """
        return "python"
    
    @property
    def file_extensions(self) -> List[str]:
        """
        Get the file extensions supported by this parser.
        
        Returns:
            List of file extensions (without dot)
        """
        return ["py"]
    
    def parse(self, file_path: str) -> ParsedContent:
        """
        Parse a Python source code file.
        
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
        Extract imports from Python code.
        
        Args:
            content: Source code content
            
        Returns:
            List of import dictionaries
        """
        imports = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Match simple imports
            if line.startswith('import '):
                imports.append({
                    'statement': line,
                    'type': 'import',
                    'modules': [mod.strip() for mod in line[7:].split(',')]
                })
            
            # Match from imports
            elif line.startswith('from '):
                parts = line.split('import ')
                if len(parts) == 2:
                    from_module = parts[0].replace('from ', '').strip()
                    imported_items = [item.strip() for item in parts[1].split(',')]
                    imports.append({
                        'statement': line,
                        'type': 'from_import',
                        'from': from_module,
                        'imports': imported_items
                    })
        
        return imports
    
    def _extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract classes from Python code.
        
        Args:
            content: Source code content
            
        Returns:
            List of class dictionaries
        """
        classes = []
        
        # Simple regex pattern for class definitions
        class_pattern = r"class\s+(\w+)(?:\(([^)]*)\))?:"
        class_matches = re.finditer(class_pattern, content)
        
        for match in class_matches:
            class_name = match.group(1)
            parent_classes = match.group(2).split(',') if match.group(2) else []
            parent_classes = [p.strip() for p in parent_classes if p.strip()]
            
            # Extract docstring (simplified approach)
            class_start_pos = match.end()
            next_lines = content[class_start_pos:].split('\n')
            docstring = ""
            
            # Look for triple-quoted docstring
            for i, line in enumerate(next_lines):
                line = line.strip()
                if line.startswith('"""') or line.startswith("'''"):
                    end_quote = line[0:3]
                    docstring_lines = []
                    docstring_lines.append(line[3:])
                    
                    # Look for closing quote
                    if end_quote in line[3:]:
                        # Single line docstring
                        docstring = line[3:line.find(end_quote, 3)]
                        break
                    
                    # Multi-line docstring
                    for j, next_line in enumerate(next_lines[i+1:]):
                        if end_quote in next_line:
                            docstring_lines.append(next_line[:next_line.find(end_quote)])
                            break
                        docstring_lines.append(next_line)
                    
                    docstring = '\n'.join(docstring_lines)
                    break
            
            # Extract methods (simplified approach)
            methods = []
            method_pattern = r"(?:^|\n)\s+def\s+(\w+)\s*\(([^)]*)\)"
            class_content = content[class_start_pos:]
            method_matches = re.finditer(method_pattern, class_content)
            
            for method_match in method_matches:
                method_name = method_match.group(1)
                method_params = method_match.group(2).split(',')
                
                # Clean up parameters
                clean_params = []
                for param in method_params:
                    param = param.strip()
                    if param:
                        if param == 'self':
                            continue
                        param_parts = param.split('=')
                        param_name = param_parts[0].strip()
                        param_default = param_parts[1].strip() if len(param_parts) > 1 else None
                        
                        param_dict = {'name': param_name}
                        if param_default:
                            param_dict['default'] = param_default
                        
                        clean_params.append(param_dict)
                
                methods.append({
                    'name': method_name,
                    'params': clean_params
                })
            
            classes.append({
                'name': class_name,
                'parents': parent_classes,
                'docstring': docstring,
                'methods': methods
            })
        
        return classes
    
    def _extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract top-level functions from Python code.
        
        Args:
            content: Source code content
            
        Returns:
            List of function dictionaries
        """
        functions = []
        
        # Simple regex pattern for function definitions (top-level only)
        # Excludes indented functions (methods)
        func_pattern = r"(?:^|\n)def\s+(\w+)\s*\(([^)]*)\)"
        func_matches = re.finditer(func_pattern, content)
        
        for match in func_matches:
            func_name = match.group(1)
            func_params = match.group(2).split(',')
            
            # Clean up parameters
            clean_params = []
            for param in func_params:
                param = param.strip()
                if param:
                    param_parts = param.split('=')
                    param_name = param_parts[0].strip()
                    param_default = param_parts[1].strip() if len(param_parts) > 1 else None
                    
                    # Look for type annotations
                    if ':' in param_name:
                        name_type_parts = param_name.split(':')
                        param_name = name_type_parts[0].strip()
                        param_type = name_type_parts[1].strip()
                        
                        param_dict = {'name': param_name, 'type': param_type}
                    else:
                        param_dict = {'name': param_name}
                        
                    if param_default:
                        param_dict['default'] = param_default
                    
                    clean_params.append(param_dict)
            
            # Extract return type annotation (simplified)
            return_type = None
            lines = content[match.start():].split('\n')
            first_line = lines[0]
            if '->' in first_line:
                return_type = first_line.split('->')[1].split(':')[0].strip()
            
            # Extract docstring (simplified)
            func_start_pos = match.end()
            next_lines = content[func_start_pos:].split('\n')
            docstring = ""
            
            # Skip to function body
            for i, line in enumerate(next_lines):
                if ':' in line:
                    break
            
            # Look for docstring in function body
            for j, line in enumerate(next_lines[i+1:]):
                line = line.strip()
                if line.startswith('"""') or line.startswith("'''"):
                    end_quote = line[0:3]
                    docstring_lines = []
                    docstring_lines.append(line[3:])
                    
                    # Look for closing quote
                    if end_quote in line[3:]:
                        # Single line docstring
                        docstring = line[3:line.find(end_quote, 3)]
                        break
                    
                    # Multi-line docstring
                    for k, next_line in enumerate(next_lines[i+j+2:]):
                        if end_quote in next_line:
                            docstring_lines.append(next_line[:next_line.find(end_quote)])
                            break
                        docstring_lines.append(next_line)
                    
                    docstring = '\n'.join(docstring_lines)
                    break
            
            functions.append({
                'name': func_name,
                'params': clean_params,
                'return_type': return_type,
                'docstring': docstring
            })
        
        return functions
    
    def _extract_variables(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract top-level variables from Python code.
        
        Args:
            content: Source code content
            
        Returns:
            List of variable dictionaries
        """
        variables = []
        lines = content.split('\n')
        
        for line in lines:
            # Skip indented lines (not top-level)
            if line.startswith(' ') or line.startswith('\t'):
                continue
                
            # Skip imports, function/class definitions, comments
            if (line.startswith('import ') or line.startswith('from ') or
                line.startswith('def ') or line.startswith('class ') or
                line.strip().startswith('#')):
                continue
                
            # Look for assignments
            if '=' in line and not line.strip().startswith('#') and not '==' in line:
                # Skip function calls with assignment
                if '(' in line.split('=')[0]:
                    continue
                
                var_name = line.split('=')[0].strip()
                var_value = line.split('=')[1].strip()
                
                # Skip complex expressions or dictionary assignments
                if var_name.startswith('(') or var_name.startswith('[') or '{' in var_name:
                    continue
                
                # Extract type annotation if present
                var_type = None
                if ':' in var_name:
                    name_parts = var_name.split(':')
                    var_name = name_parts[0].strip()
                    var_type = name_parts[1].strip()
                
                # Only add if it's a simple variable name
                if var_name.isidentifier():
                    var_dict = {
                        'name': var_name,
                        'value': var_value
                    }
                    if var_type:
                        var_dict['type'] = var_type
                    
                    # Determine if constant (all caps)
                    if var_name.isupper():
                        var_dict['is_constant'] = True
                    
                    variables.append(var_dict)
        
        return variables

# Register the parser
register_parser(PythonParser)