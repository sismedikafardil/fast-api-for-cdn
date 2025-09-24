from fastapi import FastAPI
from pydantic import BaseModel
import re
from typing import Optional, Dict, Any

app = FastAPI(title="Google Drive Link Generator API")


class DriveLink(BaseModel):
    share_url: str


def convert_drive_link(share_url: str) -> Optional[Dict[str, Any]]:
    """
    Convert various Google Drive share link formats into a normalized response.

    - File links like:
      - https://drive.google.com/file/d/<id>/view?... -> direct download URL
      - https://drive.google.com/open?id=<id> -> direct download URL
    - Folder links like:
      - https://drive.google.com/drive/folders/<id>
      - https://drive.google.com/drive/u/1/folders/<id>

    Returns a dict with keys: `type` ('file'|'folder'), `id`, and `link` (normalized).
    Returns None if not recognized.
    """
    if not isinstance(share_url, str):
        return None

    # 1) File id in /d/<id>/
    m = re.search(r'/d/([a-zA-Z0-9_-]+)', share_url)
    if m:
        fid = m.group(1)
        return {"type": "file", "id": fid, "link": f"https://drive.google.com/uc?export=download&id={fid}"}

    # 2) open?id=<id> or ?id=<id>
    m = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', share_url)
    if m:
        fid = m.group(1)
        return {"type": "file", "id": fid, "link": f"https://drive.google.com/uc?export=download&id={fid}"}

    # 3) Folder links: /folders/<id> (possibly under /drive/u/<n>/folders/<id>)
    m = re.search(r'/folders/([a-zA-Z0-9_-]+)', share_url)
    if m:
        fid = m.group(1)
        return {"type": "folder", "id": fid, "link": f"https://drive.google.com/drive/folders/{fid}"}

    return None


@app.post("/generate")
def generate_link(link: DriveLink):
    result = convert_drive_link(link.share_url)
    if not result:
        return {"error": "Invalid Google Drive link"}
    return result
