import boto3

from PyQt5.QtCore import pyqtSignal, QObject

from smartrewind.backend.tests.mocks.mock_iam import MockIAMResource
from smartrewind.backend.tests.mocks.mock_sns import MockSNSResource
from smartrewind.backend.tests.mocks.mock_sqs import MockSQSResource
from smartrewind.backend.tests.mocks.mock_s3 import MockS3Resource
from smartrewind.backend.tests.mocks.mock_rekognition import MockRekognitionClient
from smartrewind.progresstracker.statemachine import ProgressStateMachine
from smartrewind.logger import Logger

class Model(QObject):
    status_button_update_signal = pyqtSignal()
    refresh_generation_objects_signal = pyqtSignal()

    def __init__(self, logger = Logger, debug=True) -> None:
        super().__init__()
        self.video_file_location: str = ""
        self.collection_folder_location: str = ""
        self.metadata_file_storage_location: str = ""
        if debug:
            self.sns_resource = MockSNSResource()
            self.s3_resource = MockS3Resource("test")
            self.sqs_resource = MockSQSResource()
            self.iam_resource = MockIAMResource()
            self.rekognition_client = MockRekognitionClient()
        else:
            self.iam_resource = boto3.resource("iam")
            self.sns_resource = boto3.resource("sns")
            self.sqs_resource = boto3.resource("sqs")
            self.rekognition_client = boto3.client("rekognition")
            self.s3_resource = boto3.resource("s3", region_name='us-west-2')
        self.progress_machine = ProgressStateMachine()
        self.logger = logger

    def reset(self):
        self.video_file_location = ""
        self.collection_folder_location = ""
        self.metadata_file_storage_location = ""
        self.status_button_update_signal.emit()