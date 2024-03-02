"""
Code Source: https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/s3/s3_basics/scenario_getting_started.py
"""

import boto3
from boto3.s3.transfer import S3UploadFailedError
from botocore.exceptions import ClientError
import uuid
import os

def upload(file_name) -> Exception|bool:
    if file_name is None:
        raise Exception("No filename found")
    if not os.path.exists(file_name):
        raise Exception(f"Couldn't find file {file_name}. Are you sure it exists?")
    
    bucket_name = f"msc-test-{uuid.uuid4()}"
    bucket = s3_resource.Bucket(bucket_name)
    try:
        bucket.create(
            CreateBucketConfiguration={
                "LocationConstraint": s3_resource.meta.client.meta.region_name
            }
        )
        print(f"Created demo bucket named {bucket.name}.")
    except ClientError as err:
        print(f"Tried and failed to create demo bucket {bucket_name}.")
        print(f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}")
        print(f"\nCan't continue the demo without a bucket!")
        return False

    obj = bucket.Object(os.path.basename(file_name))
    try:
        obj.upload_file(file_name)
        print(
            f"Uploaded file {file_name} into bucket {bucket.name} with key {obj.key}."
        )
    except S3UploadFailedError as err:
        print(f"Couldn't upload file {file_name} to {bucket.name}.")
        print(f"\t{err}")
        return False
    return True

if __name__=="__main__":
    os.environ['AWS_PROFILE'] = "default"
    os.environ['AWS_DEFAULT_REGION'] = "us-west-2"
    upload(s3_resource=boto3.resource("s3", region_name='us-west-2'))