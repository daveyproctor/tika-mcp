#!/usr/bin/env python3
"""
Register the Tika MCP server with the MCP configuration file.
"""

import os
import json
import pathlib
import argparse

def main():
    parser = argparse.ArgumentParser(description="Register the Tika MCP server with the MCP configuration file.")
    parser.add_argument("--config-path", help="Path to the MCP configuration file. If not provided, will use the default location.")
    parser.add_argument("--server-path", help="Path to the Tika MCP server script. If not provided, will use the current directory.")
    parser.add_argument("--python-path", help="Path to the Python executable. If not provided, will use the current Python executable.")
    args = parser.parse_args()
    
    # Determine the config path
    if args.config_path:
        config_path = pathlib.Path(args.config_path)
    else:
        # Default location is ~/.mcp/config.json
        config_path = pathlib.Path.home() / ".mcp" / "config.json"
    
    # Determine the server path
    if args.server_path:
        server_path = pathlib.Path(args.server_path)
    else:
        # Default is the current directory
        server_path = pathlib.Path(__file__).parent / "simple_mcp_server.py"
    
    # Determine the Python path
    if args.python_path:
        python_path = args.python_path
    else:
        # Use the current Python executable
        python_path = "python"
    
    # Create the config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load the existing config if it exists
    if config_path.exists():
        with open(config_path, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse existing config file at {config_path}. Creating a new one.")
                config = {"servers": {}}
    else:
        config = {"servers": {}}
    
    # Add or update the Tika MCP server
    server_id = "tika-mcp-server"
    server_config = {
        "name": "Tika MCP Server",
        "description": "MCP server for extracting content and metadata from files using Apache Tika.",
        "command": f"{python_path} -m app.simple_mcp_server",
        "cwd": str(pathlib.Path.cwd()),
        "transport": "stdio"
    }
    
    config["servers"][server_id] = server_config
    
    # Write the updated config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Registered Tika MCP server with ID '{server_id}' in {config_path}")
    print(f"Command: {server_config['command']}")
    print(f"Working directory: {server_config['cwd']}")

if __name__ == "__main__":
    main()
