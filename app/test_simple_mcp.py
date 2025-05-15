#!/usr/bin/env python3
"""
Test script for the simple MCP server.
"""

import subprocess
import json
import pathlib
import time
import sys

def send_mcp_request(proc, method, params, request_id):
    """Send a JSON-RPC request to the MCP server."""
    req = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": request_id
    })
    print(f"📤 Sending request: {req}")
    proc.stdin.write(req + "\n")
    proc.stdin.flush()
    resp = proc.stdout.readline()
    print(f"🔁 Response: {resp.strip()}")
    return resp

def send_mcp_notification(proc, method, params):
    """Send a JSON-RPC notification to the MCP server."""
    req = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params
    })
    print(f"📤 Sending notification: {req}")
    proc.stdin.write(req + "\n")
    proc.stdin.flush()

def main():
    # Start the simple MCP server
    print("🚀 Starting simple MCP server...")
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
        init_response = send_mcp_request(
            proc,
            "initialize",
            {
                "protocolVersion": "0.1.0",
                "capabilities": {}
            },
            0
        )
        
        # Send initialized notification
        print("📣 Sending initialized notification...")
        send_mcp_notification(
            proc,
            "initialized",
            {}
        )
        
        # List available tools
        print("📋 Listing available tools...")
        tools_response = send_mcp_request(
            proc,
            "tools/list",
            {},
            1
        )
        
        # Call the extract_file tool
        print("🔨 Calling extract_file tool...")
        test_file = pathlib.Path("examples/test-ocr.pdf").resolve()
        extract_response = send_mcp_request(
            proc,
            "tools/call",
            {
                "name": "extract_file",
                "arguments": {
                    "file_path": str(test_file),
                    "tika_url": "http://localhost:9998"
                }
            },
            2
        )
        
        # Parse and print the responses
        try:
            init_json = json.loads(init_response)
            print("\n📊 Initialize response:")
            print(json.dumps(init_json, indent=2))
            
            tools_json = json.loads(tools_response)
            print("\n📊 Tools list response:")
            print(json.dumps(tools_json, indent=2))
            
            extract_json = json.loads(extract_response)
            print("\n📊 Extract file response:")
            print(json.dumps(extract_json, indent=2))
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("🛑 Terminating MCP server...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("⚠️ Process did not terminate, killing...")
            proc.kill()
        
        # Print any stderr output
        stderr_data = proc.stderr.read()
        if stderr_data:
            print("\n🔴 Server stderr output:")
            print(stderr_data)

if __name__ == "__main__":
    main()
