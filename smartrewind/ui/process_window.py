import os

from PyQt5.QtWidgets import QProgressDialog, QMessageBox
from PyQt5.QtCore import QSize

from smartrewind.ui.model import Model

LABEL_TEXT_CHAR_LIMIT = 60

class ProcessingWindow(QProgressDialog):
    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model
        self.setCancelButton(None)
        self.setLabelText("Creating metadata file...")
        self.setAutoReset(False)
        self.cancel()
        self.model.progress_machine.set_action_func(self.setValue)
        self.setRange(0, 100)
        self.setWindowTitle("Generating Metadata File")
        self.setFixedSize(QSize(500,150))
        self.completed_state_dialog_box = self.create_completed_dialog_box()

    def create_completed_dialog_box(self) -> QMessageBox:
        box = QMessageBox(self)
        box.setWindowTitle("Generation Completed!")
        box.setText("Metadata file has been successfully generated! Press 'Open' to open file location")
        box.setStandardButtons(QMessageBox.Open|QMessageBox.Close)
        box.setIcon(QMessageBox.Information)
        return box
    
    def trim_text(self, text):
        if len(text) <= 60:
            return text
        text = text[:LABEL_TEXT_CHAR_LIMIT-3] + "..."
        return text

    def setValue(self, progress: int, message: str) -> None:
        if progress < 0 or progress > 100:
            return
        self.setLabelText(self.trim_text(message))
        super().setValue(progress)
        if progress < 100:
            return
        button_pressed = self.completed_state_dialog_box.exec()
        if button_pressed == QMessageBox.Open:
            os.startfile(self.model.metadata_file_storage_location)
        self.model.reset()
        self.close()
        