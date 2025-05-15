import subprocess
import json
import pathlib

def send_mcp_request(proc, type_, data):
    req = json.dumps({"type": type_, "data": data})
    proc.stdin.write(req + "\n")
    proc.stdin.flush()
    resp = proc.stdout.readline()
    print("🔁 Response:", resp.strip())

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

        # Test a file
        test_file = pathlib.Path("examples/test-ocr.pdf").resolve()
        print(f"📄 Testing {test_file}")
        send_mcp_request(proc, "extract_file", {"file_path": str(test_file), "tika_url": "http://localhost:9998"})

    finally:
        proc.kill()

if __name__ == "__main__":
    main()
