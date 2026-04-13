"""
Clawdex Python SDK

The official Python SDK for interacting with Clawdex - the collective AI coding agent brain.
Every verified fix makes ALL AI agents smarter.

Example:
    >>> from clawdex import Clawdex
    >>>
    >>> client = Clawdex()
    >>>
    >>> # Find solutions for an error
    >>> result = client.find_solution(
    ...     error_message="Cannot find module react",
    ...     language="typescript"
    ... )
    >>>
    >>> # Log an error fix
    >>> client.log_error_fix(
    ...     error_message="Module not found",
    ...     solution="Run npm install",
    ...     verified=True
    ... )

With Custom Configuration:
    >>> from clawdex import Clawdex
    >>>
    >>> client = Clawdex(
    ...     api_url="http://localhost:8000",
    ...     timeout=60,
    ...     debug=True
    ... )

Error Handling:
    >>> from clawdex import Clawdex, ValidationError, NetworkError
    >>>
    >>> client = Clawdex()
    >>>
    >>> try:
    ...     client.find_solution(error_message="")
    ... except ValidationError as e:
    ...     print(f"Invalid input: {e.field}")
    ... except NetworkError as e:
    ...     print(f"Network issue: {e.message}")
"""

__version__ = "0.1.0"

# Main client
from .client import Clawdex, ClawdexClient

# Error classes
from .errors import (
    ClawdexError,
    NetworkError,
    ApiError,
    TimeoutError,
    ValidationError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
)

# Types
from .types import (
    # Context
    Context,
    # Solution types
    Solution,
    FindSolutionResult,
    LogResult,
    # Decision types
    Decision,
    FindDecisionResult,
    # Pattern types
    Pattern,
    FindPatternResult,
    # Verification types
    VerifySolutionResult,
    # Stats types
    ClawdexStats,
    StatsResult,
)

__all__ = [
    # Version
    "__version__",
    # Main client
    "Clawdex",
    "ClawdexClient",
    # Errors
    "ClawdexError",
    "NetworkError",
    "ApiError",
    "TimeoutError",
    "ValidationError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    # Types
    "Context",
    "Solution",
    "FindSolutionResult",
    "LogResult",
    "Decision",
    "FindDecisionResult",
    "Pattern",
    "FindPatternResult",
    "VerifySolutionResult",
    "ClawdexStats",
    "StatsResult",
]
