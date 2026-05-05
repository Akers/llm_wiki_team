"""共享测试工具函数和类。

被 conftest.py 和各测试文件直接 import。
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import time
from pathlib import Path
from typing import Generator

import requests

# ---------------------------------------------------------------------------
# Binary / project paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
"""Absolute path to the repository root."""

SERVER_BINARY = PROJECT_ROOT / "llm_wiki_lite" / "src-server" / "target" / "debug" / "llm-wiki-server"
"""Path to the compiled debug server binary."""


# ---------------------------------------------------------------------------
# Port / networking helpers
# ---------------------------------------------------------------------------


def find_free_port() -> int:
    """Find and return an available TCP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def wait_for_server(base_url: str, timeout: float = 10.0, interval: float = 0.2) -> bool:
    """Poll the /api/health endpoint until it responds 200 or *timeout* expires."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            r = requests.get(f"{base_url}/api/health", timeout=2)
            if r.status_code == 200:
                return True
        except requests.ConnectionError:
            pass
        time.sleep(interval)
    return False


# ---------------------------------------------------------------------------
# JSON-RPC helpers
# ---------------------------------------------------------------------------

_json_rpc_id = 0


def next_rpc_id() -> int:
    global _json_rpc_id
    _json_rpc_id += 1
    return _json_rpc_id


def make_jsonrpc_request(method: str, params: dict | None = None, request_id: int | None = None) -> dict:
    """Build a well-formed JSON-RPC 2.0 request dict."""
    if request_id is None:
        request_id = next_rpc_id()
    req: dict = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
    }
    if params is not None:
        req["params"] = params
    return req


def call_mcp(base_url: str, method: str, params: dict | None = None, request_id: int | None = None) -> requests.Response:
    """Send a single JSON-RPC request to POST /mcp and return the response."""
    body = make_jsonrpc_request(method, params, request_id)
    return requests.post(
        f"{base_url}/mcp",
        json=body,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )


def call_mcp_tool(base_url: str, tool_name: str, arguments: dict) -> dict:
    """Call an MCP tool via tools/call and return the parsed result content."""
    resp = call_mcp(
        base_url,
        "tools/call",
        {"name": tool_name, "arguments": arguments},
    )
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    body = resp.json()
    assert "result" in body, f"Missing 'result' in response: {body}"
    result = body["result"]
    content_text = result["content"][0]["text"]
    return {
        "jsonrpc_body": body,
        "is_error": result.get("isError", False),
        "content": content_text,
        "parsed": json.loads(content_text) if content_text.startswith("{") or content_text.startswith("[") else content_text,
    }


# ---------------------------------------------------------------------------
# Project scaffolding
# ---------------------------------------------------------------------------


def create_project_structure(base_dir: Path, project_id: str = "test-project") -> Path:
    """Create the minimum directory tree a project needs to function.

    Returns the project directory path.
    """
    project_dir = base_dir / project_id
    (project_dir / "wiki").mkdir(parents=True, exist_ok=True)
    (project_dir / "sources").mkdir(parents=True, exist_ok=True)
    (project_dir / ".llm-wiki").mkdir(parents=True, exist_ok=True)
    return project_dir


def write_toml_config(
    config_path: Path,
    *,
    port: int = 3000,
    data_dir: str = "./data",
    mcp_enabled: bool = True,
    mcp_project_id: str = "test-project",
    extra: str = "",
) -> None:
    """Write a minimal TOML config file suitable for testing."""
    content = f"""\
host = "127.0.0.1"
port = {port}
data_dir = "{data_dir}"

[llm]
provider = "openai"
api_key = "test-key-for-ci"
model = "gpt-4o"
max_context_size = 128000

[embedding]
enabled = false

[search]

[server]
max_upload_size_mb = 100
ingest_timeout_secs = 900

[mcp]
enabled = {str(mcp_enabled).lower()}
project_id = "{mcp_project_id}"
{extra}
"""
    config_path.write_text(content)


# ---------------------------------------------------------------------------
# Server lifecycle
# ---------------------------------------------------------------------------


class ServerHandle:
    """Holds runtime information about a running server instance."""

    def __init__(self, proc: subprocess.Popen, base_url: str, port: int,
                 data_dir: Path, project_dir: Path, project_id: str,
                 config_path: Path):
        self.proc = proc
        self.base_url = base_url
        self.port = port
        self.data_dir = data_dir
        self.project_dir = project_dir
        self.project_id = project_id
        self.config_path = config_path

    def mcp(self, method: str, params: dict | None = None, request_id: int | None = None) -> requests.Response:
        return call_mcp(self.base_url, method, params, request_id)

    def mcp_tool(self, tool_name: str, arguments: dict) -> dict:
        return call_mcp_tool(self.base_url, tool_name, arguments)

    def health(self) -> requests.Response:
        return requests.get(f"{self.base_url}/api/health", timeout=5)


    def shutdown(self) -> None:
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=3)


def _start_server(
    tmp_path: Path,
    *,
    port: int | None = None,
    mcp_enabled: bool = True,
    mcp_project_id: str = "test-project",
    extra_env: dict[str, str] | None = None,
    extra_cli_args: list[str] | None = None,
) -> ServerHandle:
    """Low-level helper: build config, start process, wait for health, return handle."""
    if port is None:
        port = find_free_port()

    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    project_dir = create_project_structure(data_dir, mcp_project_id)

    config_path = tmp_path / "config.toml"
    write_toml_config(
        config_path,
        port=port,
        data_dir=str(data_dir),
        mcp_enabled=mcp_enabled,
        mcp_project_id=mcp_project_id,
    )

    cmd = [
        str(SERVER_BINARY),
        "--port", str(port),
        "--config", str(config_path),
        "-d", str(data_dir),
    ]
    if extra_cli_args:
        cmd.extend(extra_cli_args)

    env = {**os.environ}
    if extra_env:
        env.update(extra_env)

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )

    base_url = f"http://127.0.0.1:{port}"
    ok = wait_for_server(base_url)
    if not ok:
        proc.terminate()
        out, err = proc.communicate(timeout=5)
        raise RuntimeError(
            f"Server did not start within timeout.\nstdout: {out.decode(errors='replace')}\nstderr: {err.decode(errors='replace')}"
        )

    return ServerHandle(
        proc=proc,
        base_url=base_url,
        port=port,
        data_dir=data_dir,
        project_dir=project_dir,
        project_id=mcp_project_id,
        config_path=config_path,
    )
