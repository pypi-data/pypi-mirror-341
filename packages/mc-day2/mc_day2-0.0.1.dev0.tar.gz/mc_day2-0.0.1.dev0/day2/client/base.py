"""Base client implementation for the MontyCloud DAY2 SDK."""

import json
import logging

# Use TYPE_CHECKING to avoid circular imports
from typing import TYPE_CHECKING, Any, Dict

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from day2.exceptions import (
    AuthenticationError,
    ClientError,
    ResourceNotFoundError,
    ServerError,
    ValidationError,
)

if TYPE_CHECKING:
    from day2.session import Session

logger = logging.getLogger(__name__)


class BaseClient:
    """Base client for MontyCloud API services."""

    def __init__(self, session: "Session", service_name: str):
        """Initialize a new client.

        Args:
            session: MontyCloud session.
            service_name: Name of the service this client will interact with.
        """
        self.session = session
        self.service_name = service_name
        self._config = session._config

    def _get_endpoint_url(self, endpoint: str) -> str:
        """Get the full URL for an endpoint.

        Args:
            endpoint: API endpoint path.

        Returns:
            Full URL for the endpoint.
        """
        if endpoint.startswith("/"):
            endpoint = endpoint[1:]

        # For MontyCloud API, we don't include the service name in the URL
        return f"{self._config.api_url}/{endpoint}"

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests.

        Returns:
            Headers dictionary including authentication and tenant context.
        """
        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": (
                str(self.session.credentials.api_key)
                if self.session.credentials.api_key
                else ""
            ),
        }

        # Add Authorization header if available
        # Use auth_token (which is actually the api_secret_key internally)
        if (
            hasattr(self.session.credentials, "auth_token")
            and self.session.credentials.auth_token
        ):
            headers["Authorization"] = self.session.credentials.auth_token

        if self.session.tenant_id:
            headers["x-tenant-id"] = str(self.session.tenant_id)

        # Add any additional headers from config
        if self._config.additional_headers:
            # Ensure all header values are strings
            for key, value in self._config.additional_headers.items():
                headers[key] = str(value)

        return headers

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions.

        Args:
            response: Response from API request.

        Returns:
            Response data as dictionary.

        Raises:
            ValidationError: If the request was invalid (400).
            AuthenticationError: If authentication failed (401).
            ResourceNotFoundError: If the requested resource was not found (404).
            ClientError: For other client errors (4xx).
            ServerError: For server errors (5xx).
        """
        request_id = response.headers.get("x-request-id")

        try:
            data: Dict[str, Any] = response.json()
            logger.info("Response data: %s", json.dumps(data, indent=2)[:1000])
        except ValueError:
            data = {"message": response.text}
            logger.info("Response text: %s", response.text[:1000])

        if 400 <= response.status_code < 500:
            message = data.get("message", "Client error")

            if response.status_code == 400:
                raise ValidationError(message, response.status_code, request_id)
            if response.status_code in (401, 403):
                raise AuthenticationError(message, response.status_code, request_id)
            if response.status_code == 404:
                raise ResourceNotFoundError(message, response.status_code, request_id)
            raise ClientError(message, response.status_code, request_id)

        if response.status_code >= 500:
            message = data.get("message", "Server error")
            raise ServerError(message, response.status_code, request_id)

        return dict(data)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(ServerError),
        reraise=True,
    )
    def _request_with_retry(
        self, method: str, url: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Make an API request with retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            url: Full URL for the request.
            **kwargs: Additional arguments to pass to requests.

        Returns:
            Response data as dictionary.

        Raises:
            ClientError: For client errors (4xx).
            ServerError: For server errors (5xx).
        """
        headers = self._get_headers()

        # Update headers with any provided in kwargs
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))

        # Log request details
        logger.debug(
            "Making %s request to %s with headers %s and kwargs %s",
            method,
            url,
            headers,
            kwargs,
        )

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                timeout=self._config.timeout,
                **kwargs,
            )

            # Log response details
            logger.info("Received response with status %s", response.status_code)
            logger.debug("Response headers: %s", response.headers)
            logger.debug("Response content: %s", response.text[:1000])

            return self._handle_response(response)

        except requests.RequestException as e:
            logger.error("Request failed: %s", e)
            raise ServerError(str(e), 0) from e

    def _make_request(
        self, method: str, endpoint: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Make an API request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            endpoint: API endpoint path.
            **kwargs: Additional arguments to pass to requests.

        Returns:
            Response data as dictionary.
        """
        # Handle JSON data
        if "json_data" in kwargs:
            kwargs["json"] = kwargs.pop("json_data")

        url = self._get_endpoint_url(endpoint)
        logger.info("Making request to %s %s", method, url)
        # Pass the full URL to the request method
        return self._request_with_retry(method, url, **kwargs)
