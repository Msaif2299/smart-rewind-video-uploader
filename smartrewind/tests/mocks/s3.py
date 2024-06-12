from dataclasses import dataclass
from botocore.exceptions import ClientError
from boto3.s3.transfer import S3UploadFailedError

@dataclass    
class MockS3ResourceErrorCases:
    raise_bucket_headbucket_error: bool = False
    raise_bucket_create_error: bool = False
    raise_upload_error: bool = False

class MockS3Bucket:
    class Meta:
        def __init__(self, raise_error_cases: MockS3ResourceErrorCases) -> None:
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
                
    class buckObject:
        def __init__(self, bucket_name, raise_error:MockS3ResourceErrorCases) -> None:
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
            
    def __init__(self, name, error_cases:MockS3ResourceErrorCases) -> None:
        self.name = name
        self.error_cases = error_cases
        self.meta = self.Meta(error_cases)
    def create(self, **kwargs):
        if self.error_cases.raise_bucket_create_error:
            raise ClientError({
                "Error": {
                    "Code": "EntityNotFound",
                    "Message": "Create Bucket Failed"
                }
            }, "S3 Bucket Create")
    def Object(self, *args, **kwargs):
        return self.buckObject(self.name, self.error_cases)

class MockS3Resource:
    class meta:
        class client:
            class meta:
                region_name: str

    def __init__(self, region_name, raise_error_cases:MockS3ResourceErrorCases=MockS3ResourceErrorCases()) -> None:
        self.meta.client.meta.region_name = region_name
        self.raise_error_cases = raise_error_cases

    def Bucket(self, name):
        return MockS3Bucket(name, self.raise_error_cases)
