import argparse
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    """
    Configuration for the server.
    """

    db_path: Path
    """
    Path to DuckDB database file.
    """

    readonly: bool
    """
    Run server in read-only mode.
    """

    db_in_memory: bool
    """
    Use an in-memory DuckDB database.
    """

    @staticmethod
    def from_arguments() -> "Config":
        """
        Parse command line arguments.
        """
        parser = argparse.ArgumentParser(description="DuckDB MCP Server")

        parser.add_argument(
            "--db-path",
            type=Path,
            help="Path to DuckDB database file",
            required=False,
        )

        parser.add_argument(
            "--db-in-memory",
            action="store_true",
            default=True,
            help="Use an in-memory DuckDB database",
        )

        parser.add_argument(
            "--readonly",
            action="store_true",
            help="Run server in read-only mode. "
            "If the file does not exist, it is not created when connecting in read-only mode. "
            "Use duckdb.connect(), passing read_only=True. Set --db-in-memory to False to use a file. "
            "See: https://duckdb.org/docs/api/python/dbapi.html#read_only-connections",
        )

        args = parser.parse_args()
        return Config(
            db_path=args.db_path,
            db_in_memory=args.db_in_memory,
            readonly=args.readonly,
        )
