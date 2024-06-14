import pytest
from smartrewind.backend.rekognition import Rekognition
from smartrewind.backend.sqs import Queue
from smartrewind.backend.s3 import Video
from smartrewind.tests.mocks.sqs import MockSQSResource
from smartrewind.tests.mocks.iam import MockIAMResource
from smartrewind.tests.mocks.sns import MockSNSResource
from smartrewind.tests.mocks.rekognition import MockRekognitionClient, MockRekognitionClientErrorCases
from smartrewind.tests.mocks.s3 import MockS3Resource
import os

@pytest.mark.parametrize(
    "error_cases, should_handle_exception", [
    (MockRekognitionClientErrorCases(), False),
    (MockRekognitionClientErrorCases(raise_start_person_tracking_error=True), True),
    (MockRekognitionClientErrorCases(raise_get_person_tracking_error=True), True)
])
def test_rekognition(error_cases: MockRekognitionClientErrorCases, should_handle_exception: bool):
    q = Queue("test", MockIAMResource(), MockSNSResource(), MockSQSResource())
    q.create()
    vid = Video("smartrewind/tests/test_assets/results.txt", MockS3Resource("test"), None)
    temp_test_file = "smartrewind/tests/test_assets/rekognition_temp.txt"
    if should_handle_exception:
        with pytest.raises(Exception):
            Rekognition("test", q, vid, MockRekognitionClient(error_cases)).test_person_tracking(temp_test_file)
    else:
        Rekognition("test", q, vid, MockRekognitionClient(error_cases)).test_person_tracking(temp_test_file)
    if os.path.exists(temp_test_file):
        print(f"Temp file found, deleting...")
        os.remove(temp_test_file)
