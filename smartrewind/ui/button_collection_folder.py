from model import Model
from typing import Optional

from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFileDialog

from smartrewind.ui.base_button_style import ComboButton

class ChooseCollectionFolderButton(ComboButton):
    def __init__(self, model: Model):
        super().__init__(model)
        self.setText("Choose Collection Folder")
    
    def mousePressEvent(self, e: Optional[QMouseEvent]) -> None:
        old_collection_folder_loc = "."
        if self.model.collection_folder_location != "":
            old_collection_folder_loc = self.model.collection_folder_location
        folder_location = QFileDialog.getExistingDirectory(self, "Choose Collections Folder", old_collection_folder_loc)
        if folder_location != "" and folder_location is not None:
            self.model.collection_folder_location = folder_location
        self.set_text(self.model.collection_folder_location)
        self.model.status_button_update_signal.emit()
        return super().mousePressEvent(e)