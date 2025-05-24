"""
RAG (Retrieval Augmented Generation) package for InsightAI.
"""

from .pipeline import RagPipeline
from .role_manager import RoleManager

__all__ = ['RagPipeline', 'RoleManager']