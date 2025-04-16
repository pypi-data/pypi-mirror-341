from typing import Dict, Any, Optional


class HerawError(Exception):
    """Exception raised for heraw API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class AuthenticationError(HerawError):
    """Raised when there are issues with authentication."""

    pass


class ValidationError(HerawError):
    """Raised when the API returns validation errors."""

    pass


class RateLimitError(HerawError):
    """Raised when the API rate limit is exceeded."""

    pass


class ServerError(HerawError):
    """Raised when the API returns a server error."""

    pass
