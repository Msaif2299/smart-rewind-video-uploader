from smartrewind.backend.tests.mocks.rekognition import MockRekognitionClient
from smartrewind.backend.tests.mocks.iam import MockIAMResource
from smartrewind.backend.tests.mocks.sns import MockSNSResource
from smartrewind.backend.tests.mocks.sqs import MockSQSResource
from smartrewind.backend.tests.mocks.s3 import MockS3Resource
from smartrewind.backend.sqs import Queue
from smartrewind.backend.scene_segment import TimelineSegment
from smartrewind.backend.s3 import Video
import os

def test_rekognition_scene_segment():
    q = Queue("test", MockIAMResource(), MockSNSResource(), MockSQSResource())
    q.create()
    vid = Video("smartrewind/backend/tests/test_assets/results.txt", MockS3Resource("test"), None)
    temp_test_file = "smartrewind/backend/tests/test_assets/rekognition_temp.txt"
    TimelineSegment("test", q, vid, MockRekognitionClient(), temp_test_file).segment()
    if os.path.exists(temp_test_file):
        print(f"Temp file found, deleting...")
        os.remove(temp_test_file)