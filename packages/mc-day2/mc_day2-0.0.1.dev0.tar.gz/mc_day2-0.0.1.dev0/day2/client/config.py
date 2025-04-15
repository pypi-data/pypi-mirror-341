"""Configuration for the MontyCloud SDK."""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Config:
    """Configuration for the MontyCloud SDK."""

    # Base URL for the MontyCloud API
    base_url: str = "https://stg1-api.montycloud.com/day2/api"

    # API version
    api_version: str = "v1"

    # Request timeout in seconds
    timeout: int = 30

    # Maximum number of retries for failed requests
    max_retries: int = 3

    # Retry backoff factor
    retry_backoff_factor: float = 1.0

    # Minimum retry delay in seconds
    retry_min_delay: float = 2.0

    # Maximum retry delay in seconds
    retry_max_delay: float = 10.0

    # Status codes to retry on
    retry_status_codes: tuple = (500, 502, 503, 504)

    # Additional headers to include in all requests
    additional_headers: Dict[str, str] = field(default_factory=dict)

    @property
    def api_url(self) -> str:
        """Get the full API URL.

        Returns:
            Full API URL including version.
        """
        return f"{self.base_url}/{self.api_version}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary.

        Returns:
            Dictionary representation of configuration.
        """
        return {
            "base_url": self.base_url,
            "api_version": self.api_version,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "retry_backoff_factor": self.retry_backoff_factor,
            "retry_min_delay": self.retry_min_delay,
            "retry_max_delay": self.retry_max_delay,
            "retry_status_codes": self.retry_status_codes,
            "additional_headers": self.additional_headers,
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "Config":
        """Create configuration from dictionary.

        Args:
            config_dict: Dictionary containing configuration values.

        Returns:
            Config object initialized with values from dictionary.
        """
        return cls(**config_dict)
