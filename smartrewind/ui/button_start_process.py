from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QSizePolicy, QPushButton
from typing import Optional
from smartrewind.ui.model import Model
from smartrewind.backend.main_process import process_video
from smartrewind.ui.process_window import ProcessingWindow
import threading

class StartProcessButton(QPushButton):
    def __init__(self, model: Model):
        super().__init__()
        self.setText("Start Process")
        self.model = model
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setEnabled(False)
        self.model.status_button_update_signal.connect(self.enable)

    def enable(self):
        self.model.refresh_generation_objects_signal.emit()
        if self.model.video_file_location != "" and self.model.collection_folder_location != "" and self.model.metadata_file_storage_location != "":
            self.setEnabled(True)
            return
        self.setEnabled(False)
    
    def mousePressEvent(self, e: Optional[QMouseEvent]) -> None:
        main_process_thread = threading.Thread(target=process_video, args=(
            self.model.iam_resource,
            self.model.sns_resource,
            self.model.sqs_resource,
            self.model.s3_resource,
            self.model.rekognition_client,
            self.model.video_file_location,
            self.model.collection_folder_location,
            self.model.metadata_file_storage_location,
            self.model.progress_machine,
        ))
        self.start_processing_window()
        main_process_thread.start()
        return super().mousePressEvent(e)
    
    def start_processing_window(self):
        window = ProcessingWindow(self.model)
        window.show()
        window.activateWindow()
