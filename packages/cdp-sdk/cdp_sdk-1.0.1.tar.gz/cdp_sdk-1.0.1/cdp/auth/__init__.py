"""Authentication package for the SDK.

This package provides authentication utilities and JWT token handling functionality.
"""

from .utils.jwt import (
    generate_jwt,
    generate_wallet_jwt,
    JwtOptions,
    WalletJwtOptions,
)
from .utils.http import get_auth_headers, GetAuthHeadersOptions
from .clients.urllib3.client import Urllib3AuthClient, Urllib3AuthClientOptions

__all__ = [
    # JWT utils exports
    "generate_jwt",
    "generate_wallet_jwt",
    "JwtOptions",
    "WalletJwtOptions",
    # Client exports
    "Urllib3AuthClient",
    "Urllib3AuthClientOptions",
    # HTTP utils exports
    "get_auth_headers",
    "GetAuthHeadersOptions",
]

"""CDP SDK Auth package."""

# Empty file to mark directory as Python package
