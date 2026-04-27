import os
import boto3
from dotenv import load_dotenv

load_dotenv()

R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_BUCKET = os.getenv("R2_BUCKET")

s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
)


def upload_file(local_path: str, key: str) -> None:
    s3.upload_file(local_path, R2_BUCKET, key)


def download_file(key: str, local_path: str) -> None:
    s3.download_file(R2_BUCKET, key, local_path)


def create_presigned_url(key: str) -> str:
    return s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": R2_BUCKET,
            "Key": key,
        },
        ExpiresIn=3600,
    )