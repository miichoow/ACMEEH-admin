"""ACMEEH Admin API client library."""

from acmeeh_admin.client import AcmeehAdminClient
from acmeeh_admin.exceptions import (
    AcmeehAdminError,
    AcmeehAuthenticationError,
    AcmeehConnectionError,
)

__version__ = "1.0.0"
__all__ = [
    "AcmeehAdminClient",
    "AcmeehAdminError",
    "AcmeehAuthenticationError",
    "AcmeehConnectionError",
    "__version__",
]
