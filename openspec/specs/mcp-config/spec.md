# MCP Configuration

## Purpose

This capability defines the configuration schema and CLI flags for the MCP Server integration in llm-wiki-lite.

**Status**: TBD

---

## Requirements

### Requirement: MCP configuration section
The system SHALL support a `[mcp]` configuration section in the TOML config file with the following fields:
- `enabled` (boolean, default: `true`): Whether to enable the MCP Server
- `project_id` (string, required when MCP is enabled): The UUID of the Wiki project to bind to

#### Scenario: MCP enabled with valid project
- **WHEN** the config contains `[mcp] enabled = true, project_id = "<valid-uuid>"`
- **THEN** the MCP Server starts and all tools operate on the specified project

#### Scenario: MCP disabled
- **WHEN** the config contains `[mcp] enabled = false` or no `[mcp]` section
- **THEN** the MCP endpoints are not registered and MCP functionality is not available

#### Scenario: MCP enabled without project_id
- **WHEN** the config contains `[mcp] enabled = true` but no `project_id`
- **THEN** the WikiServer initialization fails with an error log and MCP routes are not registered

### Requirement: Environment variable overrides for MCP config
The system SHALL support environment variable overrides for MCP configuration, following the existing precedence (CLI > ENV > TOML > default).

#### Scenario: Override project_id via environment
- **WHEN** the environment variable `MCP_PROJECT_ID` is set to a valid project UUID
- **THEN** the MCP Server uses that project_id regardless of the TOML config value

#### Scenario: Override enabled via environment
- **WHEN** the environment variable `MCP_ENABLED` is set to "true" or "1"
- **THEN** the MCP Server sets `mcp.enabled = true` regardless of the TOML config value

### Requirement: Startup mode CLI flag
The system SHALL support a `--mode` CLI flag to determine the startup mode:
- Default (no flag or `--mode http`): Start Actix Web HTTP server with MCP SSE endpoints
- `--mode mcp-stdio`: Start MCP stdio server only

#### Scenario: Default mode starts both HTTP and MCP SSE
- **WHEN** the server is started without `--mode` flag
- **THEN** both the HTTP REST API and MCP SSE endpoints are available

#### Scenario: MCP SSE endpoint routing
- **WHEN** the server starts in default mode with MCP enabled
- **THEN** the routes `POST /mcp` and `GET /sse` are registered in the Actix Web router
