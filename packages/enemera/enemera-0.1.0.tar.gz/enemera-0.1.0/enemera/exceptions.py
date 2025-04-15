"""
Custom exceptions for the Enemera API client.
"""

class EnemeraError(Exception):
    """Base exception for all Enemera API client errors."""
    pass


class AuthenticationError(EnemeraError):
    """Raised when authentication with the API fails."""
    pass


class RateLimitError(EnemeraError):
    """Raised when the API rate limit is exceeded."""
    pass


class APIError(EnemeraError):
    """Raised when the API returns an error response."""
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"API Error {status_code}: {detail}")


class ValidationError(EnemeraError):
    """Raised when input validation fails."""
    pass


class ConnectionError(EnemeraError):
    """Raised when connection to the API fails."""
    pass