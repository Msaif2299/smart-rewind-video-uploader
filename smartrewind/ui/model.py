from PyQt5.QtCore import pyqtSignal, QObject
from smartrewind.tests.mocks.iam import MockIAMResource
from smartrewind.tests.mocks.sns import MockSNSResource
from smartrewind.tests.mocks.sqs import MockSQSResource
from smartrewind.tests.mocks.s3 import MockS3Resource
from smartrewind.tests.mocks.rekognition import MockRekognitionClient
from smartrewind.progresstracker.statemachine import ProgressStateMachine
class Model(QObject):
    status_button_update_signal = pyqtSignal()
    refresh_generation_objects_signal = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.video_file_location: str = ""
        self.collection_folder_location: str = ""
        self.metadata_file_storage_location: str = ""
        self.sns_resource = MockSNSResource()
        self.s3_resource = MockS3Resource("test")
        self.sqs_resource = MockSQSResource()
        self.iam_resource = MockIAMResource()
        self.rekognition_client = MockRekognitionClient()
        self.progress_machine = ProgressStateMachine()

    def reset(self):
        self.video_file_location = ""
        self.collection_folder_location = ""
        self.metadata_file_storage_location = ""
        self.status_button_update_signal.emit()