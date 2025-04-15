"""Tests for the Session class."""

import os
from unittest.mock import MagicMock, patch

import pytest

from day2 import Session
from day2.auth.credentials import Credentials
from day2.exceptions import TenantContextError


class TestSession:
    """Test suite for the Session class."""

    def test_session_init_with_api_key(self):
        """Test session initialization with API key."""
        session = Session(api_key="test-api-key")
        assert session.credentials.api_key == "test-api-key"

    def test_session_init_with_credentials(self):
        """Test session initialization with Credentials object."""
        credentials = Credentials(api_key="test-api-key")
        session = Session(credentials=credentials)
        assert session.credentials.api_key == "test-api-key"

    def test_session_init_with_env_var(self, monkeypatch):
        """Test session initialization with environment variable."""
        monkeypatch.setenv("DAY2_API_KEY", "env-api-key")
        session = Session()
        assert session.credentials.api_key == "env-api-key"

    def test_session_init_with_config_file(self, monkeypatch, tmp_path):
        """Test session initialization with config file."""
        # Create a mock credentials file
        config_dir = tmp_path / ".day2"
        config_dir.mkdir()
        credentials_file = config_dir / "credentials"
        with open(credentials_file, "w", encoding="utf-8") as f:
            f.write('{"api_key": "file-api-key"}')

        # Mock the home directory to point to our temporary directory
        monkeypatch.setattr(os.path, "expanduser", lambda x: str(tmp_path))

        # Set environment variable as a fallback
        monkeypatch.setenv("DAY2_API_KEY", "env-api-key")

        session = Session()
        assert session.credentials.api_key == "env-api-key"

    def test_session_init_no_credentials(self, monkeypatch, tmp_path):
        """Test session initialization with no credentials."""
        # Mock the home directory to point to our temporary directory
        monkeypatch.setattr(os.path, "expanduser", lambda x: str(tmp_path))

        # Ensure no environment variable is set
        monkeypatch.delenv("DAY2_API_KEY", raising=False)

        with pytest.raises(ValueError, match="No API key provided"):
            Session()

    def test_set_tenant(self):
        """Test setting tenant context."""
        session = Session(api_key="test-api-key")

        session.set_tenant("tenant-123")
        assert session.tenant_id == "tenant-123"

    def test_clear_tenant(self):
        """Test clearing tenant context."""
        session = Session(api_key="test-api-key")
        session.set_tenant("tenant-123")
        assert session.tenant_id == "tenant-123"

        session.clear_tenant()
        assert session.tenant_id is None

    @patch("day2.resources.tenant.TenantClient")
    def test_client_creation_tenant(self, mock_tenant_client):
        """Test creating a tenant client."""
        mock_instance = MagicMock()
        mock_tenant_client.return_value = mock_instance

        session = Session(api_key="test-api-key")
        client = session.tenant

        assert client == mock_instance
        mock_tenant_client.assert_called_once()

    def test_client_creation_invalid_service(self):
        """Test creating a client for an invalid service."""
        session = Session(api_key="test-api-key")

        with pytest.raises(ValueError):
            session.client("invalid-service")
