"""
Vault404 REST API

FastAPI-based REST API server for the Vault404 collective AI coding agent brain.
Provides HTTP endpoints for searching and logging solutions, decisions, and patterns.
"""

from .server import app, create_app

__all__ = ["app", "create_app"]
