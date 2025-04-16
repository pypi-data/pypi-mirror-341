import logging
from contextlib import closing
from pathlib import Path
from typing import Any, List

import duckdb
import mcp.server.stdio
import mcp.types as types
from mcp.server import Server
from duckdbmcp.lib.handler import DuckDbTools
from pydantic import AnyUrl

from duckdbmcp import Config

logger = logging.getLogger("duckdbmcp")
logger.info("Starting MCP DuckDB Server")


class DuckDBDatabase:
    def __init__(self, config: Config):
        self.config = config
        self.db_path = config.db_path
        self.db_in_memory = config.db_in_memory
        self.readonly = config.readonly

        if self.db_in_memory:
            self.handler = DuckDbTools(
                db_path=':memory:',
                read_only=self.readonly,
            )
        else:
            self.handler = DuckDbTools(
                db_path=self.db_path.as_uri(),
                read_only=self.readonly,
            )


async def main(config: Config):
    logger.info(f"Starting DuckDB MCP Server with DB path: {config.db_path}")

    db = DuckDBDatabase(config)
    server = Server("mcp-duckdb-server")

    logger.debug("Registering handlers")

    @server.list_resources()
    async def handle_list_resources() -> list[types.Resource]:
        """
        List available duckdb resources.
        """
        return []

    @server.read_resource()
    async def handle_read_resource(uri: AnyUrl) -> str:
        """
        Read a specific note's content by its URI.
        """
        return "No data"

    @server.list_prompts()
    async def handle_list_prompts() -> list[types.Prompt]:
        """
        List available prompts.
        """
        return []

    @server.get_prompt()
    async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
        """
        Generate a prompt by combining arguments with server state.
        """

        return types.GetPromptResult(
            description="No",
            messages=[],
        )

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        tools = [
            types.Tool(
                name="query",
                description="Execute a query on the DuckDB database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL query to execute",
                        },
                    },
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="is_table_exists",
                description="Check if a table exists in the DuckDB database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table": {
                            "type": "string",
                            "description": "Name of table to check"
                        }
                    },
                    "required": ["table"]
                }
            ),
            types.Tool(
                name="show_tables",
                description="Show all tables in the DuckDB database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "include_views": {
                            "type": "boolean",
                            "description": "Whether to include views in the result",
                            "default": False
                        }
                    },
                    "required": []
                }
            ),
            types.Tool(
                name="describe_table",
                description="Describe a table in the DuckDB database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table": {
                            "type": "string",
                            "description": "Name of table to describe"
                        }
                    },
                    "required": ["table"]
                }
            ),
            types.Tool(
                name="inspect_query",
                description="Inspect a query in the DuckDB database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL query to inspect"
                        }
                    },
                    "required": ["query"]
                }
            ),
            types.Tool(
                name="create_table_from_path",
                description="Create a table from a file path",
                inputSchema={
                    "type": "object", 
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to the file to load"
                        },
                        "table": {
                            "type": "string",
                            "description": "Optional table name to use"
                        },
                        "replace": {
                            "type": "boolean", 
                            "description": "Whether to replace existing table",
                            "default": False
                        }
                    },
                    "required": ["path"]
                }
            ),
            types.Tool(
                name="create_table_from_url",
                description="Create a table from a URL",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to the file to load"
                        },
                        "table": {
                            "type": "string",
                            "description": "Optional table name to use"
                        },
                        "replace": {
                            "type": "boolean",
                            "description": "Whether to replace existing table", 
                            "default": False
                        }
                    },
                    "required": ["url"]
                }
            ),
            types.Tool(
                name="create_table_from_s3",
                description="Create a table from an S3 path",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "S3 path to the file to load"
                        },
                        "table": {
                            "type": "string",
                            "description": "Optional table name to use"
                        }
                    },
                    "required": ["path"]
                }
            ),
            types.Tool(
                name="create_table_from_csv",
                description="Create a table from a CSV file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to the CSV file"
                        },
                        "table": {
                            "type": "string",
                            "description": "Optional table name to use"
                        },
                        "delimiter": {
                            "type": "string",
                            "description": "Optional delimiter to use"
                        }
                    },
                    "required": ["path"]
                }
            ),
            types.Tool(
                name="summarize_table", 
                description="Get summary statistics for a table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table": {
                            "type": "string",
                            "description": "Name of table to summarize"
                        }
                    },
                    "required": ["table"]
                }
            ),
            types.Tool(
                name="export_table_to_path",
                description="Export a table to a file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table": {
                            "type": "string", 
                            "description": "Name of table to export"
                        },
                        "format": {
                            "type": "string",
                            "description": "Format to export in (default: parquet)",
                            "default": "PARQUET"
                        },
                        "path": {
                            "type": "string",
                            "description": "Path to export to"
                        }
                    },
                    "required": ["table"]
                }
            ),
            types.Tool(
                name="smart_load_multiple_csv_files",
                description="Load multiple CSV files and intelligently name the tables based on content analysis",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "paths": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of paths to CSV files"
                        },
                        "delimiter": {
                            "type": "string",
                            "description": "Optional delimiter to use for all CSV files"
                        }
                    },
                    "required": ["paths"]
                }
            ),
        ]

        return tools

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            if not arguments:
                raise ValueError("Missing arguments")
            
            if name == "query":
                results = db.handler.run_query(arguments["query"])
                return [types.TextContent(type="text", text=str(results))]
            
            if name == "is_table_exists":
                results = db.handler.is_table_exists(arguments["table"])
                return [types.TextContent(type="text", text=str(results))]
            
            elif name == "show_tables":
                results = db.handler.show_tables(True)
                return [types.TextContent(type="text", text=str(results))]
            
            elif name == "describe_table":
                results = db.handler.describe_table(arguments["table"])
                return [types.TextContent(type="text", text=str(results))]
            
            elif name == "inspect_query":
                results = db.handler.inspect_query(arguments["query"])
                return [types.TextContent(type="text", text=str(results))]
            
            elif name == "create_table_from_path":  
                results = db.handler.create_table_from_path(
                    path=arguments["path"],
                    table=arguments.get("table"),
                    replace=arguments.get("replace", False)
                )
                return [types.TextContent(type="text", text=str(results))]
            
            elif name == "create_table_from_url":
                results = db.handler.create_table_from_path(
                    path=arguments["url"],
                    table=arguments.get("table"),
                    replace=arguments.get("replace", False)
                )
                return [types.TextContent(type="text", text=str(results))]
            
            elif name == "create_table_from_s3":
                results = db.handler.load_s3_path_to_table(
                    path=arguments["path"],
                    table=arguments.get("table")
                )
                return [types.TextContent(type="text", text=str(results))]
            
            elif name == "create_table_from_csv":
                results = db.handler.load_local_csv_to_table(
                    path=arguments["path"],
                    table=arguments.get("table"),
                    delimiter=arguments.get("delimiter")
                )
                return [types.TextContent(type="text", text=str(results))]
            
            elif name == "summarize_table":
                results = db.handler.summarize_table(arguments["table"])
                return [types.TextContent(type="text", text=str(results))]
            
            elif name == "export_table_to_path":
                results = db.handler.export_table_to_path(
                    table=arguments["table"],
                    format=arguments.get("format", "PARQUET"),
                    path=arguments.get("path")
                )
                return [types.TextContent(type="text", text=str(results))]
                
            elif name == "smart_load_multiple_csv_files":
                results = db.handler.smart_load_multiple_csv_files(
                    paths=arguments["paths"],
                    delimiter=arguments.get("delimiter"),
                )
                # Format the results as a readable table mapping with descriptions
                formatted_results = "Original Table Name → Smart Table Name → Description\n"
                formatted_results += "---------------------------------------------------------\n"
                for original in results:
                    formatted_results += f"{original}\n"
                return [types.TextContent(type="text", text=formatted_results)]
            else:
                raise ValueError(f"Unknown tool: {name}")
        except duckdb.Error as e:
            return [types.TextContent(type="text", text=f"Database error: {str(e)}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    # Run the server using stdin/stdout streams
    options = server.create_initialization_options()
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("DuckDB MCP Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            options,
        )
