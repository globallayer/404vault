"""Tests for the Clawdex Python SDK client."""

import pytest
from unittest.mock import patch, MagicMock
import json

import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from clawdex import (
    Clawdex,
    ClawdexClient,
    ValidationError,
    NetworkError,
    Context,
    Solution,
    Decision,
    Pattern,
)


class TestClawdexClient:
    """Test the Clawdex client initialization and configuration."""

    def test_default_initialization(self):
        """Test client initializes with default values."""
        client = Clawdex()
        assert client.api_url == "https://api.clawdex.dev"

    def test_custom_api_url(self):
        """Test client accepts custom API URL."""
        client = Clawdex(api_url="http://localhost:8000")
        assert client.api_url == "http://localhost:8000"

    def test_url_normalization(self):
        """Test trailing slashes are removed from API URL."""
        client = Clawdex(api_url="http://localhost:8000/")
        assert client.api_url == "http://localhost:8000"

    def test_clawdex_client_alias(self):
        """Test ClawdexClient is an alias for Clawdex."""
        assert ClawdexClient is Clawdex


class TestValidation:
    """Test input validation."""

    def test_find_solution_requires_error_message(self):
        """Test find_solution validates error_message is required."""
        client = Clawdex()
        with pytest.raises(ValidationError) as exc_info:
            client.find_solution(error_message=None)
        assert exc_info.value.field == "error_message"

    def test_find_solution_rejects_empty_error_message(self):
        """Test find_solution rejects empty error_message."""
        client = Clawdex()
        with pytest.raises(ValidationError) as exc_info:
            client.find_solution(error_message="   ")
        assert exc_info.value.field == "error_message"

    def test_log_error_fix_requires_both_fields(self):
        """Test log_error_fix validates both required fields."""
        client = Clawdex()

        with pytest.raises(ValidationError) as exc_info:
            client.log_error_fix(error_message=None, solution="fix")
        assert exc_info.value.field == "error_message"

        with pytest.raises(ValidationError) as exc_info:
            client.log_error_fix(error_message="error", solution=None)
        assert exc_info.value.field == "solution"

    def test_log_decision_requires_title_and_choice(self):
        """Test log_decision validates required fields."""
        client = Clawdex()

        with pytest.raises(ValidationError):
            client.log_decision(title=None, choice="option")

        with pytest.raises(ValidationError):
            client.log_decision(title="Decision", choice=None)

    def test_log_pattern_requires_all_fields(self):
        """Test log_pattern validates all required fields."""
        client = Clawdex()

        with pytest.raises(ValidationError):
            client.log_pattern(name=None, category="cat", problem="prob", solution="sol")

        with pytest.raises(ValidationError):
            client.log_pattern(name="name", category=None, problem="prob", solution="sol")

        with pytest.raises(ValidationError):
            client.log_pattern(name="name", category="cat", problem=None, solution="sol")

        with pytest.raises(ValidationError):
            client.log_pattern(name="name", category="cat", problem="prob", solution=None)


class TestTypes:
    """Test type definitions."""

    def test_context_creation(self):
        """Test Context dataclass creation."""
        ctx = Context(
            project="my-app",
            language="python",
            framework="fastapi",
        )
        assert ctx.project == "my-app"
        assert ctx.language == "python"
        assert ctx.framework == "fastapi"
        assert ctx.database is None

    def test_solution_creation(self):
        """Test Solution dataclass creation."""
        solution = Solution(
            id="ef_123",
            solution="Run npm install",
            original_error="Module not found",
            context=Context(language="typescript"),
            confidence=0.95,
            verified=True,
            source="local",
        )
        assert solution.id == "ef_123"
        assert solution.confidence == 0.95
        assert solution.verified is True

    def test_decision_creation(self):
        """Test Decision dataclass creation."""
        decision = Decision(
            id="dec_123",
            title="Database choice",
            choice="PostgreSQL",
            alternatives=["MySQL", "MongoDB"],
            relevance=0.85,
        )
        assert decision.choice == "PostgreSQL"
        assert len(decision.alternatives) == 2

    def test_pattern_creation(self):
        """Test Pattern dataclass creation."""
        pattern = Pattern(
            id="pat_123",
            name="Optimistic UI",
            category="frontend",
            problem="Slow UI feedback",
            solution="Update immediately",
            relevance=0.9,
        )
        assert pattern.name == "Optimistic UI"
        assert pattern.category == "frontend"


class TestHealthCheck:
    """Test health check functionality."""

    def test_health_check_returns_bool(self):
        """Test health_check returns a boolean."""
        client = Clawdex(api_url="http://invalid-url-that-does-not-exist.local")
        # Should return False for unreachable server (not raise)
        result = client.health_check()
        assert isinstance(result, bool)
        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
