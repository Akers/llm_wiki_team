# Graph Report - .  (2026-04-30)

## Corpus Check
- Corpus is ~42,429 words - fits in a single context window. You may not need a graph.

## Summary
- 513 nodes · 1104 edges · 34 communities detected
- Extraction: 68% EXTRACTED · 32% INFERRED · 0% AMBIGUOUS · INFERRED: 351 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Core API & Caching|Core API & Caching]]
- [[_COMMUNITY_Web Server & Backend|Web Server & Backend]]
- [[_COMMUNITY_Wiki Cleanup & Indexing|Wiki Cleanup & Indexing]]
- [[_COMMUNITY_Ingest Pipeline & Queue|Ingest Pipeline & Queue]]
- [[_COMMUNITY_Vector Store & Search|Vector Store & Search]]
- [[_COMMUNITY_Config & Pipeline Utils|Config & Pipeline Utils]]
- [[_COMMUNITY_Auto-Ingest & LLM Prompts|Auto-Ingest & LLM Prompts]]
- [[_COMMUNITY_Project Identity|Project Identity]]
- [[_COMMUNITY_Project Manager & API|Project Manager & API]]
- [[_COMMUNITY_LLM Client & Deep Research|LLM Client & Deep Research]]
- [[_COMMUNITY_Search & RRF Merge|Search & RRF Merge]]
- [[_COMMUNITY_Embedding Pipeline|Embedding Pipeline]]
- [[_COMMUNITY_LLM Provider Adapters|LLM Provider Adapters]]
- [[_COMMUNITY_Language Detection|Language Detection]]
- [[_COMMUNITY_Ingest Cache|Ingest Cache]]
- [[_COMMUNITY_Context Budget|Context Budget]]
- [[_COMMUNITY_Project Templates|Project Templates]]
- [[_COMMUNITY_Wiki Filename Utils|Wiki Filename Utils]]
- [[_COMMUNITY_Server Config Types|Server Config Types]]
- [[_COMMUNITY_Wiki Types|Wiki Types]]
- [[_COMMUNITY_API Response Types|API Response Types]]
- [[_COMMUNITY_Config Type Defs|Config Type Defs]]
- [[_COMMUNITY_Types Module|Types Module]]
- [[_COMMUNITY_Wiki Module|Wiki Module]]
- [[_COMMUNITY_Filesystem Module|Filesystem Module]]
- [[_COMMUNITY_Utility Module|Utility Module]]
- [[_COMMUNITY_Wikilink Enrichment|Wikilink Enrichment]]
- [[_COMMUNITY_Pipeline Module|Pipeline Module]]
- [[_COMMUNITY_Review Sweep|Review Sweep]]
- [[_COMMUNITY_Markdown Lint|Markdown Lint]]
- [[_COMMUNITY_Project Module|Project Module]]
- [[_COMMUNITY_LLM Module|LLM Module]]
- [[_COMMUNITY_Vector Module|Vector Module]]
- [[_COMMUNITY_Frontend (Legacy)|Frontend (Legacy)]]

## God Nodes (most connected - your core abstractions)
1. `get_project_path_by_id()` - 23 edges
2. `vector_upsert_chunks()` - 18 edges
3. `tmp_project()` - 17 edges
4. `LLM Wiki Lite` - 17 edges
5. `auto_ingest_impl()` - 14 edges
6. `get_provider_config()` - 14 edges
7. `Actix Web 4` - 13 edges
8. `parse_sse_line()` - 12 edges
9. `read_file()` - 11 edges
10. `open_project()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `remove_page_embedding()` --calls--> `vector_delete_page()`  [INFERRED]
  llm_wiki_lite/src-server/src/pipeline/embedding.rs → llm_wiki_lite/src-server/src/vector/store.rs
- `get_embedding_count()` --calls--> `vector_count_chunks()`  [INFERRED]
  llm_wiki_lite/src-server/src/pipeline/embedding.rs → llm_wiki_lite/src-server/src/vector/store.rs
- `LLM Wiki Lite` --references--> `MM-Wiki`  [EXTRACTED]
  llm_wiki_lite/README.md → README.md
- `cascade_delete_wiki_page()` --calls--> `vector_delete_page()`  [INFERRED]
  llm_wiki_lite/src-server/src/wiki/delete.rs → llm_wiki_lite/src-server/src/vector/store.rs
- `execute_ingest_writes()` --calls--> `merge_sources_into_content()`  [INFERRED]
  llm_wiki_lite/src-server/src/pipeline/ingest.rs → llm_wiki_lite/src-server/src/wiki/sources_merge.rs

## Hyperedges (group relationships)
- **Tauri to Server Mode Transformation** — tauri_desktop_app, llm_wiki_lite, actix_web, server_mode_plan [EXTRACTED 0.95]
- **Knowledge Processing Pipeline** — ingest_pipeline, hybrid_search, embedding_pipeline, deep_research [EXTRACTED 0.95]
- **Document Ingestion Stack** — text_chunker, context_budget, two_step_cot_ingest, filesystem_operations [EXTRACTED 0.85]

## Communities

### Community 0 - "Core API & Caching"
Cohesion: 0.09
Nodes (47): cache_path_for(), read_cache(), write_cache(), post_clip(), cascade_delete_wiki_page(), decode_xml_entities(), extract_docx_markdown(), extract_docx_with_library() (+39 more)

### Community 1 - "Web Server & Backend"
Cohesion: 0.05
Nodes (46): Actix Web 4, Backend API (Go), chat(), ChatRequest, MessageInput, ClipRequest, ClipResponse, get_pending_clips() (+38 more)

### Community 2 - "Wiki Cleanup & Indexing"
Cohesion: 0.08
Nodes (32): build_deleted_keys(), clean_index_listing(), DeleteInfo, extract_frontmatter_title(), get_index_entry_re(), get_wikilink_re(), normalize_wiki_key(), strip_deleted_wikilinks() (+24 more)

### Community 3 - "Ingest Pipeline & Queue"
Cohesion: 0.09
Nodes (29): ingest(), ingest_batch(), ingest_queue(), IngestBatchRequest, IngestBatchResponse, IngestRequest, IngestResponse, cancel_all() (+21 more)

### Community 4 - "Vector Store & Search"
Cohesion: 0.14
Nodes (38): ChunkSearchResult, ChunkUpsertInput, db_path(), drop_legacy_is_noop_when_v1_missing(), drop_legacy_removes_v1_but_leaves_v2(), fake_embedding(), legacy_row_count_returns_zero_when_absent(), legacy_row_count_sees_v1_rows() (+30 more)

### Community 5 - "Config & Pipeline Utils"
Cohesion: 0.11
Nodes (30): Config, main(), __reset_project_locks_for_testing(), test_concurrent_locks_same_project(), test_different_projects_parallel(), test_with_project_lock(), with_project_lock(), apply_overlap() (+22 more)

### Community 6 - "Auto-Ingest & LLM Prompts"
Cohesion: 0.1
Nodes (30): auto_ingest(), auto_ingest_impl(), build_analysis_prompt(), build_generation_prompt(), build_ingest_analysis_prompt(), build_language_directive(), detect_language(), detect_script() (+22 more)

### Community 7 - "Project Identity"
Cohesion: 0.1
Nodes (22): ensure_project_id(), get_project_id_by_path(), identity_path(), load_registry(), ProjectIdentity, ProjectRegistryEntry, registry_path(), save_registry() (+14 more)

### Community 8 - "Project Manager & API"
Cohesion: 0.13
Nodes (24): ApiResponse<T>, extract_xlsx_markdown(), create_project(), create_project_impl(), delete_project(), list_projects(), open_project(), test_create_and_open_project() (+16 more)

### Community 9 - "LLM Client & Deep Research"
Cohesion: 0.12
Nodes (15): chat(), chat_with_thinking(), stream_chat(), execute_research(), generate_search_queries(), ResearchResult, ResearchStatus, ResearchTask (+7 more)

### Community 10 - "Search & RRF Merge"
Cohesion: 0.16
Nodes (16): build_snippet(), count_occurrences(), extract_title(), flatten_md_files(), MergedHit, rrf_merge(), search_wiki(), SearchResult (+8 more)

### Community 11 - "Embedding Pipeline"
Cohesion: 0.14
Nodes (18): ChunkMatch, embed_all_pages(), embed_page(), EmbedAllResponse, embedding_count(), embedding_embed(), embedding_embed_all(), EmbeddingCountResponse (+10 more)

### Community 12 - "LLM Provider Adapters"
Cohesion: 0.17
Nodes (18): build_anthropic_body(), build_anthropic_headers(), build_anthropic_url(), build_google_body(), build_openai_body(), build_request(), ChatMessage, encode_model_for_url() (+10 more)

### Community 13 - "Language Detection"
Cohesion: 0.16
Nodes (4): detect_language(), detect_latin_language(), get_script(), in_range()

### Community 14 - "Ingest Cache"
Cohesion: 0.36
Nodes (9): cache_path(), CacheData, CacheEntry, check_ingest_cache(), compute_hash(), load_cache(), remove_from_ingest_cache(), save_cache() (+1 more)

### Community 15 - "Context Budget"
Cohesion: 0.36
Nodes (9): compute_context_budget(), compute_context_budget_from_size(), ContextBudget, test_budget_proportions(), test_custom_context_size(), test_default_context_budget(), test_max_page_size_respects_ceiling(), test_max_page_size_respects_floor() (+1 more)

### Community 16 - "Project Templates"
Cohesion: 0.38
Nodes (5): get_template(), list_templates(), test_get_template(), test_list_templates(), WikiTemplate

### Community 17 - "Wiki Filename Utils"
Cohesion: 0.53
Nodes (4): make_query_slug(), make_wiki_filename(), test_wiki_filename(), wiki_filename()

### Community 18 - "Server Config Types"
Cohesion: 0.4
Nodes (4): EmbeddingConfig, LlmConfig, SearchConfig, ServerConfig

### Community 19 - "Wiki Types"
Cohesion: 0.67
Nodes (2): FileNode, WikiProject

### Community 20 - "API Response Types"
Cohesion: 0.67
Nodes (2): ApiResponse, HealthResponse

### Community 21 - "Config Type Defs"
Cohesion: 1.0
Nodes (0): 

### Community 22 - "Types Module"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Wiki Module"
Cohesion: 1.0
Nodes (0): 

### Community 24 - "Filesystem Module"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "Utility Module"
Cohesion: 1.0
Nodes (0): 

### Community 26 - "Wikilink Enrichment"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "Pipeline Module"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Review Sweep"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Markdown Lint"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Project Module"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "LLM Module"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Vector Module"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "Frontend (Legacy)"
Cohesion: 1.0
Nodes (1): Frontend (Web UI)

## Knowledge Gaps
- **90 isolated node(s):** `LlmConfig`, `EmbeddingConfig`, `SearchConfig`, `ServerConfig`, `Cli` (+85 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Config Type Defs`** (1 nodes): `config.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Types Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Wiki Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Filesystem Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Utility Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Wikilink Enrichment`** (1 nodes): `enrich_wikilinks.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pipeline Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Review Sweep`** (1 nodes): `sweep_reviews.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Markdown Lint`** (1 nodes): `lint.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Project Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `LLM Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vector Module`** (1 nodes): `mod.rs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Frontend (Legacy)`** (1 nodes): `Frontend (Web UI)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Actix Web 4` connect `Web Server & Backend` to `Core API & Caching`, `Embedding Pipeline`, `Ingest Pipeline & Queue`, `Project Identity`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Why does `detect_language()` connect `Language Detection` to `Wiki Cleanup & Indexing`, `Config & Pipeline Utils`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `get_project_path_by_id()` (e.g. with `list_wiki()` and `read_wiki_file()`) actually correct?**
  _`get_project_path_by_id()` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `vector_upsert_chunks()` (e.g. with `embed_page()` and `.ok()`) actually correct?**
  _`vector_upsert_chunks()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `auto_ingest_impl()` (e.g. with `read_file()` and `.new()`) actually correct?**
  _`auto_ingest_impl()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `LlmConfig`, `EmbeddingConfig`, `SearchConfig` to the rest of the system?**
  _90 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Core API & Caching` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._