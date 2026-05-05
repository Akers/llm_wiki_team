# Graph Report - .  (2026-05-05)

## Corpus Check
- 93 files · ~57,732 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 797 nodes · 1594 edges · 43 communities detected
- Extraction: 68% EXTRACTED · 32% INFERRED · 0% AMBIGUOUS · INFERRED: 515 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_API Response & Chat|API Response & Chat]]
- [[_COMMUNITY_MCP Config Tests|MCP Config Tests]]
- [[_COMMUNITY_HTTP API Endpoints|HTTP API Endpoints]]
- [[_COMMUNITY_Configuration System|Configuration System]]
- [[_COMMUNITY_MCP Tools Tests|MCP Tools Tests]]
- [[_COMMUNITY_MCP Test Fixtures|MCP Test Fixtures]]
- [[_COMMUNITY_Wiki Index & Links|Wiki Index & Links]]
- [[_COMMUNITY_Ingest Pipeline|Ingest Pipeline]]
- [[_COMMUNITY_Vector Store|Vector Store]]
- [[_COMMUNITY_System Architecture|System Architecture]]
- [[_COMMUNITY_Ingest Analysis|Ingest Analysis]]
- [[_COMMUNITY_Text Chunking|Text Chunking]]
- [[_COMMUNITY_LLM Providers|LLM Providers]]
- [[_COMMUNITY_Search Pipeline|Search Pipeline]]
- [[_COMMUNITY_Language Detection|Language Detection]]
- [[_COMMUNITY_Path Utilities|Path Utilities]]
- [[_COMMUNITY_Ingest Cache|Ingest Cache]]
- [[_COMMUNITY_Panic Guard|Panic Guard]]
- [[_COMMUNITY_Context Budget|Context Budget]]
- [[_COMMUNITY_Web Search|Web Search]]
- [[_COMMUNITY_Wiki Templates|Wiki Templates]]
- [[_COMMUNITY_Wiki Filename|Wiki Filename]]
- [[_COMMUNITY_Deep Research|Deep Research]]
- [[_COMMUNITY_Wiki Data Model|Wiki Data Model]]
- [[_COMMUNITY_API Types|API Types]]
- [[_COMMUNITY_Types Config|Types Config]]
- [[_COMMUNITY_Wiki Module|Wiki Module]]
- [[_COMMUNITY_FS Module|FS Module]]
- [[_COMMUNITY_API Module|API Module]]
- [[_COMMUNITY_Util Module|Util Module]]
- [[_COMMUNITY_Wikilink Enrichment|Wikilink Enrichment]]
- [[_COMMUNITY_Pipeline Module|Pipeline Module]]
- [[_COMMUNITY_Review Sweep|Review Sweep]]
- [[_COMMUNITY_Lint Pipeline|Lint Pipeline]]
- [[_COMMUNITY_Project Module|Project Module]]
- [[_COMMUNITY_LLM Module|LLM Module]]
- [[_COMMUNITY_Vector Module|Vector Module]]
- [[_COMMUNITY_Web Frontend|Web Frontend]]
- [[_COMMUNITY_Library Root|Library Root]]
- [[_COMMUNITY_MCP Module|MCP Module]]
- [[_COMMUNITY_Tests Init A|Tests Init A]]
- [[_COMMUNITY_Tests Init B|Tests Init B]]
- [[_COMMUNITY_Changes Init|Changes Init]]

## God Nodes (most connected - your core abstractions)
1. `ServerHandle` - 73 edges
2. `get_project_path_by_id()` - 23 edges
3. `Actix Web` - 21 edges
4. `vector_upsert_chunks()` - 18 edges
5. `tmp_project()` - 17 edges
6. `LLM Wiki Lite` - 17 edges
7. `auto_ingest_impl()` - 14 edges
8. `get_provider_config()` - 14 edges
9. `parse_sse_line()` - 12 edges
10. `read_file()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `rmcp crate v1.5` --semantically_similar_to--> `ServerHandle pytest fixture`  [INFERRED] [semantically similar]
  llm_wiki_lite/docs/plans/2026-05-02-mcp-server-design.md → tests/README.md
- `Actix Web` --conceptually_related_to--> `HTTP + MCP SSE Coexistence`  [INFERRED]
  llm_wiki_lite/docs/plans/2026-05-02-mcp-server-design.md → openspec/specs/mcp-server/spec.md
- `remove_page_embedding()` --calls--> `vector_delete_page()`  [INFERRED]
  llm_wiki_lite/src-server/src/pipeline/embedding.rs → llm_wiki_lite/src-server/src/vector/store.rs
- `get_embedding_count()` --calls--> `vector_count_chunks()`  [INFERRED]
  llm_wiki_lite/src-server/src/pipeline/embedding.rs → llm_wiki_lite/src-server/src/vector/store.rs
- `LLM Wiki Lite` --references--> `MM-Wiki`  [EXTRACTED]
  llm_wiki_lite/README.md → README.md

## Hyperedges (group relationships)
- **MCP Tool Implementation Stack** — wiki_server, tool_router_macro, server_handler_trait, search_wiki_tool, read_wiki_page_tool, write_wiki_page_tool, ingest_text_tool, check_ingest_status_tool [EXTRACTED 0.95]
- **MCP Configuration Hierarchy** — mcp_config, mcp_enabled_field, mcp_project_id_field, mcp_enabled_env, mcp_project_id_env, mode_cli_flag [EXTRACTED 0.95]
- **MCP Transport Modes** — sse_transport, stdio_transport, http_mode, mcp_stdio_mode, actix_web [EXTRACTED 0.90]

## Communities

### Community 0 - "API Response & Chat"
Cohesion: 0.04
Nodes (112): ApiResponse<T>, cache_path_for(), read_cache(), write_cache(), chat(), extract_frontmatter_title(), chat(), chat_with_thinking() (+104 more)

### Community 1 - "MCP Config Tests"
Cohesion: 0.04
Nodes (45): MCP 配置相关测试。  覆盖 mcp-config spec 中的所有场景： - MCP enabled with valid project_id → MC, Scenario: mcp.enabled=true but mcp.project_id is empty → MCP not initialized., POST /mcp returns 404 when project_id is not configured., REST API still works even when MCP is not initialized., Scenario: MCP_PROJECT_ID env var overrides TOML config., Scenario: MCP_ENABLED env var can disable MCP., Scenario: mcp.enabled=true + mcp.project_id set → MCP routes registered and func, POST /mcp should return 200 (not 404) when MCP is enabled with a valid project. (+37 more)

### Community 2 - "HTTP API Endpoints"
Cohesion: 0.04
Nodes (60): Actix Web, call_mcp JSON-RPC helper function, call_mcp_tool helper function, ChatRequest, MessageInput, CheckIngestStatusParams struct, check_ingest_status MCP Tool, ClipRequest (+52 more)

### Community 3 - "Configuration System"
Cohesion: 0.05
Nodes (30): Config, EmbeddingConfig, LlmConfig, McpConfig, SearchConfig, ServerConfig, test_cli(), test_mcp_config_default() (+22 more)

### Community 4 - "MCP Tools Tests"
Cohesion: 0.06
Nodes (16): MCP 工具测试。  覆盖 mcp-tools spec 中的所有场景（17/17）： - search_wiki: 有结果、无结果、缺少参数、空 query, 读取不存在的页面返回错误，并提示使用 search_wiki。, 路径包含 .. 的请求被拒绝（路径遍历攻击）。, write_wiki_page 工具测试。, 创建新页面成功，action = 'created'。, 覆盖已有页面，action = 'updated'。, 带 title 和 source_type 参数提交。, 提交后在 sources/mcp-ingest/ 目录创建文件。 (+8 more)

### Community 5 - "MCP Test Fixtures"
Cohesion: 0.06
Nodes (39): MCP-specific fixtures for the add-mcp-server change tests., Start a server with MCP enabled and a default project.      The server is automa, Start a server with MCP enabled but *no* project_id configured.      In this sta, Start a server with MCP explicitly disabled., Return sample Markdown content for wiki pages., server(), server_mcp_disabled(), server_no_project() (+31 more)

### Community 6 - "Wiki Index & Links"
Cohesion: 0.07
Nodes (32): build_deleted_keys(), clean_index_listing(), DeleteInfo, get_index_entry_re(), get_wikilink_re(), normalize_wiki_key(), strip_deleted_wikilinks(), test_clean_index_listing() (+24 more)

### Community 7 - "Ingest Pipeline"
Cohesion: 0.08
Nodes (33): auto_ingest(), ingest(), ingest_batch(), ingest_queue(), IngestBatchRequest, IngestBatchResponse, IngestRequest, IngestResponse (+25 more)

### Community 8 - "Vector Store"
Cohesion: 0.14
Nodes (38): ChunkSearchResult, ChunkUpsertInput, db_path(), drop_legacy_is_noop_when_v1_missing(), drop_legacy_removes_v1_but_leaves_v2(), fake_embedding(), legacy_row_count_returns_zero_when_absent(), legacy_row_count_sees_v1_rows() (+30 more)

### Community 9 - "System Architecture"
Cohesion: 0.08
Nodes (31): Backend API (Go), Context Budget Allocation, Deep Research, Docker Deployment, Embedding Pipeline, Filesystem Operations, Hybrid Search (Token + Vector + RRF), Ingest Pipeline (+23 more)

### Community 10 - "Ingest Analysis"
Cohesion: 0.11
Nodes (25): build_analysis_prompt(), build_ingest_analysis_prompt(), build_language_directive(), detect_language(), detect_script(), get_file_name(), IngestResult, is_safe_ingest_path() (+17 more)

### Community 11 - "Text Chunking"
Cohesion: 0.15
Nodes (22): apply_overlap(), Atom, AtomKind, Chunk, chunk_markdown(), chunk_section(), merge_small(), Piece (+14 more)

### Community 12 - "LLM Providers"
Cohesion: 0.17
Nodes (18): build_anthropic_body(), build_anthropic_headers(), build_anthropic_url(), build_google_body(), build_openai_body(), build_request(), ChatMessage, encode_model_for_url() (+10 more)

### Community 13 - "Search Pipeline"
Cohesion: 0.17
Nodes (13): build_snippet(), count_occurrences(), extract_title(), flatten_md_files(), MergedHit, SearchResult, test_tokenize_query_cjk(), test_tokenize_query_english() (+5 more)

### Community 14 - "Language Detection"
Cohesion: 0.16
Nodes (4): detect_language(), detect_latin_language(), get_script(), in_range()

### Community 15 - "Path Utilities"
Cohesion: 0.18
Nodes (4): get_file_name(), get_file_stem(), get_relative_path(), is_absolute_path()

### Community 16 - "Ingest Cache"
Cohesion: 0.36
Nodes (9): cache_path(), CacheData, CacheEntry, check_ingest_cache(), compute_hash(), load_cache(), remove_from_ingest_cache(), save_cache() (+1 more)

### Community 17 - "Panic Guard"
Cohesion: 0.38
Nodes (9): async_catches_panic(), async_catches_panic_after_await_point(), report(), run_guarded(), run_guarded_async(), sync_catches_panic_with_non_string_payload(), sync_catches_string_panic(), sync_passes_through_err() (+1 more)

### Community 18 - "Context Budget"
Cohesion: 0.36
Nodes (9): compute_context_budget(), compute_context_budget_from_size(), ContextBudget, test_budget_proportions(), test_custom_context_size(), test_default_context_budget(), test_max_page_size_respects_ceiling(), test_max_page_size_respects_floor() (+1 more)

### Community 19 - "Web Search"
Cohesion: 0.22
Nodes (6): TavilyRequest, TavilyResponse, TavilyResult, TavilyResultSnippet, web_search_with_snippet(), WebSearchResult

### Community 20 - "Wiki Templates"
Cohesion: 0.38
Nodes (5): get_template(), list_templates(), test_get_template(), test_list_templates(), WikiTemplate

### Community 21 - "Wiki Filename"
Cohesion: 0.53
Nodes (4): make_query_slug(), make_wiki_filename(), test_wiki_filename(), wiki_filename()

### Community 22 - "Deep Research"
Cohesion: 0.5
Nodes (3): ResearchResult, ResearchStatus, ResearchTask

### Community 23 - "Wiki Data Model"
Cohesion: 0.67
Nodes (2): FileNode, WikiProject

### Community 24 - "API Types"
Cohesion: 0.67
Nodes (2): ApiResponse, HealthResponse

### Community 25 - "Types Config"
Cohesion: 1.0
Nodes (0): 

### Community 26 - "Wiki Module"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "FS Module"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "API Module"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Util Module"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Wikilink Enrichment"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "Pipeline Module"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Review Sweep"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "Lint Pipeline"
Cohesion: 1.0
Nodes (0): 

### Community 34 - "Project Module"
Cohesion: 1.0
Nodes (0): 

### Community 35 - "LLM Module"
Cohesion: 1.0
Nodes (0): 

### Community 36 - "Vector Module"
Cohesion: 1.0
Nodes (0): 

### Community 37 - "Web Frontend"
Cohesion: 1.0
Nodes (1): Frontend (Web UI)

### Community 38 - "Library Root"
Cohesion: 1.0
Nodes (0): 

### Community 39 - "MCP Module"
Cohesion: 1.0
Nodes (0): 

### Community 40 - "Tests Init A"
Cohesion: 1.0
Nodes (0): 

### Community 41 - "Tests Init B"
Cohesion: 1.0
Nodes (0): 

### Community 42 - "Changes Init"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **128 isolated node(s):** `LlmConfig`, `EmbeddingConfig`, `SearchConfig`, `ServerConfig`, `Cli` (+123 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Types Config`** (1 nodes): `config.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Wiki Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `FS Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `API Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Util Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Wikilink Enrichment`** (1 nodes): `enrich_wikilinks.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pipeline Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Review Sweep`** (1 nodes): `sweep_reviews.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Lint Pipeline`** (1 nodes): `lint.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Project Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `LLM Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vector Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Web Frontend`** (1 nodes): `Frontend (Web UI)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Library Root`** (1 nodes): `lib.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `MCP Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tests Init A`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tests Init B`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Changes Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Actix Web` connect `HTTP API Endpoints` to `API Response & Chat`, `System Architecture`, `Configuration System`, `Ingest Pipeline`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Are the 65 inferred relationships involving `ServerHandle` (e.g. with `MCP-specific fixtures for the add-mcp-server change tests.` and `Start a server with MCP enabled and a default project.      The server is automa`) actually correct?**
  _`ServerHandle` has 65 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `get_project_path_by_id()` (e.g. with `.get()` and `.ok()`) actually correct?**
  _`get_project_path_by_id()` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `vector_upsert_chunks()` (e.g. with `.ok()` and `.err()`) actually correct?**
  _`vector_upsert_chunks()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `LlmConfig`, `EmbeddingConfig`, `SearchConfig` to the rest of the system?**
  _128 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `API Response & Chat` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._
- **Should `MCP Config Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._