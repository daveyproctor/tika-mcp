import asyncio
from app.tika_client import extract_metadata

async def extract_file_content(file_path: str, tika_url: str) -> dict:
    print(f"extract_file_content called with file_path: {file_path}, tika_url: {tika_url}")
    try:
        file_bytes = await asyncio.to_thread(read_file_bytes, file_path)
        print(f"Read {len(file_bytes)} bytes from {file_path}")
        metadata, content = await asyncio.to_thread(extract_metadata, file_bytes, tika_url)
        print("extract_metadata returned successfully")
        return {"metadata": metadata, "content": content}
    except Exception as e:
        print(f"Error in extract_file_content: {e}")
        return {"error": str(e)}

def read_file_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()
