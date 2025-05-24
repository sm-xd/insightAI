"""
Tests for code parsers.
"""

import os
import unittest
import tempfile
from textwrap import dedent

from parsers.base_parser import ParsedContent
from parsers.languages.javascript_parser import JavaScriptParser
from parsers.parser_registry import get_parser_for_file, get_parser_for_language


class TestParsers(unittest.TestCase):
    """Test cases for code parsers."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temp directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_files = {}
        
        # Create a sample Python file
        py_content = """
import os
import sys

def hello_world():
    \"\"\"Say hello to the world.\"\"\"
    print("Hello, World!")
    
class Calculator:
    \"\"\"A simple calculator class.\"\"\"
    
    def __init__(self):
        self.value = 0
        
    def add(self, x):
        \"\"\"Add a number to the current value.\"\"\"
        self.value += x
        return self.value
        
if __name__ == "__main__":
    hello_world()
    calc = Calculator()
    result = calc.add(5)
    print(f"Result: {result}")
"""
        py_path = os.path.join(self.temp_dir.name, "test_sample.py")
        with open(py_path, 'w') as f:
            f.write(py_content)
        self.test_files["python"] = py_path
        
        # Create a sample JavaScript file
        js_content = """
import { Component } from 'react';
const axios = require('axios');

// Constants
const API_URL = 'https://api.example.com';

// Helper function
function formatResponse(data) {
  return {
    id: data.id,
    name: data.name,
    timestamp: new Date()
  };
}

class ApiClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl || API_URL;
  }
  
  async fetchData(endpoint) {
    try {
      const response = await axios.get(`${this.baseUrl}/${endpoint}`);
      return formatResponse(response.data);
    } catch (error) {
      console.error('API error:', error);
      return null;
    }
  }
}

// Export the client
export default new ApiClient();
"""
        js_path = os.path.join(self.temp_dir.name, "api_client.js")
        with open(js_path, 'w') as f:
            f.write(js_content)
        self.test_files["javascript"] = js_path
    
    def tearDown(self):
        """Clean up after tests."""
        self.temp_dir.cleanup()
    
    def test_get_parser_for_file(self):
        """Test getting the correct parser for a file."""
        python_parser = get_parser_for_file(self.test_files["python"])
        self.assertIsNotNone(python_parser, "Should get a parser for Python files")
        if python_parser:
            self.assertEqual(python_parser.language, "python")
        
        js_parser = get_parser_for_file(self.test_files["javascript"])
        self.assertIsNotNone(js_parser, "Should get a parser for JavaScript files")
        if js_parser:
            self.assertEqual(js_parser.language, "javascript")
    
    def test_python_parser(self):
        """Test Python parser functionality."""
        python_parser = get_parser_for_language("python")
        if not python_parser:
            self.skipTest("Python parser not available")
        
        parsed = python_parser.parse(self.test_files["python"])
        
        self.assertIsInstance(parsed, ParsedContent)
        self.assertEqual(parsed.language, "python")
        
        # Check imports
        self.assertGreaterEqual(len(parsed.imports), 2)
        import_modules = [imp["statement"] for imp in parsed.imports]
        self.assertIn("import os", import_modules)
        self.assertIn("import sys", import_modules)
        
        # Check functions
        self.assertGreaterEqual(len(parsed.functions), 1)
        func_names = [func["name"] for func in parsed.functions]
        self.assertIn("hello_world", func_names)
        
        # Check classes
        self.assertGreaterEqual(len(parsed.classes), 1)
        class_names = [cls["name"] for cls in parsed.classes]
        self.assertIn("Calculator", class_names)
    
    def test_javascript_parser(self):
        """Test JavaScript parser functionality."""
        js_parser = get_parser_for_language("javascript")
        if not js_parser:
            self.skipTest("JavaScript parser not available")
        
        parsed = js_parser.parse(self.test_files["javascript"])
        
        self.assertIsInstance(parsed, ParsedContent)
        self.assertEqual(parsed.language, "javascript")
        
        # Check imports
        self.assertGreaterEqual(len(parsed.imports), 1)
        
        # Check functions
        self.assertGreaterEqual(len(parsed.functions), 1)
        func_names = [func["name"] for func in parsed.functions]
        self.assertIn("formatResponse", func_names)
        
        # Check classes
        self.assertGreaterEqual(len(parsed.classes), 1)
        class_names = [cls["name"] for cls in parsed.classes]
        self.assertIn("ApiClient", class_names)


class TestJavaScriptParser(unittest.TestCase):
    """Test cases for JavaScript parser."""
    
    def setUp(self):
        """Set up test environment."""
        self.parser = JavaScriptParser()
    
    def test_parser_registration(self):
        """Test parser registration and lookup."""
        test_files = [
            ('test.js', True),
            ('test.jsx', True),
            ('test.ts', True),
            ('test.tsx', True),
            ('test.py', False),
            ('test.txt', False)
        ]
        
        for file_path, should_match in test_files:
            parser = get_parser_for_file(file_path)
            if should_match:
                self.assertIsInstance(parser, JavaScriptParser)
            else:
                self.assertNotIsInstance(parser, JavaScriptParser)
    
    def test_extract_imports(self):
        """Test extracting imports."""
        code = dedent('''
            import React from 'react';
            import { useState, useEffect } from 'react';
            import * as utils from './utils';
            const axios = require('axios');
        ''')
        
        imports = self.parser._extract_imports(code)
        
        self.assertEqual(len(imports), 4)
        self.assertEqual(imports[0]['module'], 'react')
        self.assertEqual(imports[1]['module'], 'react')
        self.assertEqual(imports[2]['module'], './utils')
        self.assertEqual(imports[3]['module'], 'axios')
    
    def test_extract_classes(self):
        """Test extracting classes."""
        code = dedent('''
            class MyComponent extends React.Component {
                constructor(props) {
                    super(props);
                    this.state = {};
                }
                
                async fetchData() {
                    return await fetch('/api/data');
                }
                
                render() {
                    return <div>Hello</div>;
                }
            }
        ''')
        
        classes = self.parser._extract_classes(code)
        
        self.assertEqual(len(classes), 1)
        self.assertEqual(classes[0]['name'], 'MyComponent')
        self.assertEqual(classes[0]['parent'], 'React.Component')
        
        methods = classes[0]['methods']
        self.assertEqual(len(methods), 3)
        self.assertEqual(methods[0]['name'], 'constructor')
        self.assertEqual(methods[1]['name'], 'fetchData')
        self.assertTrue(methods[1]['is_async'])
        self.assertEqual(methods[2]['name'], 'render')
    
    def test_extract_functions(self):
        """Test extracting functions."""
        code = dedent('''
            function greet(name = 'world') {
                return `Hello ${name}`;
            }
            
            const add = (a, b) => a + b;
            
            async function fetchData() {
                return await fetch('/api/data');
            }
        ''')
        
        functions = self.parser._extract_functions(code)
        
        self.assertEqual(len(functions), 3)
        self.assertEqual(functions[0]['name'], 'greet')
        self.assertEqual(functions[0]['params'][0]['name'], 'name')
        self.assertEqual(functions[0]['params'][0]['default'], "'world'")
        
        self.assertEqual(functions[1]['name'], 'add')
        self.assertEqual(len(functions[1]['params']), 2)
        
        self.assertEqual(functions[2]['name'], 'fetchData')
        self.assertTrue(functions[2]['is_async'])
    
    def test_extract_variables(self):
        """Test extracting variables."""
        code = dedent('''
            const PI = 3.14159;
            let count = 0;
            var name = 'test';
            const fn = () => {};  // Should be ignored
        ''')
        
        variables = self.parser._extract_variables(code)
        
        self.assertEqual(len(variables), 3)
        self.assertEqual(variables[0]['name'], 'PI')
        self.assertEqual(variables[0]['value'], '3.14159')
        self.assertEqual(variables[0]['kind'], 'const')
        
        self.assertEqual(variables[1]['name'], 'count')
        self.assertEqual(variables[1]['value'], '0')
        self.assertEqual(variables[1]['kind'], 'let')
        
        self.assertEqual(variables[2]['name'], 'name')
        self.assertEqual(variables[2]['value'], "'test'")
        self.assertEqual(variables[2]['kind'], 'var')


if __name__ == '__main__':
    unittest.main()