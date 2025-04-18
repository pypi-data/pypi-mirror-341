"""Configuration management for Task Blaster."""

import os
from pathlib import Path
from typing import Dict, Optional, Annotated

from pydantic import BaseModel, Field, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

CLAUDE_MODEL = os.getenv("MODEL")


class Config(BaseSettings):
    """Main configuration settings."""

    # Model Settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # AI Service Settings
    anthropic_api_key: Optional[str] = Field(
        None,
        env="ANTHROPIC_API_KEY",
        description="API key for direct Anthropic/Claude services"
    )
    
    # AWS Bedrock Settings
    use_bedrock: bool = Field(
        False,
        env="USE_BEDROCK",
        description="Whether to use AWS Bedrock for Claude"
    )
    aws_access_key: Optional[str] = Field(
        None,
        env="AWS_ACCESS_KEY_ID",
        description="AWS access key for Bedrock"
    )
    aws_secret_key: Optional[str] = Field(
        None,
        env="AWS_SECRET_ACCESS_KEY",
        description="AWS secret key for Bedrock"
    )
    aws_session_token: Optional[str] = Field(
        None,
        env="AWS_SESSION_TOKEN",
        description="AWS session token for temporary credentials"
    )
    aws_region: str = Field(
        "us-east-1",
        env="AWS_REGION",
        description="AWS region for Bedrock"
    )
    
    # Perplexity Settings
    perplexity_api_key: Optional[str] = Field(
        None,
        env="PERPLEXITY_API_KEY",
        description="API key for Perplexity AI services"
    )
    perplexity_model: str = Field(
        "sonar-pro",
        env="PERPLEXITY_MODEL",
        description="Model to use for Perplexity AI"
    )
    # Model Settings
    claude_model: str = Field(
        os.getenv("MODEL"),
        env="CLAUDE_MODEL",
        description="Model to use for Claude AI"
    )
    
    # Task Generation Settings
    max_tokens: int = Field(
        4000,
        env="MAX_TOKENS",
        ge=1,
        le=100000,
        description="Maximum tokens for AI responses"
    )
    temperature: float = Field(
        0.7,
        env="TEMPERATURE",
        ge=0.0,
        le=1.0,
        description="Temperature for AI responses"
    )
    default_subtasks: int = Field(
        5,
        env="DEFAULT_SUBTASKS",
        ge=1,
        le=20,
        description="Default number of subtasks to generate"
    )
    
    # File Paths
    tasks_dir: Path = Field(
        default_factory=lambda: Path("tasks"),
        description="Directory for task files"
    )
    output_file: Path = Field(
        default_factory=lambda: Path("output.json"),
        description="Path for output JSON file"
    )
    
    # Debug Settings
    debug: bool = Field(
        False,
        env="DEBUG",
        description="Enable debug mode"
    )
    
    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
    
    def has_aws_credentials(self) -> bool:
        """Check if AWS credentials are available.
        
        Returns:
            True if AWS credentials are available either through environment
            variables or AWS credential file
        """
        # Check environment variables
        if self.aws_access_key and self.aws_secret_key:
            return True
        
        # Check AWS credentials file
        aws_creds_file = os.path.expanduser("~/.aws/credentials")
        return os.path.exists(aws_creds_file)
    
    def validate_ai_config(self) -> Dict[str, bool]:
        """Validate AI service configuration.
        
        Returns:
            Dictionary indicating which services are available
        """
        services = {
            "claude_direct": False,
            "claude_bedrock": False,
            "perplexity": False
        }
        
        # Check direct Claude access
        if self.anthropic_api_key:
            services["claude_direct"] = True
        
        # Check AWS Bedrock access
        if self.use_bedrock and self.has_aws_credentials():
            services["claude_bedrock"] = True
        
        # Check Perplexity access
        if self.perplexity_api_key:
            services["perplexity"] = True
        
        return services


class TaskStatus:
    """Task status constants."""
    
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"
    
    _VALID_STATUSES = {PENDING, IN_PROGRESS, DONE, BLOCKED}
    
    @classmethod
    def is_valid(cls, status: str) -> bool:
        """Check if a status is valid."""
        return status in cls._VALID_STATUSES
    
    @classmethod
    def get_valid_statuses(cls) -> set:
        """Get set of valid statuses."""
        return cls._VALID_STATUSES.copy()


class TaskPriority:
    """Task priority constants."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
    _VALID_PRIORITIES = {LOW, MEDIUM, HIGH}
    
    @classmethod
    def is_valid(cls, priority: str) -> bool:
        """Check if a priority is valid."""
        return priority in cls._VALID_PRIORITIES
    
    @classmethod
    def get_valid_priorities(cls) -> set:
        """Get set of valid priorities."""
        return cls._VALID_PRIORITIES.copy()


# Create a global config instance
config = Config()

# Ensure required directories exist
config.ensure_directories()

# Validate AI configuration
available_services = config.validate_ai_config()

# Only show warning if no Claude service is available
if not (available_services["claude_direct"] or available_services["claude_bedrock"]):
    import warnings
    warnings.warn(
        "No Claude AI service is available. Please either:\n"
        "1. Set ANTHROPIC_API_KEY for direct Claude access, or\n"
        "2. Set USE_BEDROCK=true and configure AWS credentials for Bedrock access"
    )