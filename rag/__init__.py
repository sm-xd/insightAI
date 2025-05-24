"""
RAG (Retrieval-Augmented Generation) package for InsightAI.

This package implements the core RAG functionality using LangChain,
combining retrieved context with role-specific prompts.
"""

__version__ = "0.1.0"

from .role_manager import RoleManager
from .pipeline import RagPipeline

__all__ = ["RoleManager", "RagPipeline"]