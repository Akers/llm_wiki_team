## Why

llm_wiki_lite 的 README 声称支持 MCP 接入，但代码中完全没有实现。当前 AI Agent 无法通过标准化协议（Model Context Protocol）与 Wiki 知识库交互，只能通过 REST API 手动集成。需要提供原生 MCP 接口，让 Agent 能够以标准化方式查询知识库、读取/写入 Wiki 页面、以及通过 LLM 管线智能摄入文本，形成完整的知识管理闭环。

## What Changes

- 新增 MCP Server 模块，基于 rmcp crate v1.5 实现，支持 SSE 和 stdio 双传输模式
- 新增 5 个 MCP 工具：search_wiki、read_wiki_page、write_wiki_page、ingest_text、check_ingest_status
- 在 Actix Web 路由中集成 MCP SSE 端点（POST /mcp、GET /sse），HTTP API 与 MCP 共存于同一进程
- 增加 `--mode mcp-stdio` CLI 参数，支持纯 stdio MCP Server 启动
- 新增 `[mcp]` 配置段（enabled、project_id），支持单项目绑定模式
- 新增 Cargo 依赖：rmcp v1.5、schemars v0.8

## Capabilities

### New Capabilities
- `mcp-server`: MCP Server 核心能力，包括 ServerHandler 定义、传输层（SSE/stdio）、工具注册与路由
- `mcp-tools`: 5 个 MCP 工具的实现（search_wiki、read_wiki_page、write_wiki_page、ingest_text、check_ingest_status），每个工具定义输入参数、输出格式、内部调用逻辑和错误处理
- `mcp-config`: MCP 相关配置管理，包括启动模式、项目绑定、SSE 端点路由

### Modified Capabilities
<!-- 无现有 specs 需要修改 -->

## Impact

- **代码**：新增 `src/mcp/` 模块（3 个文件）、新增 `src/api/mcp.rs`、修改 `main.rs`（启动分支）、修改 `config.rs`（配置项）、修改 `api/mod.rs`（路由注册）
- **依赖**：新增 rmcp v1.5（含 server、transport-sse、transport-streamable-http features）、schemars v0.8
- **配置**：新增 `[mcp]` 配置段
- **API**：新增 POST /mcp 和 GET /sse 端点（与现有 REST API 无冲突）
- **构建**：Dockerfile 可能需要更新以支持 mcp-stdio 模式的入口点
