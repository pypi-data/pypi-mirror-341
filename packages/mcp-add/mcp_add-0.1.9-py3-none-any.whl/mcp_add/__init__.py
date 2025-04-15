"""Math Calculator MCP Server."""

import sys
from . import server

__version__ = "0.1.9"

def main():
    """Main entry point for the package."""
    print("Starting MCP server...", file=sys.stderr)
    server.mcp.run()

if __name__ == "__main__":
    main()