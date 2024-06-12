import pytest
from smartrewind.rekognition import Rekognition
from smartrewind.sqs import Queue
from smartrewind.video import Video
from smartrewind.iam import IAM
from smartrewind.sns import SNS
from .test_sqs import MockSQSResource
from .test_iam import MockIAMResource
from .test_sns import MockSNSResource
from .test_video import S3MockResource
import os
from botocore.exceptions import ClientError
from dataclasses import dataclass

@dataclass
class MockRekognitionClientErrorCases:
    raise_start_person_tracking_error: bool = False
    raise_get_person_tracking_error: bool = False

class MockRekognitionClient:
    class exceptions:
        class ResourceAlreadyExistsException(BaseException):
            pass
    def __init__(self, raise_error_cases: MockRekognitionClientErrorCases = MockRekognitionClientErrorCases()) -> None:
        self.error_cases = raise_error_cases
        self.number_of_responses = 1
        self.current_response = 0
    def start_face_search(self, **kwargs):
        return self.start_person_tracking(**kwargs)
    def get_face_search(self, **kwargs):
        return self.get_person_tracking(**kwargs)
    def start_person_tracking(self, **kwargs):
        if self.error_cases.raise_start_person_tracking_error:
            raise ClientError({
                "Error": {
                    "Code": "DummyError",
                    "Message": "Start Person Tracking Failed"
                }
            }, "Start Person Tracking")
        return {
            "JobId": "xabc123"
        }
    def get_person_tracking(self, **kwargs):
        if self.error_cases.raise_get_person_tracking_error:
            raise ClientError({
                "Error": {
                    "Code": "DummyError",
                    "Message": "Get Person Tracking Failed"
                }
            }, "Get Person Tracking")
        data = {
            "JobStatus": "SUCCEEDED",
            "Persons": [
                {
                    "Timestamp": 0,
                    "Person": {
                        'Index': 0,
                        'Confidence': 99.80796813964844
                    },
                    "FaceMatches": [
                        {
                            'Similarity': 99,
                            'Face': {
                                'ExternalImageId': "test1"
                            }
                        }
                    ]
                },
                {
                    "Timestamp": 0,
                    "Person": {
                        'Index': 1,
                        'Confidence': 99.80796813964844
                    },
                    "FaceMatches": [
                        {
                            'Similarity': 99,
                            'Face': {
                                'ExternalImageId': "test2"
                            }
                        }
                    ]
                },
                {
                    "Timestamp": 3,
                    "Person": {
                        'Index': 2,
                        'Confidence': 99.80796813964844
                    },
                    "FaceMatches": [
                        {
                            'Similarity': 99,
                            'Face': {
                                'ExternalImageId': "test1"
                            }
                        }
                    ]
                },
                {
                    "Timestamp": 5,
                    "Person": {
                        'Index': 3,
                        'Confidence': 99.80796813964844
                    },
                    "FaceMatches": [
                        {
                            'Similarity': 99,
                            'Face': {
                                'ExternalImageId': "test2"
                            }
                        }
                    ]
                }
            ]
        }

        if self.current_response < self.number_of_responses:
            self.current_response += 1
            data["NextToken"] = "oshfoigjwrpojgopwkrphr0k"
        return data
    def start_segment_detection(self, **kwargs):
        return {
            "JobId": "xabc123"
        }
    def get_segment_detection(self, **kwargs):
        return {
            "JobStatus": "SUCCEEDED",
            "Segments": [
                {
                    "Type": "SHOT",
                    "StartTimestampMillis": 0,
                    "EndTimestampMillis": 3
                },
                {
                    "Type": "SHOT",
                    "StartTimestampMillis": 3,
                    "EndTimestampMillis": 5
                }
            ],
            "VideoMetadata": [
                {
                    "DurationMillis": 5
                }
            ]
        }
    def create_collection(self, **kwargs):
        pass
    def index_faces(self, **kwargs):
        pass

@pytest.mark.parametrize(
    "error_cases, should_handle_exception", [
    (MockRekognitionClientErrorCases(), False),
    (MockRekognitionClientErrorCases(raise_start_person_tracking_error=True), True),
    (MockRekognitionClientErrorCases(raise_get_person_tracking_error=True), True)
])
def test_rekognition(error_cases: MockRekognitionClientErrorCases, should_handle_exception: bool):
    q = Queue("test", MockIAMResource(), MockSNSResource(), MockSQSResource())
    q.create()
    vid = Video("smartrewind/tests/test_assets/results.txt", S3MockResource("test"), None)
    temp_test_file = "smartrewind/tests/test_assets/rekognition_temp.txt"
    if should_handle_exception:
        with pytest.raises(Exception):
            Rekognition("test", q, vid, MockRekognitionClient(error_cases)).test_person_tracking(temp_test_file)
    else:
        Rekognition("test", q, vid, MockRekognitionClient(error_cases)).test_person_tracking(temp_test_file)
    if os.path.exists(temp_test_file):
        print(f"Temp file found, deleting...")
        os.remove(temp_test_file)
