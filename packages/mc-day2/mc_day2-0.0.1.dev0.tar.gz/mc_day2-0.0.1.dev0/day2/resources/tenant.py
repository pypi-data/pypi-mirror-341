"""Tenant resource implementation for the MontyCloud DAY2 SDK."""

from day2.client.base import BaseClient
from day2.models.tenant import GetTenantOutput, ListTenantsOutput
from day2.session import Session


class TenantClient(BaseClient):
    """Client for interacting with the Tenant service."""

    def __init__(self, session: Session) -> None:
        """Initialize a new TenantClient.

        Args:
            session: MontyCloud session.
        """
        super().__init__(session, "tenant")

    def list_tenants(
        self, page_number: int = 1, page_size: int = 10
    ) -> ListTenantsOutput:
        """List tenants that the user has access to.

        Args:
            page_number: Page number of the tenant details to be fetched.
            page_size: Number of tenants to be fetched in a page.

        Returns:
            ListTenantsOutput: Object containing list of tenants and pagination info.

        Raises:
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key")
            >>> client = session.tenant
            >>> response = client.list_tenants(page_number=1, page_size=10)
            >>> for tenant in response.tenants:
            ...     print(f"{tenant.id}: {tenant.name}")
        """
        params = {
            "PageNumber": page_number,
            "PageSize": page_size,
        }

        response = self._make_request("GET", "tenants", params=params)
        return ListTenantsOutput.model_validate(response)

    def get_tenant(self, tenant_id: str) -> GetTenantOutput:
        """Get details of a specific tenant.

        Args:
            tenant_id: ID of the tenant to get details for.

        Returns:
            GetTenantOutput: Object containing tenant details.

        Raises:
            ResourceNotFoundError: If the tenant does not exist.
            ClientError: If the request is invalid.
            ServerError: If an internal server error occurs.
            AuthenticationError: If authentication fails.

        Examples:
            >>> session = Session(api_key="your-api-key")
            >>> client = session.tenant
            >>> response = client.get_tenant("tenant-123")
            >>> print(f"Tenant name: {response.name}")
        """
        # The endpoint for getting tenant details is directly using the tenant ID in the path
        response = self._make_request("GET", f"tenants/{tenant_id}")
        return GetTenantOutput.model_validate(response)
