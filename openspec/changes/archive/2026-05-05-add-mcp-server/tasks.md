## 1. Dependencies & Cargo Configuration

- [x] 1.1 Add `rmcp = { version = "1.5", features = ["server", "transport-io", "transport-streamable-http-server", "macros", "schemars"] }` and `schemars = "0.8"` to `[dependencies]` in `src-server/Cargo.toml`
- [x] 1.2 Run `cargo check` in `src-server/` to verify dependencies resolve
- [x] 1.3 Commit: `chore: add rmcp and schemars dependencies`

## 2. MCP Config Struct

- [x] 2.1 Write failing test: create `src-server/src/config.rs` test module (if not exists) — test `McpConfig::default()` returns `enabled=true, project_id=""`
- [x] 2.2 Run test, verify it fails (`McpConfig` not defined)
- [x] 2.3 Add `McpConfig` struct to `src-server/src/config.rs` with fields: `enabled: bool` (default true), `project_id: String` (default ""), derive `Debug, Clone, Serialize, Deserialize`
- [x] 2.4 Add `pub mcp: McpConfig` field to `Config` struct, add default in `Default` impl
- [x] 2.5 Run test, verify it passes
- [x] 2.6 Write failing test: test `Config::load` parses TOML with `[mcp]` section correctly
- [x] 2.7 Run test, verify it fails
- [x] 2.8 Add `[mcp]` section handling to TOML deserialization (already covered by serde derive)
- [x] 2.9 Run test, verify it passes
- [x] 2.10 Write failing test: test `MCP_PROJECT_ID` env var overrides `mcp.project_id`
- [x] 2.11 Run test, verify it fails
- [x] 2.12 Add `MCP_PROJECT_ID` env var override in `Config::apply_overrides()` after existing env var overrides (around line 172)
- [x] 2.13 Run test, verify it passes
- [x] 2.14 Update `src-server/config.example.toml`: add `[mcp]` section with `enabled = true` and `# project_id = ""` comment
- [x] 2.15 Commit: `feat: add McpConfig struct with TOML and env var support`

## 3. CLI `--mode` Flag

- [x] 3.1 Write failing test: test `Cli::parse_from(["prog", "--mode", "mcp-stdio"])` returns `mode = "mcp-stdio"`
- [x] 3.2 Run test, verify it fails (`mode` field not defined)
- [x] 3.3 Add `#[arg(long, default_value = "http")] mode: String` to `Cli` struct in `src-server/src/main.rs` (line 23)
- [x] 3.4 Run test, verify it passes
- [x] 3.5 Commit: `feat: add --mode CLI flag`

## 4. MCP Module Skeleton

- [x] 4.1 Create `src-server/src/mcp/mod.rs` with `pub mod server; pub mod tools;`
- [x] 4.2 Add `mod mcp;` to `src-server/src/main.rs` module declarations (after `mod wiki;`, line 19)
- [x] 4.3 Create `src-server/src/mcp/server.rs` with empty `pub struct WikiServer` and `pub mod tools;` placeholder
- [x] 4.4 Create `src-server/src/mcp/tools.rs` as empty file
- [x] 4.5 Run `cargo check`, verify module compiles
- [x] 4.6 Commit: `feat: create mcp module skeleton`

## 5. Tool Parameter Structs

- [x] 5.1 Write failing test: in `src-server/src/mcp/tools.rs`, add `#[cfg(test)] mod tests` — test `serde_json::from_value::<SearchParams>(json)` deserializes correctly
- [x] 5.2 Run test, verify it fails (`SearchParams` not defined)
- [x] 5.3 Define `SearchParams { query: String }` with `Debug, Deserialize, JsonSchema` derives in `tools.rs`
- [x] 5.4 Run test, verify it passes
- [x] 5.5 Write failing test: test `ReadPageParams` deserialization
- [x] 5.6 Define `ReadPageParams { path: String }` in `tools.rs`
- [x] 5.7 Run test, verify it passes
- [x] 5.8 Write failing test: test `WritePageParams` deserialization
- [x] 5.9 Define `WritePageParams { path: String, content: String }` in `tools.rs`
- [x] 5.10 Run test, verify it passes
- [x] 5.11 Write failing test: test `IngestTextParams` deserialization (with optional fields)
- [x] 5.12 Define `IngestTextParams { content: String, title: Option<String>, source_type: Option<String> }` in `tools.rs`
- [x] 5.13 Run test, verify it passes
- [x] 5.14 Write failing test: test `CheckIngestStatusParams` deserialization
- [x] 5.15 Define `CheckIngestStatusParams { task_id: String }` in `tools.rs`
- [x] 5.16 Run test, verify it passes
- [x] 5.17 Commit: `feat: define MCP tool parameter structs`

## 6. Path Validation Helper

- [x] 6.1 Write failing test: test `validate_wiki_path("concepts/rust.md")` returns `Ok(())`
- [x] 6.2 Write failing test: test `validate_wiki_path("../etc/passwd")` returns `Err` with security message
- [x] 6.3 Write failing test: test `validate_wiki_path("/absolute/path")` returns `Err`
- [x] 6.4 Run tests, verify they fail
- [x] 6.5 Implement `pub fn validate_wiki_path(path: &str) -> Result<(), String>` in `src-server/src/mcp/tools.rs` — reject paths containing `..`, starting with `/`, or containing `\0`
- [x] 6.6 Run tests, verify they pass
- [x] 6.7 Commit: `feat: add path validation for MCP tools`

## 7. search_wiki Tool

- [x] 7.1 Write failing test: test `search_wiki` with mock project containing a wiki file returns results with path/title/score
- [x] 7.2 Run test, verify it fails
- [x] 7.3 Implement `search_wiki` tool method on `WikiServer` — accept `SearchParams`, call `pipeline::search::search_wiki(project_path, query, config)`, map results to JSON, return top 10
- [x] 7.4 Run test, verify it passes
- [x] 7.5 Write failing test: test `search_wiki` with empty query returns error
- [x] 7.6 Add query non-empty validation, run test, verify it passes
- [x] 7.7 Commit: `feat: implement search_wiki MCP tool`

## 8. read_wiki_page Tool

- [x] 8.1 Write failing test: test `read_wiki_page` reads existing file content correctly
- [x] 8.2 Run test, verify it fails
- [x] 8.3 Implement `read_wiki_page` tool — call `validate_wiki_path`, construct full path `{project}/wiki/{path}`, call `std::fs::read_to_string`, return content
- [x] 8.4 Run test, verify it passes
- [x] 8.5 Write failing test: test `read_wiki_page` with non-existent file returns error suggesting search_wiki
- [x] 8.6 Add file-not-found error handling, run test, verify it passes
- [x] 8.7 Write failing test: test `read_wiki_page` with `..` path returns validation error
- [x] 8.8 Run test, verify it passes (already handled by `validate_wiki_path`)
- [x] 8.9 Commit: `feat: implement read_wiki_page MCP tool`

## 9. write_wiki_page Tool

- [x] 9.1 Write failing test: test `write_wiki_page` creates new file and returns success
- [x] 9.2 Run test, verify it fails
- [x] 9.3 Implement `write_wiki_page` tool — call `validate_wiki_path`, create parent dirs, call `std::fs::write`, return confirmation
- [x] 9.4 Run test, verify it passes
- [x] 9.5 Write failing test: test `write_wiki_page` overwrites existing file
- [x] 9.6 Run test, verify it passes (std::fs::write overwrites by default)
- [x] 9.7 Write failing test: test `write_wiki_page` with `..` path returns validation error
- [x] 9.8 Run test, verify it passes
- [x] 9.9 Commit: `feat: implement write_wiki_page MCP tool`

## 10. ingest_text Tool (Content Validation & Enqueue)

- [x] 10.1 Write failing test: test content size validation rejects content > 100KB (102400 bytes)
- [x] 10.2 Run test, verify it fails
- [x] 10.3 Add `const MAX_CONTENT_SIZE: usize = 102_400;` and size check in `ingest_text` tool
- [x] 10.4 Run test, verify it passes
- [x] 10.5 Write failing test: test `ingest_text` writes temp file and returns task_id
- [x] 10.6 Run test, verify it fails
- [x] 10.7 Implement `ingest_text` — write `content` to temp file under `{project}/sources/mcp-ingest/`, call `pipeline::ingest_queue::enqueue_ingest`, return task_id
- [x] 10.8 Run test, verify it passes
- [x] 10.9 Write failing test: test `ingest_text` without content returns error
- [x] 10.10 Run test, verify it passes (rmcp schema enforces required fields, but double-check)
- [x] 10.11 Commit: `feat: implement ingest_text MCP tool`

## 11. check_ingest_status Tool

- [x] 11.1 Write failing test: test `check_ingest_status` for pending task returns status "pending"
- [x] 11.2 Run test, verify it fails
- [x] 11.3 Implement `check_ingest_status` — call `pipeline::ingest_queue::queue_status`, find task by ID, return status
- [x] 11.4 Run test, verify it passes
- [x] 11.5 Write failing test: test `check_ingest_status` for unknown task_id returns "not found" error
- [x] 11.6 Run test, verify it passes
- [x] 11.7 Commit: `feat: implement check_ingest_status MCP tool`

## 12. WikiServer Struct with rmcp ServerHandler

- [x] 12.1 Write failing test: test `WikiServer` implements `rmcp::handler::server::ServerHandler` trait
- [x] 12.2 Run test, verify it fails
- [x] 12.3 Implement `ServerHandler` for `WikiServer` — `get_info()` returns `ServerInfo { name: "llm-wiki-lite", version: env!("CARGO_PKG_VERSION"), capabilities: enable_tools() }`
- [x] 12.4 Apply `#[tool_router(server_handler)]` macro to `impl WikiServer` block containing all 5 tools
- [x] 12.5 Add `WikiServer` fields: `project_path: String`, `project_id: String`, `config: std::sync::Arc<crate::config::Config>`
- [x] 12.6 Add `pub fn new(project_id, project_path, config)` constructor
- [x] 12.7 Run test, verify it passes
- [x] 12.8 Commit: `feat: implement WikiServer with rmcp ServerHandler`

## 13. Project-Bound State for MCP Tools

- [x] 13.1 Write failing test: test `WikiServer::new("bad-id", "/nonexistent", config)` — calling any tool returns error "project not found or not accessible"
- [x] 13.2 Run test, verify it fails
- [x] 13.3 Add project validation in `WikiServer::new()` — verify `{data_dir}/{project_id}/wiki/` exists
- [x] 13.4 Run test, verify it passes
- [x] 13.5 Write failing test: test MCP tools error when `project_id` is empty
- [x] 13.6 Add empty project_id guard in each tool, run test, verify it passes
- [x] 13.7 Commit: `feat: add project validation to WikiServer`

## 14. SSE Transport — Actix Web MCP Endpoint

- [x] 14.1 Create `src-server/src/api/mcp.rs` with empty module
- [x] 14.2 Write failing test: test `POST /mcp` with valid MCP `initialize` request returns 200 with JSON-RPC response
- [x] 14.3 Run test, verify it fails
- [x] 14.4 Implement `pub async fn mcp_post()` Actix handler — manual JSON-RPC dispatch to WikiServer tools (avoids Tower/Actix bridging)
- [x] 14.5 Run test, verify it passes
- [x] 14.6 Add `use actix_web::web::Bytes;` and `use futures::stream::StreamExt;` imports
- [x] 14.7 Create `sse_get()` handler with SSE response
- [x] 14.8 Add SSE keep-alive ping using tokio interval stream
- [x] 14.9 Register GET /sse route in `register_routes()`
- [x] 14.10 Commit: `feat: add MCP SSE endpoint handlers`

## 15. Register MCP Routes in Actix Web

- [x] 15.1 Write failing test: test that `GET /sse` returns 200 (not 404) when MCP is enabled
- [x] 15.2 Run test, verify it fails
- [x] 15.3 Add `pub mod mcp;` to `src-server/src/api/mod.rs` (after line 11)
- [x] 15.4 Add MCP routes via `api::mcp::register_routes()` — `POST /mcp` route registered conditionally when WikiServer is available
- [x] 15.5 Pass `WikiServer` via `web::Data` to Actix app (routes extract it from app state)
- [x] 15.6 Run test, verify it passes
- [x] 15.7 Test: MCP routes return 404 when MCP is disabled
- [x] 15.8 Test: MCP routes return 200 when MCP is enabled with valid project
- [x] 15.9 Commit: `feat: register MCP routes conditionally`

## 16. Store WikiServer in App State

- [x] 16.1 Add `Option<web::Data<WikiServer>>` to app state in `main.rs`
- [x] 16.2 Initialize `WikiServer` in `main.rs` when `mcp.enabled && !mcp.project_id.is_empty()` — resolve project path from `data_dir/project_id`
- [x] 16.3 Pass `WikiServer` via `app_data()` to Actix app
- [x] 16.4 Update `api/mcp.rs` handlers to extract `web::Data<WikiServer>` from request
- [x] 16.5 Run `cargo check`, verify compilation
- [x] 16.6 Commit: `feat: initialize WikiServer in app state`

## 17. Stdio Transport Mode

- [x] 17.1 Write failing test: test `main` with `--mode mcp-stdio` starts stdio server (integration-level)
- [x] 17.2 Add match branch in `main()` for `cli.mode == "mcp-stdio"` — init config, init `WikiServer`, call `rmcp::ServiceExt::serve(transport::io::stdio())`
- [x] 17.3 Ensure pipeline state (Queues) is initialized for stdio mode
- [x] 17.4 Run `cargo check`, verify compilation
- [x] 17.5 Commit: `feat: add mcp-stdio startup mode`

## 18. End-to-End Smoke Tests

- [x] 18.1 Manual test: start server in default mode, send MCP `initialize` via `curl POST /mcp`, verify response with server info
- [x] 18.2 Manual test: start server, call `tools/list` via MCP, verify 5 tools returned
- [x] 18.3 Manual test: call `search_wiki` tool via MCP with a real project, verify results
- [x] 18.4 Manual test: call `read_wiki_page` tool, verify content returned
- [x] 18.5 Manual test: call `write_wiki_page` tool, verify file created on disk
- [x] 18.6 Manual test: call `ingest_text` tool, verify task_id returned, then `check_ingest_status` shows progress
- [x] 18.7 Manual test: start with `--mode mcp-stdio`, send `initialize` via stdin, verify response on stdout
- [x] 18.8 Commit: `test: add e2e smoke test notes`
