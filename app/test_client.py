import subprocess
import json
import pathlib

def send_mcp_request(proc, method, params):
    # Format as JSON-RPC request
    req = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    })
    print(f"📤 Sending request: {req}")
    proc.stdin.write(req + "\n")
    proc.stdin.flush()
    resp = proc.stdout.readline()
    print("🔁 Response:", resp.strip())
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
    resp = proc.stdout.readline()
    print(f"🔁 Initialize response: {resp.strip()}")
    
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
    # Start the MCP server using the virtual environment's python interpreter
    venv_python = str(pathlib.Path(".venv/bin/python").resolve())
    proc = subprocess.Popen(
        [venv_python, "-m", "app.main"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Make sure the process is still running
        if proc.poll() is not None:
            err = proc.stderr.read()
            raise RuntimeError(f"MCP server crashed early:\n{err}")

        # Initialize the MCP connection
        print("🔄 Initializing MCP connection...")
        init_response = send_initialize_request(proc)
        
        # List available tools
        print("📋 Listing available tools...")
        tools_response = send_mcp_request(proc, "tools/list", {})
        
        # Test a file
        test_file = pathlib.Path("examples/test-ocr.pdf").resolve()
        print(f"📄 Testing {test_file}")
        send_mcp_request(
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

    finally:
        proc.kill()

if __name__ == "__main__":
    main()
