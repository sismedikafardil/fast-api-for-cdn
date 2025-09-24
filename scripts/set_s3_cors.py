"""Set an S3 bucket CORS policy to allow browser uploads from the frontend origins.

Run with the project's virtualenv active:

. .venv/bin/activate
python scripts/set_s3_cors.py

This script reads S3_BUCKET_NAME, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY from the environment
(or from the shared credentials if not set) and applies the CORS policy.
"""

import os
import json
import boto3
from botocore.exceptions import ClientError

BUCKET = os.getenv("S3_BUCKET_NAME")
REGION = os.getenv("AWS_REGION", "us-east-2")

if not BUCKET:
    raise SystemExit("Please set S3_BUCKET_NAME in the environment or .env before running this script.")

cors_configuration = {
    'CORSRules': [
        {
            'AllowedOrigins': [
                'http://localhost:5173',
                'http://127.0.0.1:5173',
                'https://sismedika.fardil.com'
            ],
            'AllowedMethods': ['GET', 'PUT', 'POST', 'HEAD', 'OPTIONS'],
            'AllowedHeaders': ['*'],
            'ExposeHeaders': ['ETag', 'x-amz-meta-custom-header'],
            'MaxAgeSeconds': 3000
        }
    ]
}

print(f"Applying CORS policy to bucket: {BUCKET} (region: {REGION})")

s3 = boto3.client('s3', region_name=REGION)
try:
    s3.put_bucket_cors(Bucket=BUCKET, CORSConfiguration=cors_configuration)
    print("CORS policy applied successfully.")
except ClientError as e:
    print("Failed to apply CORS policy:", e)
    raise

print(json.dumps(cors_configuration, indent=2))
