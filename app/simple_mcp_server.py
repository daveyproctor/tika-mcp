#!/usr/bin/env python3
"""
Simple MCP server that logs all incoming messages and uses Tika to extract content.
"""

import sys
import json
import logging
import pathlib
from app.tika_client import extract_metadata

# Set up logging to a file
logging.basicConfig(
    filename='simple_mcp_server.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Main function to run the simple MCP server."""
    logging.info("Starting simple MCP server...")
    print("Starting simple MCP server...", file=sys.stderr)
    
    try:
        # Read from stdin and write to stdout
        while True:
            line = sys.stdin.readline()
            if not line:
                logging.info("End of input, exiting...")
                break
                
            logging.info(f"Received: {line.strip()}")
            print(f"Received: {line.strip()}", file=sys.stderr)
            
            try:
                # Try to parse as JSON
                message = json.loads(line)
                logging.info(f"Parsed JSON: {message}")
                
                # Handle initialize request
                if message.get("jsonrpc") == "2.0" and message.get("method") == "initialize" and "id" in message:
                    logging.info("Handling initialize request")
                    response = {
                        "jsonrpc": "2.0",
                        "id": message["id"],
                        "result": {
                            "protocolVersion": "0.1.0",
                            "name": "simple-mcp-server",
                            "version": "0.1.0",
                            "capabilities": {
                                "tools": {}
                            }
                        }
                    }
                    response_str = json.dumps(response)
                    logging.info(f"Sending response: {response_str}")
                    print(response_str)
                    sys.stdout.flush()
                
                # Handle initialized notification
                elif message.get("jsonrpc") == "2.0" and message.get("method") == "initialized" and "id" not in message:
                    logging.info("Received initialized notification")
                    # No response needed for notifications
                
                # Handle tools/list request
                elif message.get("jsonrpc") == "2.0" and message.get("method") == "tools/list" and "id" in message:
                    logging.info("Handling tools/list request")
                    response = {
                        "jsonrpc": "2.0",
                        "id": message["id"],
                        "result": {
                            "tools": [
                                {
                                    "name": "extract_file",
                                    "description": "Extract content and metadata from a file using Tika.",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "file_path": {
                                                "type": "string",
                                                "description": "Path to the file."
                                            },
                                            "tika_url": {
                                                "type": "string",
                                                "description": "URL of the running Tika server."
                                            }
                                        },
                                        "required": ["file_path", "tika_url"]
                                    }
                                }
                            ]
                        }
                    }
                    response_str = json.dumps(response)
                    logging.info(f"Sending response: {response_str}")
                    print(response_str)
                    sys.stdout.flush()
                
                # Handle tools/call request
                elif message.get("jsonrpc") == "2.0" and message.get("method") == "tools/call" and "id" in message:
                    logging.info("Handling tools/call request")
                    params = message.get("params", {})
                    tool_name = params.get("name")
                    arguments = params.get("arguments", {})
                    
                    if tool_name == "extract_file":
                        file_path = arguments.get("file_path")
                        tika_url = arguments.get("tika_url")
                        logging.info(f"Extracting file: {file_path} using Tika at {tika_url}")
                        
                        try:
                            # Read the file
                            file_path_obj = pathlib.Path(file_path)
                            with open(file_path_obj, "rb") as f:
                                file_bytes = f.read()
                            
                            # Extract metadata using Tika
                            metadata, content = extract_metadata(file_bytes, tika_url)
                            
                            # Format the response
                            response = {
                                "jsonrpc": "2.0",
                                "id": message["id"],
                                "result": {
                                    "metadata": metadata,
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": content
                                        }
                                    ]
                                }
                            }
                        except Exception as e:
                            logging.error(f"Error extracting file: {e}")
                            response = {
                                "jsonrpc": "2.0",
                                "id": message["id"],
                                "error": {
                                    "code": -32000,
                                    "message": f"Error extracting file: {str(e)}"
                                }
                            }
                        response_str = json.dumps(response)
                        logging.info(f"Sending response: {response_str}")
                        print(response_str)
                        sys.stdout.flush()
                    else:
                        # Unknown tool
                        response = {
                            "jsonrpc": "2.0",
                            "id": message["id"],
                            "error": {
                                "code": -32601,
                                "message": f"Tool not found: {tool_name}"
                            }
                        }
                        response_str = json.dumps(response)
                        logging.info(f"Sending error response: {response_str}")
                        print(response_str)
                        sys.stdout.flush()
                
                # Handle unknown request
                elif "id" in message:
                    logging.info(f"Unknown request: {message}")
                    response = {
                        "jsonrpc": "2.0",
                        "id": message["id"],
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {message.get('method')}"
                        }
                    }
                    response_str = json.dumps(response)
                    logging.info(f"Sending error response: {response_str}")
                    print(response_str)
                    sys.stdout.flush()
                
            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse JSON: {e}")
                print(f"Failed to parse JSON: {e}", file=sys.stderr)
    
    except Exception as e:
        logging.error(f"Error in simple MCP server: {e}")
        print(f"Error in simple MCP server: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
