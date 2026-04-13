"""
Vault404 Python SDK - Exception Classes

Custom exceptions for the Vault404 client with rich error context.
"""

from typing import Any, Optional


class Vault404Error(Exception):
    """Base exception for all Vault404 errors."""

    def __init__(self, message: str, context: Optional[dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.context = context or {}

    def __str__(self) -> str:
        if self.context:
            return f"{self.message} (context: {self.context})"
        return self.message


class NetworkError(Vault404Error):
    """Raised when a network request fails."""

    def __init__(self, message: str, url: Optional[str] = None, cause: Optional[Exception] = None):
        super().__init__(message, {"url": url})
        self.url = url
        self.cause = cause


class ApiError(Vault404Error):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, status_code: int, context: Optional[dict[str, Any]] = None):
        super().__init__(message, context)
        self.status_code = status_code


class TimeoutError(Vault404Error):
    """Raised when a request times out."""

    def __init__(self, message: str, timeout_ms: int, context: Optional[dict[str, Any]] = None):
        super().__init__(message, context)
        self.timeout_ms = timeout_ms


class ValidationError(Vault404Error):
    """Raised when input validation fails."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Any = None,
        rule: Optional[str] = None,
    ):
        super().__init__(message, {"field": field, "value": value, "rule": rule})
        self.field = field
        self.value = value
        self.rule = rule


class AuthenticationError(Vault404Error):
    """Raised when authentication fails."""

    pass


class RateLimitError(Vault404Error):
    """Raised when rate limited by the API."""

    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message, {"retry_after": retry_after})
        self.retry_after = retry_after


class NotFoundError(Vault404Error):
    """Raised when a requested resource is not found."""

    pass
