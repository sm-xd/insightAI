"""
Tests for code analysis plugins.
"""

import unittest
from textwrap import dedent

from parsers.plugins.complexity_analyzer import ComplexityAnalyzerPlugin
from parsers.base_parser import ParsedContent

class TestComplexityAnalyzer(unittest.TestCase):
    """Test cases for complexity analyzer plugin."""
    
    def setUp(self):
        """Set up test environment."""
        self.plugin = ComplexityAnalyzerPlugin()
    
    def test_cyclomatic_complexity(self):
        """Test cyclomatic complexity calculation."""
        code = dedent('''
            function complexFunction(a, b) {
                if (a > 0) {
                    if (b > 0) {
                        return a + b;
                    } else {
                        return a - b;
                    }
                } else if (b > 0) {
                    return b;
                }
                return 0;
            }
        ''')
        
        complexity = self.plugin._calculate_cyclomatic_complexity(code)
        self.assertGreater(complexity, 1)  # Should have multiple paths
    
    def test_nesting_depth(self):
        """Test nesting depth calculation."""
        code = dedent('''
            function deeplyNested() {
                if (true) {
                    while (true) {
                        if (true) {
                            console.log("deep");
                        }
                    }
                }
            }
        ''')
        
        depth = self.plugin._calculate_nesting_depth(code)
        self.assertEqual(depth, 3)  # 3 levels deep
    
    def test_cognitive_complexity(self):
        """Test cognitive complexity calculation."""
        code = dedent('''
            function cognitive(a, b) {
                return a > b ? a && b : a || b;
            }
        ''')
        
        complexity = self.plugin._calculate_cognitive_complexity(code)
        self.assertGreater(complexity, 0)  # Has ternary and logical operators
    
    def test_function_analysis(self):
        """Test function analysis."""
        content = ParsedContent(
            file_path="test.js",
            language="javascript",
            imports=[],
            classes=[],
            functions=[
                {
                    "name": "simpleFunc",
                    "params": ["a", "b"]
                }
            ],
            variables=[],
            raw_content=dedent('''
                function simpleFunc(a, b) {
                    return a + b;
                }
            ''')
        )
        
        metrics = self.plugin._analyze_functions(content)
        self.assertEqual(len(metrics), 1)
        self.assertEqual(metrics[0]["name"], "simpleFunc")
        self.assertFalse(metrics[0]["is_complex"])
    
    def test_class_analysis(self):
        """Test class analysis."""
        content = ParsedContent(
            file_path="test.js",
            language="javascript",
            imports=[],
            classes=[
                {
                    "name": "SimpleClass",
                    "methods": [
                        {"name": "method1"},
                        {"name": "method2"}
                    ]
                }
            ],
            functions=[],
            variables=[],
            raw_content=dedent('''
                class SimpleClass {
                    method1() {
                        return true;
                    }
                    method2() {
                        return false;
                    }
                }
            ''')
        )
        
        metrics = self.plugin._analyze_classes(content)
        self.assertEqual(len(metrics), 1)
        self.assertEqual(metrics[0]["name"], "SimpleClass")
        self.assertEqual(metrics[0]["method_count"], 2)
    
    def test_full_analysis(self):
        """Test complete code analysis."""
        content = ParsedContent(
            file_path="test.js",
            language="javascript",
            imports=[],
            classes=[
                {
                    "name": "TestClass",
                    "methods": [
                        {"name": "complexMethod"}
                    ]
                }
            ],
            functions=[
                {
                    "name": "helperFunction",
                    "params": ["x"]
                }
            ],
            variables=[],
            raw_content=dedent('''
                class TestClass {
                    complexMethod() {
                        if (true) {
                            while (true) {
                                console.log("deep");
                            }
                        }
                    }
                }
                
                function helperFunction(x) {
                    return x > 0 ? x : -x;
                }
            ''')
        )
        
        results = self.plugin.analyze(content)
        
        self.assertIn("metrics", results)
        self.assertIn("summary", results)
        self.assertIn("recommendations", results)
        
        metrics = results["metrics"]
        self.assertIn("cyclomatic_complexity", metrics)
        self.assertIn("max_nesting_depth", metrics)
        self.assertIn("cognitive_complexity", metrics)
        self.assertGreater(len(results["recommendations"]), 0)

if __name__ == "__main__":
    unittest.main()