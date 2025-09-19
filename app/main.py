from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI(title="Google Drive Link Generator API")

class DriveLink(BaseModel):
    share_url: str

def convert_drive_link(share_url: str) -> str | None:
    """
    Convert Google Drive share link -> direct download link
    Example:
    https://drive.google.com/file/d/1xYzABC123/view?usp=sharing
    =>
    https://drive.google.com/uc?export=download&id=1xYzABC123
    """
    match = re.search(r'/d/([^/]+)/', share_url)
    if match:
        return f"https://drive.google.com/uc?export=download&id={match.group(1)}"
    return None

@app.post("/generate")
def generate_link(link: DriveLink):
    direct_link = convert_drive_link(link.share_url)
    if not direct_link:
        return {"error": "Invalid Google Drive link"}
    return {"direct_link": direct_link}
