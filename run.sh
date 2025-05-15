#!/bin/bash
# Script to run the Tika MCP server

# Default Tika URL
TIKA_URL=${1:-http://localhost:9998}

# Activate the virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Register the MCP server if needed
python -m app.register_mcp_server

# Run the MCP server
echo "Starting Tika MCP server with Tika URL: $TIKA_URL"
python -m app.simple_mcp_server
