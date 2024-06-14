from PyQt5.QtWidgets import QPushButton, QSizePolicy
from smartrewind.ui.display_file_loc_label import DisplayFileLocLabel
from smartrewind.ui.user_action_status_label import UserActionStatusLabel
from smartrewind.ui.model import Model

class ComboButton(QPushButton):
    def __init__(self, model: Model):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.user_action_status_label = UserActionStatusLabel()
        self.display_file_label = DisplayFileLocLabel()
        self.model = model

    def set_text(self, text: str):
        self.display_file_label.setText(text)
        if text == "":
            self.user_action_status_label.set_negative_state()
            return
        self.user_action_status_label.set_positive_state()