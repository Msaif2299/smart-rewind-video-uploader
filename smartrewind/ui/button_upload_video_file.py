from typing import Optional

from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFileDialog

from smartrewind.ui.base_button_style import ComboButton
from smartrewind.ui.model import Model

class UploadVideoFileButton(ComboButton):
    def __init__(self, model: Model):
        super().__init__(model)
        self.setText("Upload Video File")
    
    def mousePressEvent(self, e: Optional[QMouseEvent]) -> None:
        opening_directory = "."
        # open the folder of the video
        if self.model.video_file_location != "":
            opening_directory = "/".join(self.model.video_file_location.split("/")[:-1])
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Upload Video File", 
            opening_directory, 
            "Video (*.mp4)")
        if filename != "" and filename is not None:
            self.model.video_file_location = filename
        self.set_text(self.model.video_file_location)
        self.model.status_button_update_signal.emit()
        return super().mousePressEvent(e)