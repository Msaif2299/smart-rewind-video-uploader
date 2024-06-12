from smartrewind.char_segment import CharacterTracking
from smartrewind.sqs import Queue
from smartrewind.s3 import Video
from smartrewind.scene_segment import TimelineSegment
from smartrewind.compressor import extract_timeslots
from ..mocks.iam import MockIAMResource
from ..mocks.rekognition import MockRekognitionClient
from ..mocks.sns import MockSNSResource
from ..mocks.sqs import MockSQSResource
from ..mocks.s3 import MockS3Resource
import pytest
import os

@pytest.fixture()
def generated_meta_data_dict():
    name = "test"
    iam_resource = MockIAMResource()
    sns_resource = MockSNSResource()
    sqs_resource = MockSQSResource()
    rekognition_client = MockRekognitionClient()
    s3_resource = MockS3Resource('us-west-2')
    directory_path = "./smartrewind/tests/test_assets/"
    char_segments_results_file_path = directory_path+"char-segments-results-functest.txt"
    scene_segments_results_file_path = directory_path+"scene-segments-results-functest.txt"
    video_file_name = "dummy_sample_video.mp4"
    video_name = video_file_name.split(".")[0]
    output_metadata_file_path = directory_path+f"{video_name}_metadata.txt"

    video = Video(path=directory_path+video_file_name, s3_resource=s3_resource, object=None)#{"S3Object": {"Bucket": BUCKET_NAME, "Name": video_file_name}})

    queue = Queue(notif_channel_name=name, iam_resource=iam_resource, sns_resource=sns_resource, sqs_resource=sqs_resource)
    queue.create()

    processor = CharacterTracking(name=name, queue=queue, video=video, rekognition_client=rekognition_client, s3_resource=s3_resource, results_file_name=char_segments_results_file_path)
    processor.detect_faces()

    processor = TimelineSegment(name=name, queue=queue, video=video, rekognition_client=rekognition_client, results_file_name=scene_segments_results_file_path)
    processor.segment()

    extract_timeslots(char_segments_results_file_path, scene_segments_results_file_path, output_metadata_file_path)
    
    resource = None
    with open(output_metadata_file_path, "r") as f:
        data = f.read()
        if data is not None and data != "":
            resource = eval(data)
    yield resource

    def remove(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
    
    remove(char_segments_results_file_path)
    remove(scene_segments_results_file_path)
    remove(output_metadata_file_path)

"""
Basic functionality:
Upload any video, get character and scene timeslots, get combined metadata file, check whether generated metadata file is correct
"""
def test_basic_functionality(generated_meta_data_dict):
    assert generated_meta_data_dict == {"CHAR": {"test1": [[0, 3]], "test2": [[0, 5]]}, "SEG": [[0, 3], [3, 5]]}
        
        

        