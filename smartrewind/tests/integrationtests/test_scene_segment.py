from smartrewind.tests.mocks.rekognition import MockRekognitionClient
from smartrewind.tests.mocks.iam import MockIAMResource
from smartrewind.tests.mocks.sns import MockSNSResource
from smartrewind.tests.mocks.sqs import MockSQSResource
from smartrewind.tests.mocks.s3 import MockS3Resource
from smartrewind.backend.sqs import Queue
from smartrewind.backend.scene_segment import TimelineSegment
from smartrewind.backend.s3 import Video
import os

def test_rekognition_scene_segment():
    q = Queue("test", MockIAMResource(), MockSNSResource(), MockSQSResource())
    q.create()
    vid = Video("smartrewind/tests/test_assets/results.txt", MockS3Resource("test"), None)
    temp_test_file = "smartrewind/tests/test_assets/rekognition_temp.txt"
    TimelineSegment("test", q, vid, MockRekognitionClient(), temp_test_file).segment()
    if os.path.exists(temp_test_file):
        print(f"Temp file found, deleting...")
        os.remove(temp_test_file)