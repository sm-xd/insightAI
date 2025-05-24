"""
Code complexity analysis plugin.
"""

from typing import Dict, Any, List
import re
from .base_plugin import BasePlugin
from ..base_parser import ParsedContent
from . import plugin_manager

class ComplexityAnalyzerPlugin(BasePlugin):
    """Plugin for analyzing code complexity."""
    
    @property
    def plugin_id(self) -> str:
        return "complexity_analyzer"
    
    @property
    def name(self) -> str:
        return "Code Complexity Analyzer"
    
    @property
    def description(self) -> str:
        return "Analyzes code complexity metrics including cyclomatic complexity and nesting depth"
    
    @property
    def supported_languages(self) -> List[str]:
        return ["python", "javascript"]
    
    def analyze(self, content: ParsedContent) -> Dict[str, Any]:
        """Analyze code complexity."""
        metrics = {
            'cyclomatic_complexity': self._calculate_cyclomatic_complexity(content.raw_content),
            'max_nesting_depth': self._calculate_nesting_depth(content.raw_content),
            'cognitive_complexity': self._calculate_cognitive_complexity(content.raw_content),
            'function_metrics': self._analyze_functions(content),
            'class_metrics': self._analyze_classes(content)
        }
        
        return {
            'metrics': metrics,
            'summary': self._generate_summary(metrics),
            'recommendations': self._generate_recommendations(metrics)
        }
    
    def _calculate_cyclomatic_complexity(self, code: str) -> int:
        """Calculate cyclomatic complexity."""
        # Count decision points (if, while, for, and, or, etc.)
        decision_points = len(re.findall(
            r'\b(if|while|for|and|or)\b|&&|\|\||\?|catch\b',
            code
        ))
        
        # Add 1 for the base path
        return decision_points + 1
    
    def _calculate_nesting_depth(self, code: str) -> int:
        """Calculate maximum nesting depth."""
        lines = code.split('\n')
        max_depth = 0
        current_depth = 0
        
        for line in lines:
            # Count leading spaces/tabs
            indent = len(line) - len(line.lstrip())
            
            # Assuming 4 spaces or 1 tab per indent level
            depth = indent // 4 if indent > 0 else 0
            
            current_depth = depth
            max_depth = max(max_depth, current_depth)
        
        return max_depth
    
    def _calculate_cognitive_complexity(self, code: str) -> int:
        """Calculate cognitive complexity."""
        # This is a simplified version
        cognitive_score = 0
        
        # Count control flow structures
        control_structures = len(re.findall(
            r'\b(if|else|while|for|switch|catch)\b',
            code
        ))
        
        # Count logical operators
        logical_operators = len(re.findall(r'&&|\|\|', code))
        
        # Count ternary operators
        ternary_operators = len(re.findall(r'\?.*:(?![^{]*})', code))
        
        # Add weights
        cognitive_score += control_structures * 2  # Weight: 2
        cognitive_score += logical_operators      # Weight: 1
        cognitive_score += ternary_operators * 3  # Weight: 3
        
        return cognitive_score
    
    def _analyze_functions(self, content: ParsedContent) -> List[Dict[str, Any]]:
        """Analyze complexity metrics for each function."""
        function_metrics = []
        
        for func in content.functions:
            # Extract function body - in a real implementation, this would be more robust
            func_pattern = f"function\\s+{func['name']}.*?\\{{(.*?)\\}}"
            match = re.search(func_pattern, content.raw_content, re.DOTALL)
            
            if match:
                func_body = match.group(1)
                metrics = {
                    'name': func['name'],
                    'cyclomatic_complexity': self._calculate_cyclomatic_complexity(func_body),
                    'nesting_depth': self._calculate_nesting_depth(func_body),
                    'cognitive_complexity': self._calculate_cognitive_complexity(func_body),
                    'parameter_count': len(func.get('params', [])),
                    'is_complex': False  # Will be set below
                }
                
                # Determine if function is complex
                metrics['is_complex'] = (
                    metrics['cyclomatic_complexity'] > 10 or
                    metrics['nesting_depth'] > 3 or
                    metrics['cognitive_complexity'] > 15 or
                    metrics['parameter_count'] > 4
                )
                
                function_metrics.append(metrics)
        
        return function_metrics
    
    def _analyze_classes(self, content: ParsedContent) -> List[Dict[str, Any]]:
        """Analyze complexity metrics for each class."""
        class_metrics = []
        
        for cls in content.classes:
            metrics = {
                'name': cls['name'],
                'method_count': len(cls.get('methods', [])),
                'average_method_complexity': 0,
                'complex_methods': []
            }
            
            # Analyze methods
            total_complexity = 0
            for method in cls.get('methods', []):
                # Extract method body - in a real implementation, this would be more robust
                method_pattern = f"{method['name']}.*?\\{{(.*?)\\}}"
                match = re.search(method_pattern, content.raw_content, re.DOTALL)
                
                if match:
                    method_body = match.group(1)
                    complexity = self._calculate_cyclomatic_complexity(method_body)
                    total_complexity += complexity
                    
                    if complexity > 10:
                        metrics['complex_methods'].append(method['name'])
            
            if metrics['method_count'] > 0:
                metrics['average_method_complexity'] = (
                    total_complexity / metrics['method_count']
                )
            
            class_metrics.append(metrics)
        
        return class_metrics
    
    def _generate_summary(self, metrics: Dict[str, Any]) -> str:
        """Generate a summary of the analysis."""
        complex_functions = sum(
            1 for f in metrics['function_metrics']
            if f['is_complex']
        )
        
        total_functions = len(metrics['function_metrics'])
        total_classes = len(metrics['class_metrics'])
        
        return (
            f"Analysis found {complex_functions} complex functions out of {total_functions} "
            f"total functions across {total_classes} classes. Overall cyclomatic "
            f"complexity is {metrics['cyclomatic_complexity']} with maximum nesting "
            f"depth of {metrics['max_nesting_depth']}."
        )
    
    def _generate_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        if metrics['cyclomatic_complexity'] > 20:
            recommendations.append(
                "Consider breaking down complex logic into smaller functions"
            )
        
        if metrics['max_nesting_depth'] > 3:
            recommendations.append(
                "Reduce nesting depth by extracting deeply nested code into functions"
            )
        
        complex_functions = [
            f['name'] for f in metrics['function_metrics']
            if f['is_complex']
        ]
        
        if complex_functions:
            recommendations.append(
                f"Simplify complex functions: {', '.join(complex_functions)}"
            )
        
        for cls in metrics['class_metrics']:
            if cls['average_method_complexity'] > 10:
                recommendations.append(
                    f"Class {cls['name']} has high average complexity. "
                    "Consider splitting into smaller classes."
                )
        
        return recommendations

# Register the plugin
plugin_manager.register_plugin(ComplexityAnalyzerPlugin)