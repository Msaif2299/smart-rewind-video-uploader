"""
Code Source: https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/s3/s3_basics/scenario_getting_started.py
"""

from boto3.s3.transfer import S3UploadFailedError
from botocore.exceptions import ClientError
import os
from typing import Dict, Optional

BUCKET_NAME = "msc-test-final-bucket-2"

class Object:
    def __init__(self, path, s3_resource, object=Optional[Dict]) -> None:
        self.path = path
        self.name = os.path.basename(path)
        self.bucket_name = BUCKET_NAME
        self.object = object
        self.s3_resource = s3_resource
    
    def get_object(self) -> Dict:
        if self.object is None:
            self.object = self.upload()
        return self.object
        
    def upload(self) -> Optional[Dict]:
        if self.path is None or self.path == "":
            raise Exception("No filename found")
        if not os.path.exists(self.path):
            raise Exception(f"Couldn't find file {self.path}. Are you sure it exists?")
        self.bucket_name = f"msc-test-final-bucket-2"
        bucket = self.s3_resource.Bucket(self.bucket_name)
        try:
            bucket.meta.client.head_bucket(Bucket=self.bucket_name)
        except ClientError as err:
            print(f"Bucket {self.bucket_name} does not exist, creating...")
            try:
                bucket.create(
                    CreateBucketConfiguration={
                        "LocationConstraint": self.s3_resource.meta.client.meta.region_name
                    }
                )
                print(f"Created demo bucket named {bucket.name}.")
            except ClientError as err:
                print(f"Tried and failed to create bucket {self.bucket_name}.")
                print(f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}")
                return None

        obj = bucket.Object(self.name)
        try:
            obj.upload_file(self.path)
            print(
                f"Uploaded file {self.path} into bucket {bucket.name} with key {obj.key} and attributes are {obj.__dict__}"
            )
        except S3UploadFailedError as err:
            print(f"Couldn't upload file {self.path} to {bucket.name}.")
            print(f"\t{err}")
            return None
        return {"S3Object": {"Bucket": obj.bucket_name, "Name": obj.key}}

class Image(Object):
    def __init__(self, path, s3_resource, object=Optional[Dict]) -> None:
        super().__init__(path, s3_resource, object)

class Video(Object):
    def __init__(self, path, s3_resource, object=Optional[Dict]) -> None:
        super().__init__(path, s3_resource, object)