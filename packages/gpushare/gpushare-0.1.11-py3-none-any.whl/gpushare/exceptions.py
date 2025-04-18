# gpushare/exceptions.py

class GPUShareError(Exception):
    """Base exception for gpushare."""
    pass

class AuthenticationError(GPUShareError):
    """Raised when login, OTP, or token is invalid."""
    pass

class AuthorizationError(GPUShareError):
    """Raised when user lacks permission for an operation."""
    pass

class APIError(GPUShareError):
    """Raised on non‑200 API responses or parse failures."""
    pass

class TokenError(GPUShareError):
    """Raised on token lifecycle operations (info, refresh, revoke)."""
    pass

class TokenRevokedError(TokenError):
    """Raised when attempting to use a revoked token."""
    pass

class TokenExpiredError(TokenError):
    """Raised when the token has expired."""
    pass
