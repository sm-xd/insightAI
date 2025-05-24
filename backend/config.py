"""
Configuration settings for InsightAI backend.
"""

import os
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings."""
    
    def __init__(self):
        """Initialize settings."""
        # Server settings
        self.debug = os.getenv("DEBUG", "True").lower() == "true"
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "8000"))
        self.workers = int(os.getenv("WORKERS", "4"))
          # API keys
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Storage settings
        self.storage_path = Path(os.getenv("STORAGE_PATH", "./storage"))
        self.upload_dir = self.storage_path / "uploads"
        self.vector_db_path = self.storage_path / "vector_db"
        
        # Ensure storage directories exist
        self.storage_path.mkdir(exist_ok=True)
        self.upload_dir.mkdir(exist_ok=True)
        self.vector_db_path.mkdir(exist_ok=True)
        
        # Limits
        self.max_upload_size = int(os.getenv("MAX_UPLOAD_SIZE_MB", "100")) * 1024 * 1024
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4000"))
        self.request_timeout = int(os.getenv("REQUEST_TIMEOUT", "300"))
        
        # CORS settings
        self.cors_origins = [
            "http://localhost:3000",  # React dev server
            "http://localhost:8000",  # FastAPI dev server
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert settings to dictionary.
        
        Returns:
            Dictionary of settings
        """
        return {
            "debug": self.debug,
            "host": self.host,
            "port": self.port,
            "workers": self.workers,
            "storage_path": str(self.storage_path),
            "upload_dir": str(self.upload_dir),
            "vector_db_path": str(self.vector_db_path),
            "max_upload_size": self.max_upload_size,
            "max_tokens": self.max_tokens,
            "request_timeout": self.request_timeout,
            "cors_origins": self.cors_origins
        }

# Create global settings instance
settings = Settings()