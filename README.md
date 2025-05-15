# Tika MCP Server

This project provides a Model Context Protocol (MCP) server for extracting content and metadata from files using Apache Tika.

## Overview

The Tika MCP server allows AI assistants to extract text and metadata from various file formats (PDF, DOCX, images with OCR, etc.) using Apache Tika. This enables AI assistants to understand and work with the content of files that users upload.

## Features

- Extract text content from various file formats
- Extract metadata (author, creation date, etc.) from files
- Support for PDF, DOCX, images, and many other formats
- Simple JSON-RPC API following the Model Context Protocol

## Requirements

- Python 3.6+
- Apache Tika server running (default: http://localhost:9998)
- MCP-compatible client

## Installation

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Register the MCP server: `python -m app.register_mcp_server`

## Usage

The Tika MCP server provides a single tool:

### `extract_file`

Extracts content and metadata from a file using Apache Tika.

**Parameters:**
- `file_path`: Path to the file to extract content from
- `tika_url`: URL of the running Tika server (default: http://localhost:9998)

**Returns:**
- `metadata`: Dictionary of metadata extracted from the file
- `content`: Array of content blocks extracted from the file

## Testing

Several test scripts are provided to verify the functionality:

- `app/test_tika_simple.py`: Tests the Tika client directly
- `app/test_simple_mcp.py`: Tests the MCP server using the JSON-RPC protocol

## Project Structure

- `app/`: Main application code
  - `simple_mcp_server.py`: MCP server implementation
  - `tika_client.py`: Client for Apache Tika
  - `model.py`: Data models and business logic
  - `register_mcp_server.py`: Script to register the MCP server
- `examples/`: Example files for testing
- `requirements.txt`: Python dependencies

## Setup

Get a venv using either:

```bash
uv venv
```
or 
```bash
python3 -m venv .venv
```

Activate the virtual environment and install dependencies:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the MCP Server

Start the Apache Tika server (if not already running):

```bash
docker run -d -p 9998:9998 apache/tika
```

Register and run the MCP server:

```bash
python -m app.register_mcp_server
```

## License

MIT
