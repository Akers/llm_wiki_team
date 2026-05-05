"""MCP-specific fixtures for the add-mcp-server change tests."""

import pytest


@pytest.fixture
def wiki_page_content() -> str:
    """Return sample Markdown content for wiki pages."""
    return """\
# Test Page

This is a test wiki page about **machine learning**.

## Key Concepts

- Supervised learning
- Unsupervised learning
- Reinforcement learning

Machine learning is a subset of artificial intelligence that enables
systems to learn and improve from experience without being explicitly programmed.
"""
