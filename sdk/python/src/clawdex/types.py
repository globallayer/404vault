"""
Clawdex Python SDK - Type Definitions

Complete type definitions for the Clawdex collective AI coding agent brain.
Uses dataclasses for clean, typed data structures.
"""

from dataclasses import dataclass, field
from typing import Any, Literal, Optional


# =============================================================================
# Configuration Types
# =============================================================================


@dataclass
class ClawdexClientOptions:
    """Configuration options for the ClawdexClient."""

    api_url: str = "https://api.clawdex.dev"
    """Base URL of the Clawdex API server."""

    api_key: Optional[str] = None
    """API key for authenticated requests (optional, for future use)."""

    timeout: float = 30.0
    """Request timeout in seconds."""

    headers: dict[str, str] = field(default_factory=dict)
    """Custom headers to include in all requests."""

    debug: bool = False
    """Enable debug logging."""


# =============================================================================
# Context Types
# =============================================================================


@dataclass
class Context:
    """Context information for matching solutions and filtering queries."""

    project: Optional[str] = None
    """Project name or identifier."""

    language: Optional[str] = None
    """Programming language (e.g., 'typescript', 'python', 'go')."""

    framework: Optional[str] = None
    """Framework being used (e.g., 'nextjs', 'fastapi', 'django')."""

    database: Optional[str] = None
    """Database being used (e.g., 'postgresql', 'mongodb', 'supabase')."""

    platform: Optional[str] = None
    """Deployment platform (e.g., 'railway', 'vercel', 'aws')."""

    category: Optional[str] = None
    """Issue category (e.g., 'database', 'auth', 'api', 'deployment')."""

    versions: dict[str, str] = field(default_factory=dict)
    """Version information for dependencies."""


# =============================================================================
# Solution Types
# =============================================================================


@dataclass
class Solution:
    """A solution found in the Clawdex knowledge base."""

    id: str
    """Unique identifier for this solution record."""

    solution: str
    """Description of how to fix the error."""

    original_error: str
    """The original error message this solution addresses."""

    context: Context
    """Context in which this solution was applied."""

    confidence: float
    """Confidence score (0.0 to 1.0) based on context match."""

    verified: bool
    """Whether this solution has been verified to work."""

    source: Literal["local", "community"]
    """Source of the solution."""


@dataclass
class FindSolutionResult:
    """Result of searching for solutions."""

    found: bool
    """Whether any solutions were found."""

    message: str
    """Human-readable message about the search results."""

    solutions: list[Solution]
    """List of matching solutions, ordered by relevance."""

    suggestion: Optional[str] = None
    """Suggestion for what to do if no solutions found."""


@dataclass
class LogResult:
    """Generic result of logging an operation."""

    success: bool
    """Whether the operation was successful."""

    message: str
    """Human-readable message about the operation."""

    record_id: Optional[str] = None
    """ID of the created record (if successful)."""

    secrets_redacted: Optional[bool] = None
    """Whether any secrets were redacted from the input."""


# =============================================================================
# Decision Types
# =============================================================================


@dataclass
class Decision:
    """A decision found in the Clawdex knowledge base."""

    id: str
    """Unique identifier for this decision record."""

    title: str
    """Short title for the decision."""

    choice: str
    """What was chosen."""

    alternatives: list[str]
    """Other options that were considered."""

    relevance: float
    """Relevance score (0.0 to 1.0)."""


@dataclass
class FindDecisionResult:
    """Result of searching for decisions."""

    found: bool
    """Whether any decisions were found."""

    message: str
    """Human-readable message about the search results."""

    decisions: list[Decision]
    """List of matching decisions, ordered by relevance."""

    suggestion: Optional[str] = None
    """Suggestion for what to do if no decisions found."""


# =============================================================================
# Pattern Types
# =============================================================================


@dataclass
class Pattern:
    """A pattern found in the Clawdex knowledge base."""

    id: str
    """Unique identifier for this pattern record."""

    name: str
    """Name of the pattern."""

    category: str
    """Category of the pattern."""

    problem: str
    """The problem this pattern solves."""

    solution: str
    """How the pattern solves the problem."""

    relevance: float
    """Relevance score (0.0 to 1.0)."""


@dataclass
class FindPatternResult:
    """Result of searching for patterns."""

    found: bool
    """Whether any patterns were found."""

    message: str
    """Human-readable message about the search results."""

    patterns: list[Pattern]
    """List of matching patterns, ordered by relevance."""

    suggestion: Optional[str] = None
    """Suggestion for what to do if no patterns found."""


# =============================================================================
# Verification Types
# =============================================================================


@dataclass
class VerifySolutionResult:
    """Result of verifying a solution."""

    success: bool
    """Whether the verification was successful."""

    message: str
    """Human-readable message about the verification."""

    record_id: str
    """The record ID that was verified."""

    verified_as: Literal["successful", "unsuccessful"]
    """How the solution was verified."""

    contributed: bool = False
    """Whether the solution was contributed to the community brain."""

    contribution_note: Optional[str] = None
    """Additional note about the contribution."""


# =============================================================================
# Stats Types
# =============================================================================


@dataclass
class ClawdexStats:
    """Statistics about the Clawdex knowledge base."""

    total_records: int
    """Total number of records in the knowledge base."""

    error_fixes: int
    """Number of error fix records."""

    decisions: int
    """Number of decision records."""

    patterns: int
    """Number of pattern records."""

    data_directory: Optional[str] = None
    """Path to the data directory (local storage only)."""


@dataclass
class StatsResult:
    """Result of getting stats."""

    success: bool
    """Whether the operation was successful."""

    message: str
    """Human-readable message."""

    stats: ClawdexStats
    """The statistics."""
