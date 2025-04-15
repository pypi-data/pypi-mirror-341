"""Credential management for the MontyCloud SDK."""

import json
import os
from pathlib import Path
from typing import Optional


class Credentials:
    """Manages API keys and other authentication credentials."""

    def __init__(
        self, api_key: Optional[str] = None, api_secret_key: Optional[str] = None
    ):
        """Initialize credentials.

        Args:
            api_key: API key for authentication. If not provided, will attempt to load
                from environment variables or configuration file.
            api_secret_key: API secret key (JWT) for authentication. If not provided, will attempt to load
                from environment variables or configuration file.
        """
        self.api_key = api_key or self._load_from_env() or self._load_from_config()
        self.auth_token = (
            api_secret_key
            or self._load_token_from_env()
            or self._load_token_from_config()
        )

        if not self.api_key:
            raise ValueError(
                "No API key provided. Please provide an API key via the constructor, "
                "environment variable DAY2_API_KEY, or configuration file."
            )

    def _load_from_env(self) -> Optional[str]:
        """Load API key from environment variables.

        Returns:
            API key if found in environment variables, None otherwise.
        """
        # Check both new and old env var names for backward compatibility
        return os.environ.get("DAY2_API_KEY") or os.environ.get("MONTYCLOUD_API_KEY")

    def _load_token_from_env(self) -> Optional[str]:
        """Load API secret key from environment variables.

        Returns:
            API secret key if found in environment variables, None otherwise.
        """
        # Check both new and old env var names for backward compatibility
        return os.environ.get("DAY2_API_SECRET_KEY") or os.environ.get(
            "MONTYCLOUD_API_SECRET_KEY"
        )

    def _load_from_config(self) -> Optional[str]:
        """Load API key from configuration file.

        Returns:
            API key if found in configuration file, None otherwise.
        """
        config_dir = Path.home() / ".day2"
        config_file = config_dir / "credentials"

        if not config_file.exists():
            return None

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                api_key: Optional[str] = config.get("api_key")
                return api_key
        except (json.JSONDecodeError, IOError):
            return None

    def _load_token_from_config(self) -> Optional[str]:
        """Load API secret key from configuration file.

        Returns:
            API secret key if found in configuration file, None otherwise.
        """
        config_dir = Path.home() / ".day2"
        config_file = config_dir / "credentials"

        if not config_file.exists():
            return None

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Try both new and old key names for backward compatibility
                api_secret_key: Optional[str] = config.get("api_secret_key")
                auth_token: Optional[str] = config.get("auth_token")
                return api_secret_key or auth_token
        except (json.JSONDecodeError, IOError):
            return None

    def save_to_config(self) -> None:
        """Save credentials to configuration file."""
        if not self.api_key:
            return

        config_dir = Path.home() / ".day2"
        config_dir.mkdir(exist_ok=True)

        config_file = config_dir / "credentials"

        # Load existing config if it exists
        config = {}
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        # Update config with API key
        config["api_key"] = self.api_key

        # Update config with API secret key if available
        if self.auth_token:
            config["api_secret_key"] = self.auth_token

        # Save config
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f)
