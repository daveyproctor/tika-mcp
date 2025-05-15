import asyncio
import traceback
import logging
from app.tika_client import extract_metadata

async def extract_file_content(file_path: str, tika_url: str) -> dict:
    print(f"extract_file_content called with file_path: {file_path}, tika_url: {tika_url}")
    logging.info(f"extract_file_content called with file_path: {file_path}, tika_url: {tika_url}")
    try:
        logging.info("Reading file bytes...")
        file_bytes = await asyncio.to_thread(read_file_bytes, file_path)
        print(f"Read {len(file_bytes)} bytes from {file_path}")
        logging.info(f"Read {len(file_bytes)} bytes from {file_path}")
        
        logging.info("Calling extract_metadata...")
        metadata, content = await asyncio.to_thread(extract_metadata, file_bytes, tika_url)
        print("extract_metadata returned successfully")
        logging.info("extract_metadata returned successfully")
        
        # Log a sample of the metadata and content
        logging.info(f"Metadata sample: {str(metadata)[:200]}...")
        logging.info(f"Content sample: {str(content)[:200]}...")
        
        return {"metadata": metadata, "content": content}
    except Exception as e:
        print(f"Error in extract_file_content: {e}")
        logging.error(f"Error in extract_file_content: {e}")
        traceback.print_exc()
        logging.error(traceback.format_exc())
        return {"error": str(e)}

def read_file_bytes(file_path: str) -> bytes:
    logging.info(f"Reading file: {file_path}")
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        logging.info(f"Successfully read {len(data)} bytes")
        return data
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        raise
