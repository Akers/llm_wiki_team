## Context

llm_wiki_lite 是一个 Rust（Actix Web 4）编写的 LLM-Wiki HTTP API 服务器，核心功能包括文档摄入（PDF/DOCX 等 → LLM 分析 → 结构化 Wiki）、混合搜索（关键词 + 向量 + RRF）、深度研究、流式聊天等。README 声称支持 MCP，但代码中完全没有实现。

现有技术栈：Actix Web 4、LanceDB、tokio、reqwest（LLM 流式调用）。项目采用模块化结构（api/、pipeline/、wiki/、fs/、vector/ 等），各模块职责清晰。已有完善的摄入管线（pipeline::ingest）和搜索管线（pipeline::search），MCP 工具可直接复用。

## Goals / Non-Goals

**Goals:**
- 在 Actix Web 中集成 MCP SSE 端点，HTTP API 与 MCP 共存于同一进程
- 支持 stdio 传输模式（通过 `--mode mcp-stdio` 启动）
- 暴露 5 个核心 MCP 工具，覆盖查询（搜索、读取）和维护（写入、摄入、查询状态）闭环
- 复用现有 pipeline 和 wiki/fs 模块，不改动现有业务逻辑
- 单项目绑定模式，通过配置指定 project_id

**Non-Goals:**
- 不实现 MCP Resources、Prompts、Sampling 等高级能力（仅实现 Tools）
- 不支持多项目动态切换
- 不改动现有 REST API 的行为
- 不实现 MCP 认证/授权（依赖现有网络安全策略）
- 不实现 MCP 通知（notifications）机制

## Decisions

### 1. rmcp crate v1.5 作为 MCP SDK

**选择**：使用官方 Rust MCP SDK（rmcp v1.5）

**理由**：rmcp 是 MCP 官方维护的 Rust SDK，支持最新 MCP 规范（2025-03-26+），提供 `#[tool_router]` 宏简化工具定义，原生支持 SSE 和 stdio 传输。8.3M+ 下载量，953 个反向依赖，生产就绪。

**备选方案**：
- 手写 MCP 协议：工作量大，易出错，不利于后续升级
- Python/TS proxy 服务：多一层网络开销和进程管理

### 2. 手动 JSON-RPC 2.0 分发器（非 rmcp StreamableHttpService）

**选择**：在 `api/mcp.rs` 中实现手动 JSON-RPC 2.0 分发器，处理 POST /mcp 和 GET /sse

**理由**：
- rmcp 的 `StreamableHttpService` 依赖 Tower/Axum 生态，与 Actix Web 4 集成困难
- 手动分发逻辑简洁、依赖少、协议控制完整
- 实现难度低：只需解析 JSON-RPC 请求并调用 WikiServer 的工具方法

**端点设计**：
- `POST /mcp` — 接收 JSON-RPC 2.0 请求，处理 `initialize`、`tools/list`、`tools/call`、`ping`
- `GET /sse` — SSE keep-alive 流，每 30 秒发送 `: ping\n\n`（供需要 SSE 的 MCP 客户端使用）

**备选方案**：
- rmcp StreamableHttpService：需要复杂的 Actix-Tower 桥接层
- 独立 binary：需要重构项目结构

### 3. ingest_text 异步设计

**选择**：ingest_text 立即返回 task_id，通过 check_ingest_status 查询结果

**理由**：LLM 摄入管线耗时较长（30s-2min+），同步阻塞会违反 MCP 协议的响应时间预期。异步设计允许 Agent 在等待期间执行其他任务。

**实现**：复用现有 `pipeline::ingest_queue` 的持久化队列，将文本写入临时文件后入队。

**Completed Task 保留**：完成的 ingest task 会保留在队列中（不被移除），通过 `IngestTask.output_paths: Vec<String>` 字段存储生成的 wiki 页面路径。`check_ingest_status` 对已完成任务返回 `wiki_page_paths` 字段。

**isError 检测**：工具返回结果通过 `serde_json::from_str::<Value>` 解析，检查顶层是否存在 `"error"` 键来判断是否为错误响应。

### 4. 单项目绑定

**选择**：通过配置文件 `[mcp].project_id` 绑定单个项目

**理由**：简化 MCP 工具参数（无需每个工具都传 project_id），减少 Agent 使用复杂度。大多数 Agent 场景只需操作一个知识库。

**环境变量配置**：
- `MCP_PROJECT_ID` — 指定项目 ID（覆盖配置文件）
- `MCP_ENABLED` — 启用/禁用 MCP 端点（默认 `true`）

## Risks / Trade-offs

- **[MCP SSE 长连接]** → Actix Web 需要正确处理 SSE 长连接和断线重连。缓解：使用 `HttpResponse::streaming` 配合 `IntervalStream` 发送 keep-alive。
- **[rmcp 版本快速迭代]** → rmcp 在 1.x 阶段可能有 breaking changes。缓解：Cargo.toml 中锁定具体版本。
- **[ingest_text 临时文件管理]** → 异步摄入产生的临时文件需要清理。缓解：复用 ingest_queue 的现有清理机制。
- **[单项目限制]** → 用户可能需要 Agent 操作多个项目。缓解：可通过 docker-compose 启动多个实例绑定不同项目。
