from ..mocks.rekognition import MockRekognitionClient
from ..mocks.iam import MockIAMResource
from ..mocks.sns import MockSNSResource
from ..mocks.sqs import MockSQSResource
from ..mocks.s3 import MockS3Resource
from smartrewind.sqs import Queue
from smartrewind.scene_segment import TimelineSegment
from smartrewind.s3 import Video
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