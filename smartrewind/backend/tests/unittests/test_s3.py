import pytest

from smartrewind.backend.s3 import Video, Image
from smartrewind.backend.tests.mocks.mock_s3 import MockS3Resource, MockS3ResourceErrorCases
from smartrewind.logger import Logger

@pytest.fixture(autouse=True)
def logger():
    yield Logger("", True)

def test_video(logger: Logger):
    Video(
        "smartrewind/backend/tests/test_assets/results.txt", 
        MockS3Resource('us-west-2'), 
        logger, 
        None
    ).get_object()

def test_video_with_object(logger: Logger):
    Video(
        "smartrewind/backend/tests/test_assets/results.txt", 
        MockS3Resource('us-west-2'), 
        logger, 
        {"S3Object": {"Bucket": "test", "Name": "test"}}
    ).get_object()

def test_video_illegal_filename(logger: Logger):
    with pytest.raises(Exception):
        Video(
            "allthebest.txt", 
            MockS3Resource('us-west-2'), 
            logger, 
            None
        ).get_object()

def test_video_empty_filename(logger: Logger):
    with pytest.raises(Exception):
        Video(
            "", 
            MockS3Resource('us-west-2'), 
            logger, 
            None
        ).get_object()

def test_video_raise_head_bucket_error(logger: Logger):
    Video(
        "smartrewind/backend/tests/test_assets/results.txt",
        MockS3Resource('us-west-2', MockS3ResourceErrorCases(raise_bucket_headbucket_error=True)), 
        logger, 
        None
    ).get_object()

def test_video_create_bucket_error(logger: Logger):
    with pytest.raises(Exception):
        Video(
            "smartrewind/backend/tests/test_assets/results.txt", 
            MockS3Resource(
                'us-west-2', 
                MockS3ResourceErrorCases(raise_bucket_headbucket_error=True, raise_bucket_create_error=True)
            ), 
            logger, 
            None
        ).get_object()

def test_video_upload_failure(logger: Logger):
    with pytest.raises(Exception):
        Video(
            "smartrewind/backend/tests/test_assets/results.txt", 
            MockS3Resource('us-west-2', MockS3ResourceErrorCases(raise_upload_error=True)), 
            logger, 
            None
        ).get_object()

def test_image(logger: Logger):
    Image(
        "smartrewind/backend/tests/test_assets/results.txt", 
        MockS3Resource('us-west-2'), 
        logger, 
        None
    ).get_object()