"""Configuration module for the Workwize MCP server."""
import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Configuration class for the Workwize MCP server."""
    api_base_url: str = os.getenv('WORKWIZE_API_URL', 'https://prod-back.goworkwize.com/api/public')
    api_token: Optional[str] = os.getenv('WORKWIZE_API_TOKEN')

    def __post_init__(self):
        """Validate configuration."""
        if not self.api_token:
            raise ValueError("WORKWIZE_API_TOKEN environment variable is required")

config = Config()
