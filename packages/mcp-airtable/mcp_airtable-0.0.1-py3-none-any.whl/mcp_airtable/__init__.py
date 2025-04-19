"""Airtable MCP Server - Connect to Airtable API through MCP."""

import sys
from . import server

__version__ = "0.0.1"

def main():
    """Main entry point for the package."""
    print("Starting Airtable MCP server...", file=sys.stderr)
    server.mcp.run()

if __name__ == "__main__":
    main()