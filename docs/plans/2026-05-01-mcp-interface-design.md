# llm_wiki_lite MCP 接口设计文档

## 概述

在 `llm_wiki_lite` 子模块中增加标准 MCP (Model Context Protocol) 接口，使通用 MCP 客户端（Claude Desktop、Cursor 等）能够通过 MCP 协议调用 Wiki 的查询和文档管理功能。

## 需求

- **兼容标准 MCP 客户端**：支持 Claude Desktop、Cursor 等标准 MCP 客户端发现和调用
- **查询功能**：搜索 Wiki 内容（混合搜索：分词 + 向量 + RRF 融合）
- **添加文档功能**：Agent 直接传入文本内容（Markdown）写入 Wiki 页面
- **项目上下文**：Agent 通过参数指定项目名/ID
- **传输方式**：同时支持 stdio 和 Streamable HTTP / SSE

## 技术选型

**SDK**：`rmcp` — MCP 官方 Rust SDK (modelcontextprotocol/rust-sdk)

选择理由：
- MCP 官方组织维护，长期稳定性有保障
- 支持 stdio + Streamable HTTP 双传输
- 提供 `#[tool]` 宏简化 Tool 定义
- 有 `rmcp-actix-web` 集成示例，与现有 Actix Web 框架兼容

**Cargo 依赖**：
```toml
rmcp = { version = "0.16", features = ["server", "transport-io", "transport-streamable-http-server", "schemars"] }
```

## 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────┐
│              LLM Wiki Server (Actix Web 4)          │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │  现有 REST API │  │  MCP 端点     │                │
│  │  /api/...     │  │  /mcp (SSE)  │                │
│  └──────┬───────┘  └──────┬───────┘                 │
│         │                 │                          │
│         ▼                 ▼                          │
│  ┌─────────────────────────────────────────────┐    │
│  │         共享业务逻辑层 (Pipeline/Project)     │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘

┌──────────────────────────┐
│  独立 stdio 入口          │
│  bin/mcp_server.rs       │
│  (子进程模式，共享 Handler) │
└──────────────────────────┘
```

### 模块结构

```
llm_wiki_lite/src-server/src/
├── mcp/
│   ├── mod.rs          # 模块入口，导出 handler 和 transport
│   ├── handler.rs      # ServerHandler 实现 + 3 个 Tool 定义
│   └── transport.rs    # Actix Web Streamable HTTP 端点集成
├── bin/
│   └── mcp_server.rs   # stdio 独立二进制入口
└── ...existing...
```

### MCP Tools 定义

| Tool 名称 | 描述 | 输入参数 | 返回内容 |
|-----------|------|---------|---------|
| `search_wiki` | 搜索 Wiki 内容（混合搜索：分词 + 向量 + RRF 融合） | `project` (string): 项目名或 ID, `query` (string): 搜索关键词 | 匹配结果列表（路径、标题、摘要片段、相关度分数） |
| `write_wiki_page` | 写入或创建 Wiki 页面 | `project` (string): 项目名或 ID, `path` (string): Wiki 文件路径（如 `concepts/my-concept.md`）, `content` (string): Markdown 内容 | 操作结果（成功/失败 + 文件路径） |
| `list_wiki_pages` | 列出 Wiki 目录结构 | `project` (string): 项目名或 ID, `prefix` (可选 string): 路径前缀过滤 | 文件树结构（路径列表 + 目录层级） |

### 传输方式

#### stdio 模式

- 入口：`bin/mcp_server.rs` 编译为独立二进制
- 通信：通过 stdin/stdout 进行 JSON-RPC 2.0 通信
- 配置示例（Claude Desktop）：
```json
{
  "mcpServers": {
    "llm-wiki": {
      "command": "llm-wiki-mcp",
      "args": []
    }
  }
}
```

#### Streamable HTTP / SSE 模式

- 端点：在现有 Actix Web 服务中新增 `/mcp` 路由
- 协议：Streamable HTTP（MCP 2025-03-26 规范），向后兼容 SSE
- 适合网络部署和多客户端并发场景

### 调用流程

#### stdio 模式

1. MCP 客户端启动 `llm-wiki-mcp` 子进程
2. 客户端发送 `initialize` 请求，服务端返回能力声明（含 3 个 Tools）
3. 客户端调用 `list_tools` 获取 Tool 列表
4. 客户端调用 `call_tool` 执行具体操作（搜索/写入/列出）
5. `ServerHandler` 内部调用现有 `pipeline::search`、Wiki 文件读写 API

#### Streamable HTTP 模式

1. 客户端连接 `http://host:port/mcp`
2. Actix Web 路由将请求转发到 `rmcp` 的 StreamableHttpService
3. 共享同一个 `ServerHandler` 实例处理 Tool 调用
4. 响应通过 SSE 流返回

### 错误处理

- 项目不存在：返回 MCP 错误（项目名/ID 无效）
- 搜索无结果：返回空列表（非错误）
- 写入路径无效：返回 MCP 错误（路径格式不合法）
- 文件系统错误：返回 MCP 错误（内部错误 + 描述信息）

## 与现有代码的关系

### 复用现有模块

| MCP Tool | 复用的现有模块 |
|----------|--------------|
| `search_wiki` | `pipeline::search::search()` — 混合搜索引擎 |
| `write_wiki_page` | `wiki` 文件写入操作 + `project::manager` 项目管理 |
| `list_wiki_pages` | `wiki` 文件树读取 + `project::manager` 项目管理 |

### 不修改的部分

- 现有 REST API 端点不变
- 现有 Pipeline 逻辑不变
- 现有数据库/存储层不变
- MCP 层只做调用，不做核心逻辑修改

## 开放问题

（无——所有关键决策已与用户确认）
