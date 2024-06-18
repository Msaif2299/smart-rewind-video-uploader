from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QHBoxLayout
import sys
from smartrewind.ui.controller import Controller
from smartrewind.ui.model import Model
from logger import Logger
import traceback
class Viewer(QMainWindow):
    def __init__(self, controller: Controller) -> None:
        super().__init__()
        self.controller = controller
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.setFixedWidth(600)
        self.setWindowTitle("Smart Rewind Metadata File Generator")
        self.create_starting_window()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

    def create_starting_window(self):
        layout = QHBoxLayout()
        layout.addWidget(self.controller.upload_video_file.user_action_status_label)
        layout.addWidget(self.controller.upload_video_file)
        layout.addWidget(self.controller.upload_video_file.display_file_label)
        self.central_layout.addLayout(layout)

        layout = QHBoxLayout()
        layout.addWidget(self.controller.choose_collection_folder.user_action_status_label)
        layout.addWidget(self.controller.choose_collection_folder)
        layout.addWidget(self.controller.choose_collection_folder.display_file_label)
        self.central_layout.addLayout(layout)

        layout = QHBoxLayout()
        layout.addWidget(self.controller.choose_metadata_file_storage_loc.user_action_status_label)
        layout.addWidget(self.controller.choose_metadata_file_storage_loc)
        layout.addWidget(self.controller.choose_metadata_file_storage_loc.display_file_label)
        self.central_layout.addLayout(layout)

        layout = QHBoxLayout()
        layout.addWidget(self.controller.start_process_button)
        self.central_layout.addLayout(layout)

def launch_app(logger: Logger):
    try:
        app = QApplication(sys.argv)
        m = Model(logger)
        c = Controller(m)
        w = Viewer(c)
        w.show()
        app.exec_()
    except Exception as e:
        logger.log(traceback.format_exc())