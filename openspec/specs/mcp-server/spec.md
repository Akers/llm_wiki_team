# MCP Server

## Purpose

This capability defines the MCP Server implementation using SSE and stdio transports, integrated with the existing Actix Web HTTP server.

**Status**: TBD

---

## Requirements

### Requirement: MCP Server with SSE transport
The system SHALL expose an MCP Server endpoint via SSE transport, integrated into the Actix Web HTTP server. The MCP SSE endpoint SHALL be accessible at `POST /mcp` for JSON-RPC requests and `GET /sse` for the SSE event stream.

#### Scenario: Agent connects via SSE
- **WHEN** an MCP client sends a GET request to `/sse`
- **THEN** the system establishes an SSE connection and sends MCP protocol events to the client

#### Scenario: Agent sends JSON-RPC request
- **WHEN** an MCP client sends a POST request to `/mcp` with a valid MCP JSON-RPC message
- **THEN** the system processes the request and returns the appropriate JSON-RPC response

#### Scenario: MCP SSE coexists with HTTP API
- **WHEN** the server is started in default mode (no `--mode` flag)
- **THEN** both the existing REST API endpoints and the MCP SSE endpoints SHALL be available on the same port

### Requirement: MCP Server with stdio transport
The system SHALL support running as an MCP Server with stdio transport when started with `--mode mcp-stdio`. In this mode, the system SHALL NOT start the Actix Web HTTP server.

#### Scenario: Start in stdio mode
- **WHEN** the server is started with `--mode mcp-stdio`
- **THEN** the system starts an MCP Server communicating over stdin/stdout and does NOT start the HTTP server

#### Scenario: Stdio mode does not bind HTTP port
- **WHEN** the server is running in stdio mode
- **THEN** no HTTP port is bound and no REST API endpoints are available

### Requirement: MCP Server using rmcp crate
The system SHALL implement the MCP protocol using the rmcp crate v1.5, leveraging its `#[tool_router]` macro for tool registration and `ServerHandler` trait for server behavior.

#### Scenario: Tool registration via macro
- **WHEN** the MCP server initializes
- **THEN** all MCP tools are registered using rmcp's `#[tool_router]` macro with proper JSON Schema definitions for parameters

### Requirement: Server info and capabilities
The MCP Server SHALL report its capabilities (tools support) and server info (name: "llm-wiki-lite", version matching the project version) when queried by MCP clients.

#### Scenario: Client requests server info
- **WHEN** an MCP client sends an `initialize` request
- **THEN** the server responds with server name "llm-wiki-lite", version, and capabilities including tools support
