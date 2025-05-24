"""
Backend package for InsightAI.
"""

__version__ = "0.1.0"

from .main import app
from .config import settings

__all__ = ["app", "settings"]