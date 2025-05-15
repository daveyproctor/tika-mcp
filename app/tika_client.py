import requests
import logging
import traceback
from typing import Tuple

def extract_metadata(file_bytes: bytes, tika_url: str) -> Tuple[dict, str]:
    logging.info(f"extract_metadata called with tika_url: {tika_url}")
    
    try:
        # Request metadata
        logging.info("Requesting metadata from Tika...")
        headers = {"Accept": "application/json"}
        meta_response = requests.put(f"{tika_url}/meta", data=file_bytes, headers=headers)
        logging.info(f"Metadata response status: {meta_response.status_code}")
        
        if meta_response.status_code != 200:
            logging.error(f"Error response from Tika metadata endpoint: {meta_response.text}")
            raise Exception(f"Tika metadata request failed with status {meta_response.status_code}: {meta_response.text}")
        
        meta = meta_response.json()
        logging.info("Successfully parsed metadata JSON")
        
        # Request text content
        logging.info("Requesting text content from Tika...")
        text_response = requests.put(f"{tika_url}/tika", data=file_bytes, headers={"Accept": "text/plain"})
        logging.info(f"Text response status: {text_response.status_code}")
        
        if text_response.status_code != 200:
            logging.error(f"Error response from Tika text endpoint: {text_response.text}")
            raise Exception(f"Tika text request failed with status {text_response.status_code}: {text_response.text}")
        
        text = text_response.text
        logging.info(f"Successfully retrieved text content (length: {len(text)})")
        
        return meta, text
    except Exception as e:
        logging.error(f"Error in extract_metadata: {e}")
        traceback.print_exc()
        logging.error(traceback.format_exc())
        raise
