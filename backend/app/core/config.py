"""Configuration management for SlideForge backend."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Summarization settings
    summarizer_backend: str = Field(
        default="textrank",
        description="Summarization backend (textrank, hf_transformer)"
    )
    hf_model_name: Optional[str] = Field(
        default="sshleifer/distilbart-cnn-12-6",
        description="Hugging Face model for summarization"
    )
    hf_cache_dir: str = Field(
        default="./models",
        description="Hugging Face model cache directory"
    )
    
    # Network and API settings
    enable_network_metadata: bool = Field(
        default=True,
        description="Enable network metadata fetching"
    )
    crossref_api_url: str = Field(
        default="https://api.crossref.org/works/",
        description="Crossref API URL"
    )
    semantic_scholar_api_url: str = Field(
        default="https://api.semanticscholar.org/v1/paper/",
        description="Semantic Scholar API URL"
    )
    
    # File storage settings
    upload_dir: str = Field(
        default="./uploads",
        description="Directory for uploaded files"
    )
    output_dir: str = Field(
        default="./outputs",
        description="Directory for generated files"
    )
    temp_dir: str = Field(
        default="./temp",
        description="Directory for temporary files"
    )
    
    # Logging settings
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    log_format: str = Field(
        default="json",
        description="Logging format (json, text)"
    )
    
    # Server settings
    host: str = Field(
        default="0.0.0.0",
        description="Server host"
    )
    port: int = Field(
        default=8000,
        description="Server port"
    )
    debug: bool = Field(
        default=False,
        description="Debug mode"
    )
    
    # CORS settings
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Allowed CORS origins"
    )
    
    # Security settings
    secret_key: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Secret key for security"
    )
    
    def __init__(self, **kwargs):
        """Initialize settings and create directories."""
        super().__init__(**kwargs)
        self._create_directories()
    
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            Path(self.upload_dir),
            Path(self.output_dir),
            Path(self.temp_dir),
            Path(self.hf_cache_dir)
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Get allowed origins as a list."""
        if isinstance(self.allowed_origins, str):
            try:
                return json.loads(self.allowed_origins)
            except json.JSONDecodeError:
                return [self.allowed_origins]
        return self.allowed_origins


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
