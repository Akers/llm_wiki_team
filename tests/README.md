# llm_wiki_team 测试套件

## 目录结构

```
tests/
├── conftest.py              # 共享 fixtures（ServerHandle, JSON-RPC 辅助函数等）
├── pytest.ini               # pytest 配置
├── README.md                # 本文件
└── changes/                 # 每个变更一个子目录
    └── add-mcp-server/      # MCP Server 变更测试
        ├── conftest.py      # MCP 特有 fixtures
        ├── test_mcp_config.py
        ├── test_mcp_server.py
        ├── test_mcp_tools.py
        ├── test_mcp_stdio.py
        └── README.md
```

## 前置条件

1. **编译服务端二进制**
   ```bash
   cd llm_wiki_lite/src-server && cargo build
   ```
   测试会自动使用 `target/debug/llm-wiki-server`。

2. **Python 依赖**
   ```bash
   pip install pytest requests
   ```

## 运行测试

```bash
# 运行全部测试
pytest tests/

# 仅运行 MCP 变更相关测试
pytest tests/changes/add-mcp-server/

# 运行单个测试文件
pytest tests/changes/add-mcp-server/test_mcp_server.py

# 运行特定测试用例
pytest tests/changes/add-mcp-server/test_mcp_tools.py::TestSearchWiki::test_search_returns_results
```

## 架构

### ServerHandle

每个需要启动服务器的测试使用 `server` fixture。该 fixture：

1. 在 `/tmp` 下创建临时数据目录
2. 写入 TOML 配置文件
3. 启动 `llm-wiki-server` 子进程（随机端口）
4. 轮询 `/api/health` 确认就绪
5. 测试结束后自动终止进程

### JSON-RPC 辅助

- `call_mcp(base_url, method, params)` — 发送 JSON-RPC 2.0 请求到 POST /mcp
- `call_mcp_tool(base_url, tool_name, arguments)` — 调用 MCP 工具并解析结果
- `ServerHandle.mcp(method, params)` — 通过 fixture 发送请求
- `ServerHandle.mcp_tool(name, args)` — 通过 fixture 调用工具
