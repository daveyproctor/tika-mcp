#!/usr/bin/env python3
"""
Example client for the Tika MCP server.
This demonstrates how to use the MCP server from a client perspective.
"""

import json
import subprocess
import sys
import pathlib
import time

def main():
    """Main function to demonstrate MCP client usage."""
    # Check if a file path was provided
    if len(sys.argv) < 2:
        print("Usage: python -m app.mcp_client_example <file_path>")
        print("Example: python -m app.mcp_client_example examples/test-ocr.pdf")
        return 1
    
    file_path = pathlib.Path(sys.argv[1]).resolve()
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return 1
    
    print(f"📄 Extracting content from: {file_path}")
    
    # Start the MCP server
    print("🚀 Starting Tika MCP server...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "app.simple_mcp_server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    
    try:
        # Wait a bit for the server to initialize
        time.sleep(1)
        
        # Make sure the process is still running
        if proc.poll() is not None:
            err = proc.stderr.read()
            raise RuntimeError(f"MCP server crashed early:\n{err}")
        
        print("✅ MCP server is running")
        
        # Initialize the MCP connection
        print("🔄 Initializing MCP connection...")
        init_request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "0.1.0",
                "capabilities": {}
            },
            "id": 0
        }
        proc.stdin.write(json.dumps(init_request) + "\n")
        proc.stdin.flush()
        
        init_response = proc.stdout.readline()
        init_json = json.loads(init_response)
        print("✅ MCP server initialized")
        
        # Send initialized notification
        print("📣 Sending initialized notification...")
        init_notification = {
            "jsonrpc": "2.0",
            "method": "initialized",
            "params": {}
        }
        proc.stdin.write(json.dumps(init_notification) + "\n")
        proc.stdin.flush()
        
        # List available tools
        print("📋 Listing available tools...")
        tools_request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": 1
        }
        proc.stdin.write(json.dumps(tools_request) + "\n")
        proc.stdin.flush()
        
        tools_response = proc.stdout.readline()
        tools_json = json.loads(tools_response)
        
        # Check if the extract_file tool is available
        tools = tools_json.get("result", {}).get("tools", [])
        extract_tool = None
        for tool in tools:
            if tool.get("name") == "extract_file":
                extract_tool = tool
                break
        
        if not extract_tool:
            print("❌ extract_file tool not found")
            return 1
        
        print("✅ Found extract_file tool")
        
        # Call the extract_file tool
        print("🔨 Calling extract_file tool...")
        call_request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "extract_file",
                "arguments": {
                    "file_path": str(file_path),
                    "tika_url": "http://localhost:9998"
                }
            },
            "id": 2
        }
        proc.stdin.write(json.dumps(call_request) + "\n")
        proc.stdin.flush()
        
        call_response = proc.stdout.readline()
        call_json = json.loads(call_response)
        
        # Check if the call was successful
        if "error" in call_json:
            print(f"❌ Error calling extract_file tool: {call_json['error']['message']}")
            return 1
        
        # Extract the results
        result = call_json.get("result", {})
        metadata = result.get("metadata", {})
        content_blocks = result.get("content", [])
        
        # Print the results
        print("\n📋 Metadata:")
        print(json.dumps(metadata, indent=2))
        
        print("\n📝 Content:")
        for block in content_blocks:
            if block.get("type") == "text":
                print(block.get("text"))
        
        print("\n✅ Successfully extracted content from file")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    finally:
        # Terminate the MCP server
        print("🛑 Terminating MCP server...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("⚠️ Process did not terminate, killing...")
            proc.kill()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
