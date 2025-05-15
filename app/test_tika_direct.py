#!/usr/bin/env python3
"""
Direct test script for Apache Tika server connection.
This script bypasses the MCP server and directly tests the Tika API.
"""

import requests
import argparse
import pathlib
import json
import sys

def extract_metadata(file_bytes: bytes, tika_url: str):
    """Extract metadata and content from a file using Tika API directly."""
    print(f"Sending request to Tika server at {tika_url}...")
    
    # Request metadata
    print("Requesting metadata...")
    meta_response = requests.put(
        f"{tika_url}/meta", 
        data=file_bytes, 
        headers={"Accept": "application/json"}
    )
    
    print(f"Metadata response status: {meta_response.status_code}")
    if meta_response.status_code != 200:
        print(f"Error response: {meta_response.text}")
        return None, None
        
    # Request text content
    print("Requesting text content...")
    text_response = requests.put(
        f"{tika_url}/tika", 
        data=file_bytes, 
        headers={"Accept": "text/plain"}
    )
    
    print(f"Text response status: {text_response.status_code}")
    if text_response.status_code != 200:
        print(f"Error response: {text_response.text}")
        return meta_response.json(), None
    
    return meta_response.json(), text_response.text

def main():
    parser = argparse.ArgumentParser(description="Test Apache Tika server directly")
    parser.add_argument("file_path", help="Path to the file to analyze")
    parser.add_argument("--tika-url", default="http://localhost:9998", 
                        help="URL of the Tika server (default: http://localhost:9998)")
    args = parser.parse_args()
    
    file_path = pathlib.Path(args.file_path)
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist")
        sys.exit(1)
    
    print(f"Reading file: {file_path}")
    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        print(f"Successfully read {len(file_bytes)} bytes")
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    metadata, content = extract_metadata(file_bytes, args.tika_url)
    
    if metadata:
        print("\n=== METADATA ===")
        print(json.dumps(metadata, indent=2))
    else:
        print("\nNo metadata returned")
    
    if content:
        print("\n=== CONTENT ===")
        print(content[:1000])  # Print first 1000 chars to avoid overwhelming output
        if len(content) > 1000:
            print("... (content truncated)")
    else:
        print("\nNo content returned")

if __name__ == "__main__":
    main()
