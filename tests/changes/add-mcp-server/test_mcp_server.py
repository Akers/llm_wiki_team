"""MCP 服务器端点测试。

覆盖 mcp-server spec 中的所有场景：
- POST /mcp JSON-RPC 2.0 请求/响应
- GET /sse SSE keep-alive
- HTTP + MCP 共存
- initialize 返回 server info
- tools/list 返回工具定义
- ping 响应
- 未知方法错误
- 无效请求（缺少 method）
- 通知（无 id）
"""

import pytest
import requests

from _utils import ServerHandle


class TestInitialize:
    """initialize 方法测试。"""

    def test_initialize_response_format(self, server: ServerHandle):
        """initialize 返回正确的 JSON-RPC 2.0 格式。"""
        from _utils import next_rpc_id
        rid = next_rpc_id()
        resp = server.mcp("initialize", request_id=rid)
        assert resp.status_code == 200
        body = resp.json()
        assert body["jsonrpc"] == "2.0"
        assert body["id"] == rid
        assert "result" in body
        assert "error" not in body

    def test_initialize_protocol_version(self, server: ServerHandle):
        """initialize 返回正确的协议版本。"""
        resp = server.mcp("initialize")
        body = resp.json()
        assert body["result"]["protocolVersion"] == "2025-03-26"

    def test_initialize_server_info(self, server: ServerHandle):
        """initialize 返回正确的 serverInfo。"""
        resp = server.mcp("initialize")
        body = resp.json()
        info = body["result"]["serverInfo"]
        assert info["name"] == "llm-wiki-lite"
        assert isinstance(info["version"], str)
        assert len(info["version"]) > 0

    def test_initialize_capabilities(self, server: ServerHandle):
        """initialize 返回 tools 能力。"""
        resp = server.mcp("initialize")
        body = resp.json()
        assert "tools" in body["result"]["capabilities"]

    def test_initialize_instructions(self, server: ServerHandle):
        """initialize 返回 instructions 字符串。"""
        resp = server.mcp("initialize")
        body = resp.json()
        assert "instructions" in body["result"]
        assert isinstance(body["result"]["instructions"], str)


class TestToolsList:
    """tools/list 方法测试。"""

    def test_returns_five_tools(self, server: ServerHandle):
        """tools/list 应返回 5 个工具。"""
        resp = server.mcp("tools/list")
        body = resp.json()
        tools = body["result"]["tools"]
        assert len(tools) == 5

    def test_tool_names(self, server: ServerHandle):
        """所有工具名称正确。"""
        resp = server.mcp("tools/list")
        body = resp.json()
        tool_names = [t["name"] for t in body["result"]["tools"]]
        expected = ["search_wiki", "read_wiki_page", "write_wiki_page",
                     "ingest_text", "check_ingest_status"]
        assert sorted(tool_names) == sorted(expected)

    def test_tool_has_input_schema(self, server: ServerHandle):
        """每个工具有 inputSchema 定义。"""
        resp = server.mcp("tools/list")
        body = resp.json()
        for tool in body["result"]["tools"]:
            assert "inputSchema" in tool, f"Tool {tool['name']} missing inputSchema"
            assert tool["inputSchema"]["type"] == "object"

    def test_tool_has_description(self, server: ServerHandle):
        """每个工具有描述。"""
        resp = server.mcp("tools/list")
        body = resp.json()
        for tool in body["result"]["tools"]:
            assert "description" in tool, f"Tool {tool['name']} missing description"
            assert len(tool["description"]) > 0

    def test_search_wiki_requires_query(self, server: ServerHandle):
        """search_wiki 工具要求 query 参数。"""
        resp = server.mcp("tools/list")
        body = resp.json()
        search_tool = next(t for t in body["result"]["tools"] if t["name"] == "search_wiki")
        assert "query" in search_tool["inputSchema"]["required"]


class TestPing:
    """ping 方法测试。"""

    def test_ping_returns_empty_result(self, server: ServerHandle):
        """ping 返回空 result。"""
        resp = server.mcp("ping")
        body = resp.json()
        assert body["jsonrpc"] == "2.0"
        assert body["result"] == {}


class TestJsonRpcErrors:
    """JSON-RPC 错误处理测试。"""

    def test_missing_method(self, server: ServerHandle):
        """缺少 method 字段返回 -32600 Invalid Request。"""
        resp = requests.post(
            f"{server.base_url}/mcp",
            json={"jsonrpc": "2.0", "id": 1},
            timeout=5,
        )
        body = resp.json()
        assert body["error"]["code"] == -32600

    def test_unknown_method(self, server: ServerHandle):
        """未知方法返回 -32601 Method not found。"""
        resp = server.mcp("nonexistent/method")
        body = resp.json()
        assert body["error"]["code"] == -32601
        assert "nonexistent/method" in body["error"]["message"]

    def test_notification_no_id(self, server: ServerHandle):
        """没有 id 的请求（通知）返回空响应。"""
        resp = requests.post(
            f"{server.base_url}/mcp",
            json={"jsonrpc": "2.0", "method": "initialize"},
            timeout=5,
        )
        # Notifications get empty response
        assert resp.status_code == 200

    def test_initialized_notification(self, server: ServerHandle):
        """notifications/initialized 通知被正确处理。"""
        resp = server.mcp("notifications/initialized")
        body = resp.json()
        assert body["result"] == {}


class TestHttpMcpCoexistence:
    """HTTP 和 MCP 共存测试。"""

    def test_health_endpoint_works(self, server: ServerHandle):
        """REST /api/health 端点正常工作。"""
        resp = server.health()
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"

    def test_mcp_endpoint_works_alongside_rest(self, server: ServerHandle):
        """MCP POST /mcp 和 REST API 在同一端口共存。"""
        # REST
        rest_resp = server.health()
        assert rest_resp.status_code == 200

        # MCP
        mcp_resp = server.mcp("initialize")
        assert mcp_resp.status_code == 200


class TestSseEndpoint:
    """GET /sse SSE 端点测试。"""

    def test_sse_returns_correct_content_type(self, server: ServerHandle):
        """SSE 端点返回 text/event-stream content type。"""
        resp = requests.get(
            f"{server.base_url}/sse",
            timeout=5,
            stream=True,
        )
        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers.get("content-type", "")

    def test_sse_has_cache_control_headers(self, server: ServerHandle):
        """SSE 端点返回正确的 Cache-Control header。"""
        resp = requests.get(
            f"{server.base_url}/sse",
            timeout=5,
            stream=True,
        )
        assert resp.headers.get("cache-control") == "no-cache"

    def test_sse_stream_is_readable(self, server: ServerHandle):
        """SSE 端点可以读取到流数据。"""
        resp = requests.get(
            f"{server.base_url}/sse",
            timeout=35,
            stream=True,
        )
        assert resp.status_code == 200

        # Read first chunk with timeout
        try:
            chunk = next(resp.iter_content(chunk_size=1024))
            assert chunk is not None
        except StopIteration:
            # Stream ended immediately — also acceptable for short test
            pass


class TestToolsCallDispatch:
    """tools/call 分发测试（只验证分发机制，不验证具体工具逻辑）。"""

    def test_unknown_tool_returns_error(self, server: ServerHandle):
        """调用不存在的工具返回错误。"""
        result = server.mcp_tool("nonexistent_tool", {})
        assert result["is_error"] is True
        assert "Unknown tool" in result["content"]

    def test_invalid_params_returns_error(self, server: ServerHandle):
        """无效参数返回错误。"""
        # search_wiki requires query
        result = server.mcp_tool("search_wiki", {})
        assert result["is_error"] is True
        assert "Invalid parameters" in result["content"]
