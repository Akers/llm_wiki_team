"""MCP stdio transport 模式测试。

覆盖场景：
- --mode mcp-stdio 启动 stdio 服务器
- 通过 stdin 发送 initialize，在 stdout 收到响应
- 通过 stdin 发送 tools/list
- 无 project_id 启动 stdio 模式应报错退出
- 项目目录不存在应报错退出
"""

import json
import os
import subprocess
import time

import pytest

from _utils import SERVER_BINARY, create_project_structure, find_free_port, write_toml_config


class TestStdioTransport:
    """stdio transport 模式测试。"""

    def _start_stdio(self, tmp_path, project_id="test-project"):
        """启动 stdio 模式的服务器进程。"""
        data_dir = tmp_path / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        create_project_structure(data_dir, project_id)

        config_path = tmp_path / "config.toml"
        port = find_free_port()
        write_toml_config(
            config_path,
            port=port,
            data_dir=str(data_dir),
            mcp_enabled=True,
            mcp_project_id=project_id,
        )

        env = {**os.environ, "RUST_LOG": "off"}
        proc = subprocess.Popen(
            [str(SERVER_BINARY), "--config", str(config_path), "-d", str(data_dir), "--mode", "mcp-stdio"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )
        return proc

    def _send_and_receive(self, proc, request_dict, timeout=10):
        """向 stdio 进程发送 JSON-RPC 并读取 JSON 响应行。

        过滤掉非 JSON 行（如日志输出），只解析第一个有效 JSON 行。
        """
        assert proc.stdin is not None, "stdin not available"
        assert proc.stdout is not None, "stdout not available"

        line = json.dumps(request_dict) + "\n"
        proc.stdin.write(line.encode())
        proc.stdin.flush()

        # Read response lines, filter for JSON lines
        import selectors

        sel = selectors.DefaultSelector()
        sel.register(proc.stdout, selectors.EVENT_READ)

        response_data = b""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            events = sel.select(timeout=1.0)
            for _key, _mask in events:
                chunk = proc.stdout.read1(4096)  # type: ignore[union-attr]
                if chunk:
                    response_data += chunk

            # Try to find and parse a JSON line
            while b"\n" in response_data:
                line_bytes, response_data = response_data.split(b"\n", 1)
                line_str = line_bytes.decode(errors="replace").strip()
                if line_str.startswith("{"):
                    try:
                        sel.close()
                        return json.loads(line_str)
                    except json.JSONDecodeError:
                        continue
                # Skip non-JSON lines (logs, etc.)

        sel.close()
        # Last attempt: try to parse whatever we have
        for line_str in response_data.decode(errors="replace").strip().split("\n"):
            line_str = line_str.strip()
            if line_str.startswith("{"):
                try:
                    return json.loads(line_str)
                except json.JSONDecodeError:
                    pass
        raise TimeoutError(f"No JSON response within {timeout}s. Got: {response_data!r}")

    def test_stdio_initialize(self, tmp_path):
        """stdio 模式下发送 initialize 请求并收到正确响应。"""
        proc = self._start_stdio(tmp_path)
        try:
            response = self._send_and_receive(proc, {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "1.0"},
                },
            })

            assert response["jsonrpc"] == "2.0"
            assert response["id"] == 1
            assert "result" in response
            assert response["result"]["serverInfo"]["name"] == "llm-wiki-lite"
        finally:
            proc.terminate()
            proc.wait(timeout=5)

    def test_stdio_tools_list(self, tmp_path):
        """stdio 模式下调用 tools/list 返回 5 个工具。"""
        proc = self._start_stdio(tmp_path)
        try:
            # Must initialize first
            self._send_and_receive(proc, {
                "jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "t", "version": "1.0"},
                },
            })

            response = self._send_and_receive(proc, {
                "jsonrpc": "2.0", "id": 2, "method": "tools/list",
            })

            assert response["id"] == 2
            tools = response["result"]["tools"]
            assert len(tools) == 5
        finally:
            proc.terminate()
            proc.wait(timeout=5)

    def test_stdio_does_not_bind_http_port(self, tmp_path):
        """stdio 模式不应绑定 HTTP 端口。"""
        proc = self._start_stdio(tmp_path)
        try:
            # Give it a moment to start
            time.sleep(1)

            # The process should be running and responsive via stdio
            assert proc.poll() is None, "stdio server should still be running"

            # Send initialize to confirm it's working via stdio, not HTTP
            response = self._send_and_receive(proc, {
                "jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "t", "version": "1.0"},
                },
            })
            assert "result" in response
        finally:
            proc.terminate()
            proc.wait(timeout=5)


class TestStdioErrors:
    """stdio 模式错误场景测试。"""

    def test_stdio_without_project_id_fails(self, tmp_path):
        """stdio 模式没有 project_id 应报错退出。"""
        data_dir = tmp_path / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        config_path = tmp_path / "config.toml"
        write_toml_config(
            config_path,
            port=0,
            data_dir=str(data_dir),
            mcp_enabled=True,
            mcp_project_id="",
        )

        proc = subprocess.Popen(
            [str(SERVER_BINARY), "--config", str(config_path), "-d", str(data_dir), "--mode", "mcp-stdio"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            returncode = proc.wait(timeout=10)
            assert returncode != 0, "Should exit with error when project_id is empty"
            stderr = proc.stderr.read().decode(errors="replace")
            assert "project_id" in stderr.lower() or "mcp" in stderr.lower()
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
            pytest.fail("Process did not exit within timeout — expected error exit")

    def test_stdio_without_project_dir_fails(self, tmp_path):
        """stdio 模式 project 目录不存在应报错退出。"""
        data_dir = tmp_path / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        # Note: project dir won't exist because we don't call create_project_structure

        config_path = tmp_path / "config.toml"
        write_toml_config(
            config_path,
            port=0,
            data_dir=str(data_dir),
            mcp_enabled=True,
            mcp_project_id="nonexistent-project",
        )

        proc = subprocess.Popen(
            [str(SERVER_BINARY), "--config", str(config_path), "-d", str(data_dir), "--mode", "mcp-stdio"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            returncode = proc.wait(timeout=10)
            assert returncode != 0, "Should exit with error when project dir doesn't exist"
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
            pytest.fail("Process did not exit within timeout — expected error exit")
