"""
Base Parser implementation for InsightAI.

This module defines the base parser interface and common functionality
for all language-specific parsers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import os

from langchain.schema import Document

@dataclass
class ParsedContent:
    """
    Container for parsed file content.
    
    Attributes:
        file_path: Path to the original file
        language: Programming language of the file
        imports: List of imports/includes/requires
        classes: List of classes with methods and properties
        functions: List of top-level functions
        variables: List of top-level variables/constants
        ast: The Abstract Syntax Tree (optional)
        raw_content: The raw file content
    """
    file_path: str
    language: str
    imports: List[Dict[str, Any]]
    classes: List[Dict[str, Any]]
    functions: List[Dict[str, Any]]
    variables: List[Dict[str, Any]]
    ast: Optional[Any] = None
    raw_content: Optional[str] = None
    
    def to_documents(self) -> List[Document]:
        """
        Convert parsed content to LangChain documents for indexing.
        
        Returns:
            List of Document objects
        """
        documents = []
        
        # Create a document for the overall file
        file_meta = {
            "source": self.file_path,
            "language": self.language,
            "type": "file",
            "filename": os.path.basename(self.file_path)
        }
        
        # If we have raw content, create a document for it
        if self.raw_content:
            documents.append(Document(
                page_content=self.raw_content,
                metadata=file_meta
            ))
        
        # Create documents for each class
        for cls in self.classes:
            cls_content = f"Class: {cls['name']}\n\n"
            
            if 'docstring' in cls and cls['docstring']:
                cls_content += f"Description: {cls['docstring']}\n\n"
                
            if 'methods' in cls:
                cls_content += "Methods:\n"
                for method in cls['methods']:
                    cls_content += f"- {method['name']}"
                    if 'params' in method:
                        params = ', '.join([p['name'] for p in method['params']])
                        cls_content += f"({params})"
                    cls_content += "\n"
                    
                    if 'docstring' in method and method['docstring']:
                        cls_content += f"  {method['docstring']}\n"
                        
            cls_meta = {
                **file_meta,
                "type": "class",
                "class": cls['name']
            }
            
            documents.append(Document(
                page_content=cls_content,
                metadata=cls_meta
            ))
        
        # Create documents for each function
        for func in self.functions:
            func_content = f"Function: {func['name']}\n\n"
            
            if 'docstring' in func and func['docstring']:
                func_content += f"Description: {func['docstring']}\n\n"
                
            if 'params' in func:
                func_content += "Parameters:\n"
                for param in func['params']:
                    func_content += f"- {param['name']}"
                    if 'type' in param:
                        func_content += f" ({param['type']})"
                    if 'default' in param:
                        func_content += f" = {param['default']}"
                    func_content += "\n"
            
            if 'return_type' in func and func['return_type']:
                func_content += f"\nReturns: {func['return_type']}\n"
                
            func_meta = {
                **file_meta,
                "type": "function",
                "function": func['name']
            }
            
            documents.append(Document(
                page_content=func_content,
                metadata=func_meta
            ))
            
        return documents


class BaseParser(ABC):
    """
    Abstract base class for language-specific parsers.
    """
    
    @property
    @abstractmethod
    def language(self) -> str:
        """
        Get the language supported by this parser.
        
        Returns:
            Language name as string
        """
        pass
    
    @property
    @abstractmethod
    def file_extensions(self) -> List[str]:
        """
        Get the file extensions supported by this parser.
        
        Returns:
            List of file extensions (without dot)
        """
        pass
    
    @abstractmethod
    def parse(self, file_path: str) -> ParsedContent:
        """
        Parse a source code file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            ParsedContent: Structured content from the file
        """
        pass
    
    def can_parse(self, file_path: str) -> bool:
        """
        Check if this parser can handle a given file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if this parser can handle the file, False otherwise
        """
        extension = os.path.splitext(file_path)[1][1:].lower()
        return extension in self.file_extensions