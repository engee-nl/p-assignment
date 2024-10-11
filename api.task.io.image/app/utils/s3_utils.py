import boto3
from botocore.exceptions import ClientError
import logging

s3_client = boto3.client('s3')
S3_BUCKET_NAME = "your_bucket_name"
logger = logging.getLogger(__name__)

def upload_file_to_s3(file, filename):
    try:
        s3_client.upload_fileobj(file, S3_BUCKET_NAME, filename)
        return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{filename}"
    except ClientError as e:
        logger.error(f"Error uploading file to S3: {e}")
        raise

def retrieve_original_image(filename):
    """Retrieve the original image from AWS S3."""
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=filename)
        return response['Body'].read()
    except ClientError as e:
        logger.error(f"Error retrieving file from S3: {e}")
        raise