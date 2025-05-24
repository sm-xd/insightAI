"""
Code Analyzer Agent for InsightAI.

This agent is responsible for analyzing code structures and patterns
to provide specialized insights about the codebase.
"""

from typing import Dict, List, Any, Optional
import logging

from .base_agent import BaseAgent
from parsers.parser_registry import get_parser_for_file
from rag.pipeline import RagPipeline

logger = logging.getLogger(__name__)

class CodeAnalyzerAgent(BaseAgent):
    """
    Agent specialized in code analysis.
    """
    
    def __init__(self, name: str = None, rag_pipeline: Optional[RagPipeline] = None):
        """
        Initialize the code analyzer agent.
        
        Args:
            name: Optional agent name
            rag_pipeline: Optional RAG pipeline instance
        """
        super().__init__(name or "CodeAnalyzer")
        self.rag_pipeline = rag_pipeline or RagPipeline()
    
    @property
    def agent_type(self) -> str:
        """
        Get the type of this agent.
        
        Returns:
            Agent type as string
        """
        return "code_analyzer"
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a code analysis task.
        
        Args:
            task: Task description and parameters
                - task_type: Type of analysis to perform
                - file_paths: List of file paths to analyze
                - codebase_path: Path to the codebase root
                - focus: Optional specific area to focus on
                
        Returns:
            Analysis results
        """
        logger.info(f"Processing task: {task.get('task_type')}")
        
        task_type = task.get("task_type")
        file_paths = task.get("file_paths", [])
        codebase_path = task.get("codebase_path")
        focus = task.get("focus")
        
        if task_type == "complexity_analysis":
            return await self._analyze_complexity(file_paths)
        elif task_type == "dependency_analysis":
            return await self._analyze_dependencies(file_paths, codebase_path)
        elif task_type == "pattern_detection":
            return await self._detect_patterns(file_paths)
        elif task_type == "tech_stack_analysis":
            return await self._analyze_tech_stack(codebase_path)
        else:
            return {
                "error": f"Unsupported task type: {task_type}",
                "status": "failed"
            }
    
    async def _analyze_complexity(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Analyze code complexity for given files.
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            Complexity analysis results
        """
        # Placeholder implementation
        results = {
            "file_complexity": {},
            "overall_complexity": "medium",
            "hotspots": []
        }
        
        for file_path in file_paths:
            parser = get_parser_for_file(file_path)
            if parser:
                try:
                    parsed = parser.parse(file_path)
                    
                    # Calculate simple complexity based on number of classes and functions
                    num_classes = len(parsed.classes)
                    num_functions = len(parsed.functions)
                    num_imports = len(parsed.imports)
                    
                    complexity_score = num_classes * 3 + num_functions * 2 + num_imports
                    
                    if complexity_score > 50:
                        complexity = "high"
                    elif complexity_score > 20:
                        complexity = "medium"
                    else:
                        complexity = "low"
                    
                    results["file_complexity"][file_path] = {
                        "score": complexity_score,
                        "level": complexity,
                        "metrics": {
                            "classes": num_classes,
                            "functions": num_functions,
                            "imports": num_imports
                        }
                    }
                    
                    # Add to hotspots if complexity is high
                    if complexity == "high":
                        results["hotspots"].append({
                            "file": file_path,
                            "score": complexity_score,
                            "reason": "High number of classes and functions"
                        })
                        
                except Exception as e:
                    logger.error(f"Error analyzing complexity for {file_path}: {str(e)}")
                    results["file_complexity"][file_path] = {
                        "error": str(e)
                    }
            else:
                results["file_complexity"][file_path] = {
                    "error": "No parser available for this file type"
                }
        
        return results
    
    async def _analyze_dependencies(self, file_paths: List[str], codebase_path: str) -> Dict[str, Any]:
        """
        Analyze dependencies between files.
        
        Args:
            file_paths: List of file paths to analyze
            codebase_path: Path to the codebase root
            
        Returns:
            Dependency analysis results
        """
        # Placeholder implementation
        dependencies = {
            "file_dependencies": {},
            "dependency_graph": {
                "nodes": [],
                "edges": []
            }
        }
        
        for file_path in file_paths:
            parser = get_parser_for_file(file_path)
            if parser:
                try:
                    parsed = parser.parse(file_path)
                    imports = parsed.imports
                    
                    file_deps = []
                    for imp in imports:
                        # Very simplified import resolution
                        if "statement" in imp:
                            file_deps.append({
                                "import_statement": imp["statement"],
                                "type": imp.get("type", "unknown")
                            })
                    
                    dependencies["file_dependencies"][file_path] = file_deps
                    
                    # Add node to dependency graph
                    dependencies["dependency_graph"]["nodes"].append({
                        "id": file_path,
                        "label": file_path.replace(codebase_path, "").lstrip("/\\"),
                        "type": parser.language
                    })
                    
                    # Add edges to dependency graph (simplified)
                    for dep in file_deps:
                        dependencies["dependency_graph"]["edges"].append({
                            "source": file_path,
                            "target": dep["import_statement"],
                            "type": dep["type"]
                        })
                        
                except Exception as e:
                    logger.error(f"Error analyzing dependencies for {file_path}: {str(e)}")
                    dependencies["file_dependencies"][file_path] = {
                        "error": str(e)
                    }
            else:
                dependencies["file_dependencies"][file_path] = {
                    "error": "No parser available for this file type"
                }
        
        return dependencies
    
    async def _detect_patterns(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Detect common patterns in code.
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            Pattern detection results
        """
        # Placeholder implementation
        return {
            "patterns_detected": {
                "design_patterns": [],
                "anti_patterns": [],
                "custom_patterns": []
            },
            "status": "Placeholder implementation - actual pattern detection not implemented yet"
        }
    
    async def _analyze_tech_stack(self, codebase_path: str) -> Dict[str, Any]:
        """
        Analyze the technology stack used in the codebase.
        
        Args:
            codebase_path: Path to the codebase root
            
        Returns:
            Tech stack analysis results
        """
        # Placeholder implementation
        return {
            "tech_stack": {
                "languages": {},
                "frameworks": [],
                "libraries": [],
                "tools": []
            },
            "status": "Placeholder implementation - actual tech stack detection not implemented yet"
        }