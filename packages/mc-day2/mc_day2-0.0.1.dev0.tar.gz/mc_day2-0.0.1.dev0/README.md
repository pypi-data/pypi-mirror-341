# MontyCloud SDK

A Python SDK for interacting with the MontyCloud DAY2 API.

## Features

- Secure authentication with API key and API secret key
- Multi-tenant context management
- Comprehensive error handling with retry logic
- Strongly typed models using Pydantic
- CLI interface for common operations

## Requirements

- Python 3.11 or higher

## Installation

```bash
pip install day2
```

## Quick Start

### Using the SDK

```python
from day2 import Session

# Create a session with API key and API secret key
session = Session(
    api_key="your-api-key",
    api_secret_key="your-api-secret-key"
)

# List tenants
tenant_client = session.tenant
tenants = tenant_client.list_tenants()

for tenant in tenants.tenants:
    print(f"Tenant: {tenant.name} (ID: {tenant.id})")

# Set tenant context
session.set_tenant("tenant-123")

# List assessments in the tenant
assessment_client = session.assessment
assessments = assessment_client.list_assessments(tenant_id="tenant-123", status="PENDING")

for assessment in assessments.assessments:
    print(f"Assessment: {assessment.name} (ID: {assessment.id})")
```

### Using the CLI

Configure authentication:

```bash
day2 auth configure --api-key your-api-key --api-secret-key your-api-secret-key
```

List tenants:

```bash
day2 tenant list
```

Get details of a specific tenant:

```bash
day2 tenant get tenant-123
```

List questions for a specific pillar in an assessment:

```bash
day2 assessment questions tenant-123 assessment-456 operational-excellence
```

Create a new assessment:

```bash
day2 assessment create tenant-123 \
    --name "My Assessment" \
    --description "My assessment description" \
    --review-owner "user@example.com" \
    --scope '{"AccountId": "123456789012"}' \
    --lenses "AWS Well-Architected Framework"
```

## Authentication

The SDK supports authentication with both an API key and an API secret key. You can provide these credentials in several ways:

1. Directly in code:
   ```python
   session = Session(
       api_key="your-api-key",
       auth_token="your-api-secret-key"
   )
   ```

2. Environment variables:
   ```bash
   export DAY2_API_KEY="your-api-key"
   export DAY2_API_SECRET_KEY="your-api-secret-key"
   ```
   ```python
   session = Session()  # Will use the environment variables
   ```

3. Configuration file:
   ```bash
   # Using the CLI to configure
   day2 auth configure --api-key your-api-key --api-secret-key your-api-secret-key
   ```
   ```python
   session = Session()  # Will use the configuration file
   ```

## Multi-Tenant Support

The SDK supports multi-tenant operations through session-based tenant context:

```python
# Create a session
session = Session(
    api_key="your-api-key",
    api_secret_key="your-api-secret-key"
)

# Set tenant context
session.set_tenant("org-123")

# Operations will now be performed in the context of the tenant
assessment_client = session.assessment
assessments = assessment_client.list_assessments(tenant_id="tenant-123", status="PENDING")

# Switch to a different tenant
session.set_tenant("tenant-456")

# Operations will now be performed in the context of the new tenant
assessments = assessment_client.list_assessments(tenant_id="tenant-456", status="PENDING")

# Clear tenant context
session.clear_tenant()
```

## Running Examples

The SDK comes with example scripts in the `examples` directory that demonstrate various features. To run these examples:

1. Clone the repository:
   ```bash
   git clone https://github.com/montycloud/day2-sdk.git
   cd day2-sdk
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

4. Run an example:
   ```bash
   python examples/basic_usage.py
   ```

Note: Some examples may require you to have valid API credentials. Make sure to set up your authentication as described in the [Authentication](#authentication) section before running the examples.

## Error Handling

The SDK provides comprehensive error handling with custom exceptions:

```python
from day2 import Session
from day2.exceptions import (
    ClientError,
    ServerError,
    ValidationError,
    ResourceNotFoundError,
    AuthenticationError,
    TenantContextError,
)

try:
    session = Session(
        api_key="your-api-key",
        api_secret_key="your-api-secret-key"
    )
    tenant_client = session.tenant
    tenant_client.get_tenant("tenant-nonexistent")
except ResourceNotFoundError as e:
    print(f"Resource not found: {e}")
except ClientError as e:
    print(f"Client error: {e}")
except ServerError as e:
    print(f"Server error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Development

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/montycloud/day2-sdk.git
   cd day2-sdk
   ```

2. Install development dependencies:
   ```bash
   # Create virtual environment
   make venv

   # Install development dependencies
   make install-dev
   ```

### Testing

Run tests using pytest:

```bash
make test
```

### Run tests with coverage:

```bash
make coverage
```

### Type Checking

Run type checking using mypy:

```bash
make mypy
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
