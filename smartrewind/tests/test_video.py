from smartrewind.video import Video, Image
import pytest
from dataclasses import dataclass
from botocore.exceptions import ClientError
from boto3.s3.transfer import S3UploadFailedError

@dataclass    
class S3MockResourceErrorCases:
    raise_bucket_headbucket_error: bool = False
    raise_bucket_create_error: bool = False
    raise_upload_error: bool = False

class S3MockBucket:
    class Meta:
        def __init__(self, raise_error_cases: S3MockResourceErrorCases) -> None:
            self.client = self.Client(raise_error_cases.raise_bucket_headbucket_error)
        class Client:
            def __init__(self, raise_error=False) -> None:
                self.raise_error = raise_error
            def head_bucket(self, Bucket):
                if self.raise_error:
                    raise ClientError({
                        "Error": {
                            "Code": "EntityNotFound",
                            "Message": "Head Bucket Failed"
                        }
                    }, "S3 Meta Client Head Bucket")
                pass
    class buckObject:
        def __init__(self, bucket_name, raise_error:S3MockResourceErrorCases) -> None:
            self.bucket_name = bucket_name
            self.key = "test"
            self.raise_error = raise_error
        def upload_file(self, path):
            if self.raise_error.raise_upload_error:
                raise S3UploadFailedError({
                    "Error": {
                        "Code": "EntityNotFound",
                        "Message": "Upload Bucket Object Failed"
                    }
                }, "S3 Bucket Object Upload")
    def __init__(self, name, error_cases:S3MockResourceErrorCases) -> None:
        self.name = name
        self.error_cases = error_cases
        self.meta = self.Meta(error_cases)
    def create(self, CreateBucketConfiguration):
        if self.error_cases.raise_bucket_create_error:
            raise ClientError({
                "Error": {
                    "Code": "EntityNotFound",
                    "Message": "Create Bucket Failed"
                }
            }, "S3 Bucket Create")
    def Object(self, name):
        return self.buckObject(self.name, self.error_cases)

class S3MockResource:
    class meta:
        class client:
            class meta:
                region_name: str
    def __init__(self, region_name, raise_error_cases:S3MockResourceErrorCases=S3MockResourceErrorCases()) -> None:
        self.meta.client.meta.region_name = region_name
        self.raise_error_cases = raise_error_cases

    def Bucket(self, name):
        return S3MockBucket(name, self.raise_error_cases)

def test_video():
    Video("smartrewind/tests/test_assets/results.txt", S3MockResource('us-west-2'), None).get_object()

def test_video_with_object():
    Video("smartrewind/tests/test_assets/results.txt", S3MockResource('us-west-2'), {"S3Object": {"Bucket": "test", "Name": "test"}}).get_object()

def test_video_illegal_filename():
    with pytest.raises(Exception):
        Video("allthebest.txt", S3MockResource('us-west-2'), None).get_object()

def test_video_empty_filename():
    with pytest.raises(Exception):
        Video("", S3MockResource('us-west-2'), None).get_object()

def test_video_raise_head_bucket_error():
    Video("smartrewind/tests/test_assets/results.txt", S3MockResource('us-west-2', S3MockResourceErrorCases(raise_bucket_headbucket_error=True)), None).get_object()

def test_video_create_bucket_error():
    Video("smartrewind/tests/test_assets/results.txt", S3MockResource('us-west-2', S3MockResourceErrorCases(raise_bucket_headbucket_error=True, raise_bucket_create_error=True)), None).get_object()

def test_video_upload_failure():
    Video("smartrewind/tests/test_assets/results.txt", S3MockResource('us-west-2', S3MockResourceErrorCases(raise_upload_error=True)), None).get_object()

def test_image():
    Image("smartrewind/tests/test_assets/results.txt", S3MockResource('us-west-2'), None).get_object()