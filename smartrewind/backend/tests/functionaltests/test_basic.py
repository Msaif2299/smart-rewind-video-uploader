import pytest

from smartrewind.backend.tests.mocks.iam import MockIAMResource
from smartrewind.backend.tests.mocks.rekognition import MockRekognitionClient
from smartrewind.backend.tests.mocks.sns import MockSNSResource
from smartrewind.backend.tests.mocks.sqs import MockSQSResource
from smartrewind.backend.tests.mocks.s3 import MockS3Resource
from smartrewind.backend.main_process import process_video
from smartrewind.logger import Logger

@pytest.fixture()
def generated_meta_data_dict():
    iam_resource = MockIAMResource()
    sns_resource = MockSNSResource()
    sqs_resource = MockSQSResource()
    rekognition_client = MockRekognitionClient()
    s3_resource = MockS3Resource('us-west-2')
    output_directory_path = "./smartrewind/backend/tests/test_assets/"
    video_file_name = "dummy_sample_video.mp4"
    video_name = video_file_name.split(".")[0]
    output_metadata_file_path = output_directory_path+f"{video_name}_metadata.txt"
    process_video(
        iam_resource,
        sns_resource,
        sqs_resource,
        s3_resource,
        rekognition_client,
        video_file_path=output_directory_path+video_file_name,
        collection_path="./smartrewind/assets/sample_collection",
        logger=Logger("", True),
        output_metadata_file_path=output_directory_path
    )
    
    resource = None
    with open(output_metadata_file_path, "r") as f:
        data = f.read()
        if data is not None and data != "":
            resource = eval(data)
    yield resource

"""
Basic functionality:
Upload any video, get character and scene timeslots, get combined metadata file, check whether generated metadata file is correct
"""
def test_basic_functionality(generated_meta_data_dict):
    assert generated_meta_data_dict == {"CHAR": {"test1": [[0, 3]], "test2": [[0, 5]]}, "SEG": [[0, 3], [3, 5]]}
        
        

        