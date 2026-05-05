"""Root-level shared test fixtures.

Imports utilities from _utils.py and exposes pytest fixtures.
"""

from pathlib import Path
from typing import Generator

import pytest

from _utils import ServerHandle, _start_server


@pytest.fixture
def server(tmp_path: Path) -> Generator[ServerHandle, None, None]:
    """Start a server with MCP enabled and a default project.

    The server is automatically stopped after the test.
    """
    srv = _start_server(tmp_path)
    yield srv
    srv.shutdown()


@pytest.fixture
def server_no_project(tmp_path: Path) -> Generator[ServerHandle, None, None]:
    """Start a server with MCP enabled but *no* project_id configured.

    In this state MCP routes should NOT be registered.
    """
    srv = _start_server(tmp_path, mcp_enabled=True, mcp_project_id="")
    yield srv
    srv.shutdown()


@pytest.fixture
def server_mcp_disabled(tmp_path: Path) -> Generator[ServerHandle, None, None]:
    """Start a server with MCP explicitly disabled."""
    srv = _start_server(tmp_path, mcp_enabled=False)
    yield srv
    srv.shutdown()
