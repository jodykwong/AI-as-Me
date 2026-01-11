"""Configuration management for AI-as-Me."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class Config(BaseModel):
    """Application configuration."""
    
    api_key: str = Field(..., description="DeepSeek API key")
    api_base: str = Field(default="https://api.deepseek.com/v1", description="API base URL")
    model: str = Field(default="deepseek-chat", description="Model name")
    
    # Clarification settings
    skip_clarification: bool = Field(default=True, description="Skip clarification by default")
    
    # Paths
    project_root: Path = Field(default_factory=lambda: Path.cwd())
    soul_dir: Path = Field(default_factory=lambda: Path.cwd() / "soul")
    kanban_dir: Path = Field(default_factory=lambda: Path.cwd() / "kanban")
    logs_dir: Path = Field(default_factory=lambda: Path.cwd() / "logs")
    
    model_config = {"arbitrary_types_allowed": True}


def load_config(env_file: Optional[Path] = None) -> Config:
    """Load configuration from environment variables.
    
    Args:
        env_file: Optional path to .env file
        
    Returns:
        Config object
        
    Raises:
        ValueError: If required configuration is missing
    """
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError(
            "DEEPSEEK_API_KEY not found in environment.\n"
            "Please create a .env file with:\n"
            "DEEPSEEK_API_KEY=your_api_key_here"
        )
    
    return Config(
        api_key=api_key,
        api_base=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1"),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        skip_clarification=os.getenv("SKIP_CLARIFICATION", "true").lower() == "true",
    )
