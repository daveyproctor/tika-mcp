#!/usr/bin/env python3
"""
Debug version of the test client for the MCP server.
This script includes more debugging information to help diagnose communication issues.
"""

import subprocess
import json
import pathlib
import time
import sys

def send_mcp_request(proc, method, params):
    # Format as JSON-RPC request
    req = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    })
    print(f"📤 Sending JSON-RPC request: {req}")
    proc.stdin.write(req + "\n")
    proc.stdin.flush()
    
    # Wait a bit to ensure the server has time to process
    time.sleep(1)
    
    # Check if there's any stderr output
    if proc.stderr.readable():
        stderr_data = proc.stderr.read(1024)  # Read up to 1024 bytes
        if stderr_data:
            print(f"🔴 Error output: {stderr_data}")
    
    # Try to read the response with a timeout
    print("📥 Waiting for response...")
    
    # Check if stdout is readable
    if not proc.stdout.readable():
        print("⚠️ stdout is not readable!")
        return ""
    
    # Try to read with a longer timeout
    for i in range(20):  # Try for up to 20 seconds
        if proc.stdout.readable() and proc.poll() is None:
            # Check if there's any data available to read
            import select
            readable, _, _ = select.select([proc.stdout], [], [], 0)
            if readable:
                line = proc.stdout.readline()
                if line:
                    print(f"🔁 Response received: '{line.strip()}'")
                    return line
            
            # Check stderr for any errors
            readable, _, _ = select.select([proc.stderr], [], [], 0)
            if readable:
                stderr_data = proc.stderr.read(1024)
                if stderr_data:
                    print(f"🔴 Error output during wait: {stderr_data}")
            
            print(f"⏳ No data yet, waiting... (attempt {i+1}/20)")
            time.sleep(1)
        else:
            print("⚠️ Process is no longer running or stdout is not readable")
            break
    
    print("⚠️ No response received after timeout")
    resp = ""
    
    # If no response, check if the process is still running
    if not resp.strip() and proc.poll() is not None:
        print(f"⚠️ Process exited with code: {proc.poll()}")
        if proc.stderr.readable():
            stderr_data = proc.stderr.read()
            if stderr_data:
                print(f"🔴 Final error output: {stderr_data}")
    
    return resp

def send_initialize_request(proc):
    """Send the initialize request to the MCP server."""
    req = json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "0.1.0",
            "capabilities": {}
        },
        "id": 0
    })
    print(f"📤 Sending initialize request: {req}")
    proc.stdin.write(req + "\n")
    proc.stdin.flush()
    
    # Wait for response
    print("📥 Waiting for initialize response...")
    resp = proc.stdout.readline()
    print(f"🔁 Initialize response: '{resp.strip()}'")
    
    # Send initialized notification
    init_notification = json.dumps({
        "jsonrpc": "2.0",
        "method": "initialized",
        "params": {}
    })
    print(f"📤 Sending initialized notification: {init_notification}")
    proc.stdin.write(init_notification + "\n")
    proc.stdin.flush()
    
    return resp

def main():
    # Use the current Python interpreter (which should be the virtual environment's Python)
    venv_python = sys.executable
    print(f"� Starting MCP server using Python at: {venv_python}")
    
    proc = subprocess.Popen(
        [venv_python, "-m", "app.main"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,  # Line buffered
    )
    
    try:
        # Wait a bit for the server to initialize
        print("⏳ Waiting for server initialization...")
        time.sleep(2)
        
        # Make sure the process is still running
        if proc.poll() is not None:
            err = proc.stderr.read()
            raise RuntimeError(f"MCP server crashed early:\n{err}")
        
        print("✅ MCP server is running")
        
        # Initialize the MCP connection
        print("🔄 Initializing MCP connection...")
        init_response = send_initialize_request(proc)
        
        try:
            init_json = json.loads(init_response)
            print(f"✅ MCP connection initialized with server: {init_json.get('result', {}).get('name', 'unknown')}")
        except json.JSONDecodeError:
            print("⚠️ Could not parse initialize response as JSON")
        
        # Test a file
        test_file = pathlib.Path("examples/test-ocr.pdf").resolve()
        print(f"📄 Testing file: {test_file}")
        
        # First, list available tools
        print("📋 Listing available tools...")
        tools_response = send_mcp_request(
            proc,
            "tools/list",
            {}
        )
        
        try:
            tools_json = json.loads(tools_response)
            print(f"🔧 Available tools: {json.dumps(tools_json.get('result', {}).get('tools', []), indent=2)}")
        except json.JSONDecodeError:
            print("⚠️ Could not parse tools response as JSON")
        
        # Now call the extract_file tool
        print("🔨 Calling extract_file tool...")
        response = send_mcp_request(
            proc, 
            "tools/call", 
            {
                "name": "extract_file",
                "arguments": {
                    "file_path": str(test_file),
                    "tika_url": "http://localhost:9998"
                }
            }
        )
        
        # Try to parse the response if we got one
        if response.strip():
            try:
                parsed = json.loads(response)
                print("📊 Parsed response:")
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print("⚠️ Could not parse response as JSON")
        
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

if __name__ == "__main__":
    main()
