import requests
from typing import Tuple

def extract_metadata(file_bytes: bytes, tika_url: str) -> Tuple[dict, str]:
    headers = {"Accept": "application/json"}
    meta = requests.put(f"{tika_url}/meta", data=file_bytes, headers=headers).json()
    text = requests.put(f"{tika_url}/tika", data=file_bytes, headers={"Accept": "text/plain"}).text
    return meta, text
