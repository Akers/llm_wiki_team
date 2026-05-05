# add-mcp-server 变更测试

## 变更概述

为 llm-wiki-server 添加 MCP (Model Context Protocol) 服务器支持，包括：

- `[mcp]` 配置段（enabled / project_id）
- 环境变量覆盖（MCP_PROJECT_ID / MCP_ENABLED）
- `--mode` CLI 参数（http / mcp-stdio）
- POST /mcp JSON-RPC 2.0 端点
- GET /sse SSE keep-alive 端点
- stdio transport 模式
- 5 个 MCP 工具：search_wiki, read_wiki_page, write_wiki_page, ingest_text, check_ingest_status

## 测试覆盖

### mcp-config 规格覆盖 (6/6 scenarios)

| 测试文件 | 场景 | 描述 |
|----------|------|------|
| test_mcp_config.py | MCP enabled with valid project | 服务启动，MCP 路由可用 |
| test_mcp_config.py | MCP disabled | POST /mcp 返回 404 |
| test_mcp_config.py | MCP enabled without project_id | MCP 路由未注册 |
| test_mcp_config.py | MCP_PROJECT_ID env override | 环境变量覆盖配置 |
| test_mcp_config.py | MCP_ENABLED env override | false 禁用 MCP |
| test_mcp_config.py | --mode http | HTTP 模式启动正常 |

### mcp-server 规格覆盖 (7/7 scenarios)

| 测试文件 | 场景 | 描述 |
|----------|------|------|
| test_mcp_server.py | GET /sse | SSE 连接建立，正确 headers |
| test_mcp_server.py | POST /mcp valid JSON-RPC | 正确 JSON-RPC 2.0 响应 |
| test_mcp_server.py | HTTP+MCP coexist | /api/health 和 /mcp 同时可用 |
| test_mcp_server.py | initialize | 返回 llm-wiki-lite + version + tools 能力 |
| test_mcp_server.py | tools/list | 返回 5 个工具定义 |
| test_mcp_server.py | ping | 返回空 result |
| test_mcp_server.py | unknown method | 返回 -32601 错误 |

### mcp-tools 规格覆盖 (17/17 scenarios)

| 测试文件 | 场景 | 描述 |
|----------|------|------|
| test_mcp_tools.py | search_wiki 有结果 | 返回最多 10 条结果 |
| test_mcp_tools.py | search_wiki 无结果 | 空列表 |
| test_mcp_tools.py | search_wiki 缺少 query | 返回参数错误 |
| test_mcp_tools.py | search_wiki 空 query | 返回错误 |
| test_mcp_tools.py | read_wiki_page 正常 | 返回页面内容 |
| test_mcp_tools.py | read_wiki_page 不存在 | 错误 + 搜索建议 |
| test_mcp_tools.py | read_wiki_page 路径遍历 | 返回安全错误 |
| test_mcp_tools.py | write_wiki_page 创建 | 新建页面成功 |
| test_mcp_tools.py | write_wiki_page 覆盖 | 更新已有页面 |
| test_mcp_tools.py | write_wiki_page 路径遍历 | 返回安全错误 |
| test_mcp_tools.py | ingest_text 正常 | 返回 task_id |
| test_mcp_tools.py | ingest_text >100KB | 返回大小错误 |
| test_mcp_tools.py | ingest_text 空内容 | 返回参数错误 |
| test_mcp_tools.py | check_ingest_status pending | 返回 pending 状态 |
| test_mcp_tools.py | check_ingest_status completed | 返回 done + wiki_page_paths |
| test_mcp_tools.py | check_ingest_status 未知 ID | 返回 not found |
| test_mcp_tools.py | unknown tool | 返回未知工具错误 |

### stdio transport 覆盖

| 测试文件 | 场景 | 描述 |
|----------|------|------|
| test_mcp_stdio.py | stdio initialize | 通过 stdin/stdout 交互 |
| test_mcp_stdio.py | stdio tools/list | 返回 5 个工具 |
| test_mcp_stdio.py | 无 project_id 启动 | 进程退出并报错 |

## 异常流覆盖

- 无效 JSON-RPC（缺少 method）
- 未知方法名
- 未知工具名
- 工具参数缺失/无效
- 路径遍历攻击（read 和 write）
- 内容超限（100KB）
- 空内容提交
- 不存在的页面/任务 ID
- MCP 禁用/无项目时路由不可用
