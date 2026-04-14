"""
Multi-signal ranking engine for vault404 search.

Combines temporal decay, text similarity, context matching,
verification status, success rate, and usage popularity.
"""

import math
from datetime import datetime
from typing import Optional


# Default weights for combining signals
DEFAULT_WEIGHTS = {
    "text_similarity": 0.35,
    "context_match": 0.20,
    "temporal": 0.20,
    "verification": 0.10,
    "success_rate": 0.10,
    "popularity": 0.05,
}


def temporal_decay(
    timestamp: datetime,
    half_life_days: int = 30,
    now: Optional[datetime] = None,
) -> float:
    """
    Calculate temporal decay factor using exponential decay.

    Args:
        timestamp: When the record was created
        half_life_days: After this many days, score is halved (default: 30)
        now: Current time (for testing), defaults to datetime.now()

    Returns:
        float: 0.0 to 1.0 (1.0 = now, approaches 0 as age increases)

    Examples:
        - Record from today: ~1.0
        - Record from 30 days ago: ~0.5
        - Record from 60 days ago: ~0.25
        - Record from 90 days ago: ~0.125
    """
    if now is None:
        now = datetime.now()

    # Handle timezone-aware vs naive datetimes
    if timestamp.tzinfo is not None and now.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=None)
    elif timestamp.tzinfo is None and now.tzinfo is not None:
        now = now.replace(tzinfo=None)

    age_days = (now - timestamp).total_seconds() / 86400  # days

    if age_days < 0:
        return 1.0  # Future timestamps treated as now

    return 0.5 ** (age_days / half_life_days)


def success_rate_factor(success_count: int, failure_count: int) -> float:
    """
    Calculate success rate factor with Bayesian smoothing.

    Uses a Beta prior to handle low sample sizes:
    - Prior: 50% success rate (neutral)
    - Weight: 2 pseudo-observations

    Args:
        success_count: Number of times this fix worked
        failure_count: Number of times this fix failed

    Returns:
        float: 0.0 to 1.0 (smoothed success rate)

    Examples:
        - No data (0, 0): ~0.5 (neutral)
        - One success (1, 0): ~0.67
        - One failure (0, 1): ~0.33
        - Ten successes (10, 0): ~0.92
    """
    alpha = 1  # pseudo-successes (prior)
    beta = 1  # pseudo-failures (prior)

    smoothed_rate = (success_count + alpha) / (success_count + failure_count + alpha + beta)
    return smoothed_rate


def usage_popularity_factor(usage_count: int, max_usage: int = 100) -> float:
    """
    Calculate popularity factor from usage count.

    Uses logarithmic scaling to prevent runaway popularity
    (frequently-used solutions don't dominate completely).

    Args:
        usage_count: How many times this fix was returned in searches
        max_usage: Reference point for "very popular" (default: 100)

    Returns:
        float: 0.5 to 1.0 (0.5 = unused, 1.0 = highly popular)

    Examples:
        - 0 uses: 0.5 (neutral)
        - 1 use: ~0.65
        - 10 uses: ~0.75
        - 100 uses: ~1.0
    """
    if usage_count <= 0:
        return 0.5  # Neutral for unused

    # Log scale: log10(1) = 0, log10(10) = 1, log10(100) = 2
    # Normalize so 100 uses = 1.0
    normalized = min(math.log10(usage_count + 1) / math.log10(max_usage + 1), 1.0)
    return 0.5 + normalized * 0.5


def calculate_score(
    text_similarity: float,
    context_match: float = 0.0,
    temporal_factor: float = 1.0,
    verified: bool = False,
    success_count: int = 0,
    failure_count: int = 0,
    usage_count: int = 0,
    weights: Optional[dict[str, float]] = None,
) -> float:
    """
    Combine all ranking signals into a final score.

    Args:
        text_similarity: How well the error message matches (0-1)
        context_match: How well the context matches (0-1)
        temporal_factor: Freshness score from temporal_decay (0-1)
        verified: Whether the solution was verified
        success_count: Number of times the solution worked
        failure_count: Number of times the solution failed
        usage_count: How many times this was returned in searches
        weights: Optional custom weights (defaults to DEFAULT_WEIGHTS)

    Returns:
        float: Combined score (0-1)
    """
    w = weights or DEFAULT_WEIGHTS

    # Convert verified bool to factor (1.0 = verified, 0.5 = unverified)
    verification_factor = 1.0 if verified else 0.5

    # Calculate derived factors
    success_factor = success_rate_factor(success_count, failure_count)
    popularity_factor = usage_popularity_factor(usage_count)

    # Weighted sum
    score = (
        text_similarity * w["text_similarity"]
        + context_match * w["context_match"]
        + temporal_factor * w["temporal"]
        + verification_factor * w["verification"]
        + success_factor * w["success_rate"]
        + popularity_factor * w["popularity"]
    )

    return min(score, 1.0)
