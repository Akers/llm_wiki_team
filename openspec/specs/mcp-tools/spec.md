# MCP Tools

## Purpose

This capability defines the MCP tools exposed by the llm-wiki-lite MCP Server, enabling agents to interact with the Wiki knowledge base.

**Status**: TBD

---

## Requirements

### Requirement: search_wiki tool
The system SHALL provide an MCP tool named `search_wiki` that searches the Wiki knowledge base for pages matching the given query. The tool SHALL use the existing hybrid search pipeline (keyword + optional vector + RRF fusion).

#### Scenario: Search returns matching results
- **WHEN** an Agent calls `search_wiki` with `query` = "Rust programming"
- **THEN** the system returns up to 10 search results, each containing path, title, snippet, and score

#### Scenario: Search with no results
- **WHEN** an Agent calls `search_wiki` with `query` = "xyznonexistent123"
- **THEN** the system returns an empty results list without error

#### Scenario: Search query is required
- **WHEN** an Agent calls `search_wiki` without providing `query`
- **THEN** the system returns a tool error indicating the required parameter is missing

### Requirement: read_wiki_page tool
The system SHALL provide an MCP tool named `read_wiki_page` that reads the full Markdown content of a specified Wiki page.

#### Scenario: Read existing page
- **WHEN** an Agent calls `read_wiki_page` with `path` = "concepts/rust.md" and the page exists
- **THEN** the system returns the full Markdown content of the page

#### Scenario: Read non-existent page
- **WHEN** an Agent calls `read_wiki_page` with `path` = "nonexistent.md" and the page does not exist
- **THEN** the system returns a tool error with message suggesting to use `search_wiki` to find available pages

#### Scenario: Path traversal prevention
- **WHEN** an Agent calls `read_wiki_page` with `path` containing `..` or an absolute path
- **THEN** the system returns a tool error indicating the path is invalid for security reasons

### Requirement: write_wiki_page tool
The system SHALL provide an MCP tool named `write_wiki_page` that writes or updates a Wiki page with the provided Markdown content. The content SHALL be written directly without LLM processing.

#### Scenario: Create new page
- **WHEN** an Agent calls `write_wiki_page` with `path` = "notes/meeting-2026-05-02.md" and `content` = "# Meeting Notes\n..."
- **THEN** the system creates the Wiki page at the specified path and returns a success confirmation

#### Scenario: Overwrite existing page
- **WHEN** an Agent calls `write_wiki_page` with a `path` that already exists
- **THEN** the system overwrites the existing page content and returns a success confirmation

#### Scenario: Path traversal prevention on write
- **WHEN** an Agent calls `write_wiki_page` with `path` containing `..` or an absolute path
- **THEN** the system returns a tool error indicating the path is invalid for security reasons

### Requirement: ingest_text tool
The system SHALL provide an MCP tool named `ingest_text` that accepts raw text content and submits it to the existing LLM ingestion pipeline for intelligent processing. The tool SHALL operate asynchronously, returning a task_id immediately.

#### Scenario: Submit text for ingestion
- **WHEN** an Agent calls `ingest_text` with `content` = "Today I learned about..." and optional `title` = "Learning Notes" and `source_type` = "notes"
- **THEN** the system writes the text to a temporary file, enqueues it in the ingest queue, and returns a `task_id`

#### Scenario: Content exceeds size limit
- **WHEN** an Agent calls `ingest_text` with `content` exceeding 100KB
- **THEN** the system returns a tool error indicating the content exceeds the maximum allowed size

#### Scenario: Content parameter is required
- **WHEN** an Agent calls `ingest_text` without providing `content`
- **THEN** the system returns a tool error indicating the required parameter is missing

### Requirement: check_ingest_status tool
The system SHALL provide an MCP tool named `check_ingest_status` that queries the status of an ingestion task submitted by `ingest_text`.

#### Scenario: Query pending task
- **WHEN** an Agent calls `check_ingest_status` with a valid `task_id` that is still being processed
- **THEN** the system returns status "pending" or "processing"

#### Scenario: Query completed task
- **WHEN** an Agent calls `check_ingest_status` with a valid `task_id` that has finished processing
- **THEN** the system returns status "done" along with the list of generated Wiki page paths

#### Scenario: Query failed task
- **WHEN** an Agent calls `check_ingest_status` with a valid `task_id` where ingestion failed
- **THEN** the system returns status "error" with the error message describing the failure

#### Scenario: Query unknown task
- **WHEN** an Agent calls `check_ingest_status` with a `task_id` that does not exist
- **THEN** the system returns a tool error indicating the task was not found
