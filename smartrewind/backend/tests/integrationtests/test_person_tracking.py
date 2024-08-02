import os
import pytest

from smartrewind.backend.tests.mocks.mock_rekognition import MockRekognitionClient
from smartrewind.backend.tests.mocks.mock_iam import MockIAMResource
from smartrewind.backend.tests.mocks.mock_sns import MockSNSResource
from smartrewind.backend.tests.mocks.mock_sqs import MockSQSResource
from smartrewind.backend.tests.mocks.mock_s3 import MockS3Resource
from smartrewind.backend.sqs import Queue
from smartrewind.backend.char_segment import CharacterTracking
from smartrewind.backend.s3 import Video
from smartrewind.logger import Logger

@pytest.fixture(autouse=True)
def logger():
    yield Logger("", True)

def test_rekognition_character_tracking(logger: Logger):
    q = Queue("test", MockIAMResource(), MockSNSResource(), MockSQSResource(), logger)
    q.create()
    vid = Video("smartrewind/backend/tests/test_assets/results.txt", MockS3Resource("test"), logger, None)
    temp_test_file = "smartrewind/backend/tests/test_assets/rekognition_temp.txt"
    collection_folder = "smartrewind/assets/sample_collection"
    CharacterTracking(
        "test", 
        q, 
        vid, 
        MockRekognitionClient(), 
        MockS3Resource("test"), 
        "test", 
        collection_folder, 
        temp_test_file, 
        logger,
        None
    ).detect_faces()
    if os.path.exists(temp_test_file):
        print(f"Temp file found, deleting...")
        os.remove(temp_test_file)