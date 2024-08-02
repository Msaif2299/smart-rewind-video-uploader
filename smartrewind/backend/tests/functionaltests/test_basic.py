import pytest

from smartrewind.backend.tests.mocks.mock_iam import MockIAMResource
from smartrewind.backend.tests.mocks.mock_rekognition import MockRekognitionClient, MockRekognitionClientErrorCases
from smartrewind.backend.tests.mocks.mock_sns import MockSNSResource
from smartrewind.backend.tests.mocks.mock_sqs import MockSQSResource
from smartrewind.backend.tests.mocks.mock_s3 import MockS3Resource
from smartrewind.backend.main_process import process_video
from smartrewind.logger import Logger

@pytest.fixture()
def generated_meta_data_dict(request):
    error_cases = MockRekognitionClientErrorCases(request.param[0], request.param[1])
    iam_resource = MockIAMResource()
    sns_resource = MockSNSResource()
    sqs_resource = MockSQSResource()
    rekognition_client = MockRekognitionClient(error_cases)
    s3_resource = MockS3Resource('us-west-2')
    output_directory_path = "./smartrewind/backend/tests/test_assets/"
    video_file_name = "dummy_sample_video.mp4"
    video_name = video_file_name.split(".")[0]
    output_metadata_file_path = output_directory_path+f"{video_name}_metadata.txt"
    try:
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
    except Exception as e:
        yield str(e)
        return
    
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
@pytest.mark.parametrize('generated_meta_data_dict, expected', [
    ([False, False], {"CHAR": {"test1": [[0, 3]], "test2": [[0, 5]]}, "SEG": [[0, 3], [3, 5]]}),
    ([True, False], "Couldn't start person tracking on dummy_sample_video.mp4"),
    ([False, True], "Couldn't get items for xabc123"),
    ([True, True], "Couldn't start person tracking on dummy_sample_video.mp4")
], indirect=['generated_meta_data_dict'])
def test_basic_functionality(generated_meta_data_dict, expected):
    assert generated_meta_data_dict == expected
        
        

        