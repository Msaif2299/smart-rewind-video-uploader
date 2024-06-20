from typing import Optional

from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFileDialog

from smartrewind.ui.base_button_style import ComboButton
from smartrewind.ui.model import Model

class ChooseMetadataFileStorageButton(ComboButton):
    def __init__(self, model: Model):
        super().__init__(model)
        self.setText("Choose Metadata File Storage")

    def mousePressEvent(self, e: Optional[QMouseEvent]) -> None:
        old_metadata_storage_loc = "."
        if self.model.metadata_file_storage_location != "":
            old_metadata_storage_loc = self.model.metadata_file_storage_location
        # generally metadata file would be stored in the same folder as the video itself for easier packaging by the user
        if old_metadata_storage_loc == "." and self.model.video_file_location != "":
            old_metadata_storage_loc =  "/".join(self.model.video_file_location.split("/")[:-1])
        
        folder_location = QFileDialog.getExistingDirectory(self, "Choose Metadata File Storage Location", old_metadata_storage_loc)
        if folder_location != "" and folder_location is not None:
            self.model.metadata_file_storage_location = folder_location
        self.set_text(self.model.metadata_file_storage_location)
        self.model.status_button_update_signal.emit()
        return super().mousePressEvent(e)