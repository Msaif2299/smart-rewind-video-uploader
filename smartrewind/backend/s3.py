"""
Code Source: https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/s3/s3_basics/scenario_getting_started.py
"""

from boto3.s3.transfer import S3UploadFailedError
from botocore.exceptions import ClientError
import os
from typing import Dict, Optional
import json

from smartrewind.logger import Logger

BUCKET_NAME = "msc-test-final-bucket-2"

class Object:
    def __init__(self, path, s3_resource, logger: Logger, object=Optional[Dict]) -> None:
        self.path = path
        self.name = os.path.basename(path)
        self.bucket_name = BUCKET_NAME
        self.object = object
        self.s3_resource = s3_resource
        self.logger = logger
    
    def get_object(self) -> Dict:
        if self.object is None:
            self.object = self.upload()
        return self.object
        
    def upload(self) -> Optional[Dict]:
        if self.path is None or self.path == "":
            self.logger.log(Logger.Level.ERROR, {
                "message": "No filename found in uploading object"
            })
            raise Exception("No filename found")
        if not os.path.exists(self.path):
            self.logger.log(Logger.Level.ERROR, {
                "message": f"Couldn't find file {self.path}. Are you sure it exists?"
            })
            raise Exception(f"Couldn't find file {self.path}. Are you sure it exists?")
        self.bucket_name = f"msc-test-final-bucket-2"
        bucket = self.s3_resource.Bucket(self.bucket_name)
        try:
            response = bucket.meta.client.head_bucket(Bucket=self.bucket_name)
            if response is not None:
                self.logger.log(Logger.Level.INFO, {
                    "response": json.dumps(response), 
                    "api": "bucket.meta.client.head_bucket",
                    "params": json.dumps({
                        "bucket": self.bucket_name
                    })
                })
        except ClientError as err:
            self.logger.log(Logger.Level.WARNING, {
                "message": f"Bucket {self.bucket_name} does not exist, creating...",
                "error": err.response,
                "api": "bucket.meta.client.head_bucket"
            })
            try:
                response = bucket.create(
                    CreateBucketConfiguration={
                        "LocationConstraint": self.s3_resource.meta.client.meta.region_name
                    }
                )
                if response is not None:
                    self.logger.log(Logger.Level.INFO, {
                        "response": json.dumps(response), 
                        "api": "bucket.create",
                        "params": json.dumps({
                            "location_constraint": self.s3_resource.meta.client.meta.region_name
                        })
                    })
                self.logger.log(Logger.Level.INFO, {
                    "message": f"Created demo bucket named {bucket.name}."
                })
            except ClientError as err:
                self.logger.log(Logger.Level.ERROR, {
                    "message": f"Could not create bucket {self.bucket_name}, " + f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}",
                    "error": err.response,
                    "api": "bucket.create"
                })
                raise Exception(f"Could not create bucket {self.bucket_name}, " + f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}")

        obj = bucket.Object(self.name)
        try:
            response = obj.upload_file(self.path)
            if response is not None:
                self.logger.log(Logger.Level.INFO, {
                    "response": json.dumps(response), 
                    "api": "bucket.Object",
                    "params": json.dumps({
                        "path": self.path
                    })
                })
            self.logger.log(Logger.Level.INFO, {
                "message": f"Uploaded file {self.path} into bucket {bucket.name} with key {obj.key} and attributes are {obj.__dict__}"
            })
        except S3UploadFailedError as err:
            self.logger.log(Logger.Level.ERROR, {
                "message": f"Couldn't upload file {self.path} to {bucket.name}",
                "error": err.__dict__,
                "api": "bucket.Object"
            })
            raise Exception(f"Could not upload file {self.path} to {bucket.name} because {err}")
        return {"S3Object": {"Bucket": obj.bucket_name, "Name": obj.key}}

class Image(Object):
    def __init__(self, path, s3_resource, logger: Logger, object=Optional[Dict]) -> None:
        super().__init__(path, s3_resource, logger, object)

class Video(Object):
    def __init__(self, path, s3_resource, logger: Logger, object=Optional[Dict]) -> None:
        super().__init__(path, s3_resource, logger, object)