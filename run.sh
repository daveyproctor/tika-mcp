#!/bin/bash

TIKA_URL="$1"

if [ -z "$TIKA_URL" ]; then
  echo "Usage: ./run.sh <TIKA_SERVER_URL>"
  echo "Example: ./run.sh http://localhost:9998"
  exit 1
fi

# Activate the virtual environment
source .venv/bin/activate

# Run the MCP server over stdio and inject TIKA_URL as an environment variable
TIKA_URL="$TIKA_URL" python -m app.main
