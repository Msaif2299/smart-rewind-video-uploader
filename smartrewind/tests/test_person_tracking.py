from .test_rekognition import MockRekognitionClient
from .test_iam import MockIAMResource
from .test_sns import MockSNSResource
from .test_sqs import MockSQSResource
from .test_video import S3MockResource
from smartrewind.sqs import Queue
from smartrewind.person_tracking import CharacterTracking
from smartrewind.video import Video
import os

def test_rekognition_character_tracking():
    q = Queue("test", MockIAMResource(), MockSNSResource(), MockSQSResource())
    q.create()
    vid = Video("smartrewind/tests/test_assets/results.txt", S3MockResource("test"), None)
    temp_test_file = "smartrewind/tests/test_assets/rekognition_temp.txt"
    CharacterTracking("test", q, vid, MockRekognitionClient(), S3MockResource("test"), temp_test_file).detect_faces()
    if os.path.exists(temp_test_file):
        print(f"Temp file found, deleting...")
        os.remove(temp_test_file)