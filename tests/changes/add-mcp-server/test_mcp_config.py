"""MCP 配置相关测试。

覆盖 mcp-config spec 中的所有场景：
- MCP enabled with valid project_id → MCP 路由可用
- MCP disabled → MCP 路由返回 404
- MCP enabled without project_id → MCP 路由不注册
- MCP_PROJECT_ID 环境变量覆盖
- MCP_ENABLED 环境变量覆盖
"""

import os
import subprocess

import pytest
import requests

from _utils import (
    SERVER_BINARY,
    ServerHandle,
    create_project_structure,
    find_free_port,
    wait_for_server,
    write_toml_config,
)


# ---------------------------------------------------------------------------
# Spec Scenario: MCP enabled with valid project → MCP routes work
# ---------------------------------------------------------------------------


class TestMcpEnabledWithProject:
    """Scenario: mcp.enabled=true + mcp.project_id set → MCP routes registered and functional."""

    def test_mcp_routes_registered(self, server: ServerHandle):
        """POST /mcp should return 200 (not 404) when MCP is enabled with a valid project."""
        resp = server.mcp("initialize")
        assert resp.status_code == 200
        body = resp.json()
        assert body["jsonrpc"] == "2.0"
        assert "result" in body

    def test_initialize_returns_server_info(self, server: ServerHandle):
        """initialize 响应应包含 serverInfo.name = 'llm-wiki-lite'."""
        resp = server.mcp("initialize")
        body = resp.json()
        assert body["result"]["serverInfo"]["name"] == "llm-wiki-lite"
        assert "version" in body["result"]["serverInfo"]

    def test_tools_list_available(self, server: ServerHandle):
        """tools/list 应返回 5 个工具定义."""
        resp = server.mcp("tools/list")
        body = resp.json()
        tools = body["result"]["tools"]
        assert len(tools) == 5
        tool_names = {t["name"] for t in tools}
        assert tool_names == {
            "search_wiki",
            "read_wiki_page",
            "write_wiki_page",
            "ingest_text",
            "check_ingest_status",
        }


# ---------------------------------------------------------------------------
# Spec Scenario: MCP disabled → routes return 404
# ---------------------------------------------------------------------------


class TestMcpDisabled:
    """Scenario: mcp.enabled=false → MCP endpoints not registered."""

    def test_mcp_post_returns_404_when_disabled(self, server_mcp_disabled: ServerHandle):
        """POST /mcp returns 404 when MCP is disabled."""
        resp = requests.post(
            f"{server_mcp_disabled.base_url}/mcp",
            json={"jsonrpc": "2.0", "id": 1, "method": "initialize"},
            timeout=5,
        )
        assert resp.status_code == 404

    def test_sse_get_returns_404_when_disabled(self, server_mcp_disabled: ServerHandle):
        """GET /sse returns 404 when MCP is disabled."""
        resp = requests.get(
            f"{server_mcp_disabled.base_url}/sse",
            timeout=5,
        )
        assert resp.status_code == 404

    def test_rest_api_still_works_when_mcp_disabled(self, server_mcp_disabled: ServerHandle):
        """REST API (e.g., /api/health) should still function when MCP is disabled."""
        resp = server_mcp_disabled.health()
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Spec Scenario: MCP enabled without project_id → routes not registered
# ---------------------------------------------------------------------------


class TestMcpEnabledWithoutProject:
    """Scenario: mcp.enabled=true but mcp.project_id is empty → MCP not initialized."""

    def test_mcp_post_returns_404_without_project_id(self, server_no_project: ServerHandle):
        """POST /mcp returns 404 when project_id is not configured."""
        resp = requests.post(
            f"{server_no_project.base_url}/mcp",
            json={"jsonrpc": "2.0", "id": 1, "method": "initialize"},
            timeout=5,
        )
        assert resp.status_code == 404

    def test_rest_api_works_without_mcp_project(self, server_no_project: ServerHandle):
        """REST API still works even when MCP is not initialized."""
        resp = server_no_project.health()
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Spec Scenario: MCP_PROJECT_ID env var override
# ---------------------------------------------------------------------------


class TestMcpProjectIdEnvOverride:
    """Scenario: MCP_PROJECT_ID env var overrides TOML config."""

    def test_env_override_sets_project_id(self, tmp_path):
        """When MCP_PROJECT_ID env var is set, the project_id from config is overridden."""
        port = find_free_port()
        data_dir = tmp_path / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        # Create project with env-overridden ID
        env_project_id = "env-project"
        create_project_structure(data_dir, env_project_id)

        # Write config with empty project_id
        config_path = tmp_path / "config.toml"
        write_toml_config(config_path, port=port, data_dir=str(data_dir),
                          mcp_enabled=True, mcp_project_id="")

        proc = subprocess.Popen(
            [str(SERVER_BINARY), "--port", str(port), "--config", str(config_path), "-d", str(data_dir)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "MCP_PROJECT_ID": env_project_id},
        )

        base_url = f"http://127.0.0.1:{port}"
        try:
            ok = wait_for_server(base_url)
            assert ok, "Server failed to start"

            # MCP routes should be registered because env var set project_id
            resp = requests.post(
                f"{base_url}/mcp",
                json={"jsonrpc": "2.0", "id": 1, "method": "initialize"},
                timeout=5,
            )
            assert resp.status_code == 200
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)


# ---------------------------------------------------------------------------
# Spec Scenario: MCP_ENABLED env var override
# ---------------------------------------------------------------------------


class TestMcpEnabledEnvOverride:
    """Scenario: MCP_ENABLED env var can disable MCP."""

    def test_mcp_enabled_false_disables_routes(self, tmp_path):
        """When MCP_ENABLED=false, MCP routes should not be registered even if TOML says enabled."""
        port = find_free_port()
        data_dir = tmp_path / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        create_project_structure(data_dir, "test-project")

        config_path = tmp_path / "config.toml"
        write_toml_config(config_path, port=port, data_dir=str(data_dir),
                          mcp_enabled=True, mcp_project_id="test-project")

        proc = subprocess.Popen(
            [str(SERVER_BINARY), "--port", str(port), "--config", str(config_path), "-d", str(data_dir)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "MCP_ENABLED": "false"},
        )

        base_url = f"http://127.0.0.1:{port}"
        try:
            ok = wait_for_server(base_url)
            assert ok, "Server failed to start"

            resp = requests.post(
                f"{base_url}/mcp",
                json={"jsonrpc": "2.0", "id": 1, "method": "initialize"},
                timeout=5,
            )
            assert resp.status_code == 404  # MCP disabled via env
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
