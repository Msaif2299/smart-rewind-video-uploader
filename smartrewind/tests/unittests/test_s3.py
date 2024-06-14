from smartrewind.backend.s3 import Video, Image
import pytest
from smartrewind.tests.mocks.s3 import MockS3Resource, MockS3ResourceErrorCases

def test_video():
    Video("smartrewind/tests/test_assets/results.txt", MockS3Resource('us-west-2'), None).get_object()

def test_video_with_object():
    Video("smartrewind/tests/test_assets/results.txt", MockS3Resource('us-west-2'), {"S3Object": {"Bucket": "test", "Name": "test"}}).get_object()

def test_video_illegal_filename():
    with pytest.raises(Exception):
        Video("allthebest.txt", MockS3Resource('us-west-2'), None).get_object()

def test_video_empty_filename():
    with pytest.raises(Exception):
        Video("", MockS3Resource('us-west-2'), None).get_object()

def test_video_raise_head_bucket_error():
    Video("smartrewind/tests/test_assets/results.txt", MockS3Resource('us-west-2', MockS3ResourceErrorCases(raise_bucket_headbucket_error=True)), None).get_object()

def test_video_create_bucket_error():
    Video("smartrewind/tests/test_assets/results.txt", MockS3Resource('us-west-2', MockS3ResourceErrorCases(raise_bucket_headbucket_error=True, raise_bucket_create_error=True)), None).get_object()

def test_video_upload_failure():
    Video("smartrewind/tests/test_assets/results.txt", MockS3Resource('us-west-2', MockS3ResourceErrorCases(raise_upload_error=True)), None).get_object()

def test_image():
    Image("smartrewind/tests/test_assets/results.txt", MockS3Resource('us-west-2'), None).get_object()