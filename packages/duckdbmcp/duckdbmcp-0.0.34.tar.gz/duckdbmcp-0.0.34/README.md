# mcp-server-duckdb

[![PyPI - Version](https://img.shields.io/pypi/v/mcp-server-duckdb)](https://pypi.org/project/duckdbmcp/)
[![PyPI - License](https://img.shields.io/pypi/l/mcp-server-duckdb)](LICENSE)
[![smithery badge](https://smithery.ai/badge/mcp-server-duckdb)](https://smithery.ai/server/mcp-server-duckdb)

A Model Context Protocol (MCP) server implementation for DuckDB, providing database interaction capabilities through MCP tools.
It would be interesting to have LLM analyze it. DuckDB is suitable for local analysis.

> Forked from `https://github.com/ktanaka101/mcp-server-duckdb`

## Overview

This server enables interaction with a DuckDB database through the Model Context Protocol, providing a comprehensive set of tools for database operations including:

- SQL query execution and inspection
- Table management (creation, description, listing)
- Data import from various sources (local files, URLs, S3)
- Data export capabilities
- Schema inspection and table analysis
- Statistical summaries of table contents

The server is designed to work seamlessly with Language Models (LLMs) while maintaining data safety through optional read-only mode.

## Components

### Resources

Currently, no custom resources are implemented.

### Prompts

Currently, no custom prompts are implemented.

### Tools

The server implements the following database interaction tools:

- **query**: Execute any SQL query on the DuckDB database
  - **Input**: `query` (string) - Any valid DuckDB SQL statement
  - **Output**: Query results as text (or success message for operations like CREATE/INSERT)

- **show_tables**: Show all tables in the DuckDB database
  - **Input**: No parameters required
  - **Output**: List of table names in the database

- **describe_table**: Describe a table in the DuckDB database
  - **Input**: `table` (string) - Name of table to describe
  - **Output**: Table schema information

- **inspect_query**: Inspect a query in the DuckDB database
  - **Input**: `query` (string) - SQL query to inspect
  - **Output**: Query inspection results

- **create_table_from_path**: Create a table from a file path
  - **Input**:
    - `path` (string) - Path to the file to load
    - `table` (string, optional) - Table name to use
    - `replace` (boolean, optional) - Whether to replace existing table

- **create_table_from_url**: Create a table from a URL
  - **Input**:
    - `url` (string) - URL to the file to load
    - `table` (string, optional) - Table name to use
    - `replace` (boolean, optional) - Whether to replace existing table

- **create_table_from_s3**: Create a table from an S3 path
  - **Input**:
    - `path` (string) - S3 path to the file to load
    - `table` (string, optional) - Table name to use

- **create_table_from_csv**: Create a table from a CSV file
  - **Input**:
    - `path` (string) - Path to the CSV file
    - `table` (string, optional) - Table name to use
    - `delimiter` (string, optional) - Delimiter to use

- **summarize_table**: Get summary statistics for a table
  - **Input**: `table` (string) - Name of table to summarize
  - **Output**: Statistical summary of the table's contents

- **export_table_to_path**: Export a table to a file
  - **Input**:
    - `table` (string) - Name of table to export
    - `format` (string, optional) - Format to export as (default: parquet)
    - `path` (string, optional) - Path to export to

- **smart_load_multiple_csv_files**: Load multiple CSV files and intelligently name the tables
  - **Input**:
    - `paths` (array of strings) - List of paths to CSV files
    - `delimiter` (string, optional) - Delimiter to use for all CSV files
  - **Output**: Mapping of original table names

> [!NOTE]
> While the server provides specialized functions for common operations, it also maintains the unified `query` function for maximum flexibility. Modern LLMs can generate appropriate SQL for any database operation (SELECT, CREATE TABLE, JOIN, etc.).

> [!NOTE]
> When the server is running in `readonly` mode, DuckDB's native readonly protection is enforced.
> This ensures that the Language Model (LLM) cannot perform any write operations (CREATE, INSERT, UPDATE, DELETE), maintaining data integrity and preventing unintended changes.

## Configuration

### Required Parameters

- **db-path** (string): Path to the DuckDB database file
  - The server will automatically create the database file and parent directories if they don't exist
  - If `--readonly` is specified and the database file doesn't exist, the server will fail to start with an error

### Optional Parameters

- **--readonly**: Run server in read-only mode
  - **Description**: When this flag is set, the server operates in read-only mode. This means:
    - The DuckDB database will be opened with `read_only=True`, preventing any write operations.
    - If the specified database file does not exist, it **will not** be created.
    - **Security Benefit**: Prevents the Language Model (LLM) from performing any write operations, ensuring that the database remains unaltered.
  - **Reference**: For more details on read-only connections in DuckDB, see the [DuckDB Python API documentation](https://duckdb.org/docs/api/python/dbapi.html#read_only-connections).


## Installation

### Installing via Smithery

To install DuckDB Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/duckdbmcp):

```bash
npx -y @smithery/cli install duckdbmcp --client claude
```

### Claude Desktop Integration

Configure the MCP server in Claude Desktop's configuration file:

#### MacOS
Location: `~/Library/Application Support/Claude/claude_desktop_config.json`

#### Windows
Location: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "duckdb": {
      "command": "uvx",
      "args": [
        "duckdbmcp",
        "--db-path",
        "~/duckdbmcp/data/data.db"
      ]
    }
  }
}
```

> * Note: `~/duckdbmcp/data/data.db` should be replaced with the actual path to the DuckDB database file.

## Development

### Prerequisites

- Python with `uv` package manager
- DuckDB Python package
- MCP server dependencies

### Debugging

Debugging MCP servers can be challenging due to their stdio-based communication. We recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) for the best debugging experience.

#### Using MCP Inspector

1. Install the inspector using npm:
```bash
npx @modelcontextprotocol/inspector uv --directory ~/codes/duckdbmcp run duckdbmcp --db-path ~/duckdbmcp/data/data.db
```

2. Open the provided URL in your browser to access the debugging interface

The inspector provides visibility into:
- Request/response communication
- Tool execution
- Server state
- Error messages
