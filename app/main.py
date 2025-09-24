from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from urllib.parse import quote
from dotenv import load_dotenv
import boto3
from botocore.client import Config

# Load envnya
load_dotenv()

app = FastAPI(title="S3 Presigned URL Generator")

# CORS configuration: allow frontend origins for development and production
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://sismedika.fardil.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # includes OPTIONS/POST
    allow_headers=["*"],
)

REGION = os.getenv("AWS_REGION", "us-east-2")
BUCKET = os.getenv("S3_BUCKET_NAME", "cdn-fardil-2025")
s3 = boto3.client("s3", region_name=REGION)


def get_s3_client():
    # Prefer explicit env vars, otherwise let boto3 use the provider chain
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "us-east-2")

    if not aws_access_key or not aws_secret:
        return boto3.client("s3", region_name=region, config=Config(signature_version="s3v4"))

    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret,
        region_name=region,
        config=Config(signature_version="s3v4"),
    )


class PresignRequest(BaseModel):
    filename: str
    content_type: str | None = None


@app.post("/generate-presigned-url")
def generate_presigned_url(req: PresignRequest):
    bucket = os.getenv("S3_BUCKET_NAME")
    if not bucket:
        raise HTTPException(status_code=500, detail="S3_BUCKET_NAME not configured in environment")

    s3 = get_s3_client()
    try:
        params = {"Bucket": bucket, "Key": req.filename}
        if req.content_type:
            params["ContentType"] = req.content_type

        upload_url = s3.generate_presigned_url(
            "put_object",
            Params=params,
            ExpiresIn=3600,
        )

        region = os.getenv("AWS_REGION", "us-east-2")
        public_url = f"https://{bucket}.s3.{region}.amazonaws.com/{req.filename}"

        return {"upload_url": upload_url, "public_url": public_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        key = f"uploads/{file.filename}"  # consider UUID to avoid collisions
        extra = {"ContentType": file.content_type or "application/octet-stream"}
        s3.upload_fileobj(file.file, BUCKET, key, ExtraArgs=extra)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    public_url = f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{quote(key)}"
    return {"key": key, "url": public_url}


@app.get("/health")
def health():
    return {"ok": True}
