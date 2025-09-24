from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import boto3
from botocore.client import Config

app = FastAPI(title="S3 Presigned URL Generator")


class PresignRequest(BaseModel):
    filename: str
    content_type: str | None = None


def get_s3_client():
    # Prefer environment variables; boto3 will also fall back to shared config
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "us-east-2")

    if not aws_access_key or not aws_secret:
        # Allow boto3 to pick up credentials from environment, shared config, or IAM role
        return boto3.client("s3", region_name=region, config=Config(signature_version="s3v4"))

    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret,
        region_name=region,
        config=Config(signature_version="s3v4"),
    )


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
