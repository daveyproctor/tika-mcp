# Tika MCP

This project implements an MCP (Model Compute Protocol) server that wraps Apache Tika, exposing content and metadata extraction as an MCP tool.

## Requirements

- Python 3.11+
- `uv` or `pip`
- Apache Tika running as a server (e.g., in Docker)

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Or if using pyproject.toml:

```bash
uv pip install .
```

Running the MCP
```bash
./run.sh http://localhost:9998
```

Testing
Use cline or any MCP-compatible agent to send input to this server over stdio.

Apache Tika Docker (optional)
```bash
docker run -d -p 9998:9998 apache/tika
```
