#!/usr/bin/env python3
"""
Simple test script for the Tika client.
This script directly uses the tika_client.py module to extract metadata from a file.
"""

import pathlib
import json
from app.tika_client import extract_metadata

def main():
    # Test a file
    test_file = pathlib.Path("examples/test-ocr.pdf").resolve()
    print(f"📄 Testing file: {test_file}")
    
    # Read the file
    with open(test_file, "rb") as f:
        file_bytes = f.read()
    
    print(f"📊 Read {len(file_bytes)} bytes from {test_file}")
    
    # Extract metadata
    print("🔍 Extracting metadata...")
    try:
        metadata, content = extract_metadata(file_bytes, "http://localhost:9998")
        print("✅ Metadata extraction successful")
        
        # Print metadata
        print("\n📋 Metadata:")
        print(json.dumps(metadata, indent=2))
        
        # Print content (truncated if too long)
        print("\n📝 Content:")
        if len(content) > 1000:
            print(content[:1000] + "...")
        else:
            print(content)
            
    except Exception as e:
        print(f"❌ Error extracting metadata: {e}")

if __name__ == "__main__":
    main()
