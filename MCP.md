# Model Context Protocol (MCP) Configuration

This document describes the MCP server configuration and tools used in the demo_project for enhanced GitHub Copilot integration and database analysis capabilities.

## MCP Servers Configuration and Setup Instructions

### Prerequisites

1. **PostgreSQL Database**: Running on `localhost:5431` (via Docker)
2. **GitHub Access**: Personal access token with repository permissions
3. **MCP-Enabled Environment**: VSCode ver 1.103.0 with GitHub Copilot and MCP support

### 1. PostgreSQL MCP Server

**Purpose**: Provides direct database connectivity and analysis capabilities to GitHub Copilot.

**Configuration**:

- install PostgreSQL extension for VSCode
- use any other postgresql MCP server, in this project I'm also using standalone `postgres_mcp_server` module (included in `pyproject.toml` so it is installed at project initialization). This needs to be explicitly added to VSCode configuration file `.vscode/mcp.json`

**Capabilities**:

- Direct SQL query execution and analysis
- Database schema inspection and documentation
- Performance analysis with EXPLAIN queries
- Index usage statistics and optimization recommendations
- Data distribution analysis
- Constraint validation and integrity checks

**Key Tools Used in This Project**:

- `pgsql_connect` - Establish database connections
- `pgsql_db_context` - Retrieve complete database schema
- `pgsql_query` - Execute read-only analytical queries
- `pgsql_modify` - Execute DDL/DML statements (when needed)
- `pgsql_disconnect` - Clean connection management

### 2. GitHub MCP Server

**Purpose**: Enables comprehensive GitHub repository management and automation.

**Configuration**:
It is automatically configured once you add this MCP server to VSCode.

**Capabilities**:

- Issue creation and management
- Pull request operations
- Repository analysis and file operations
- Workflow and CI/CD integration
- Code review automation
- Project planning and tracking

**Key Tools Used in This Project**:

- `mcp_github_create_issue` - Automated issue creation from analysis
- `mcp_github_get_me` - User authentication and repository access
- `mcp_github_list_issues` - Project tracking and management
- `mcp_github_create_pull_request` - Code change management
